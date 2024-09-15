import cv2
import numpy as np
import logging
from datetime import datetime
from collections import deque
import os 


# Create the log directory if it doesn't exist
log_dir = 'backend/log'
os.makedirs(log_dir, exist_ok=True)

# Generate a timestamp for unique log file naming
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = os.path.join(log_dir, f'tool_tracking_{timestamp}.log')

# Set up logging with a unique filename
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Open cameras
cam0 = cv2.VideoCapture(0)  # Tool field camera
cam1 = cv2.VideoCapture(2)  # Discard area camera
cam2 = cv2.VideoCapture(2)  # Additional camera (e.g., work area camera)

# Define color ranges in HSV for each tool (example colors)
color_ranges = {
    'neon_green': [(35, 100, 100), (85, 255, 255)],  # Neon Green
    'neon_pink': [(140, 100, 100), (180, 255, 255)], # Neon Pink
    'neon_blue': [(90, 100, 100), (130, 255, 255)]  # Neon Blue
}


# Initialize a deque to store recent log entries
log_entries = deque(maxlen=10)  # Adjust maxlen as needed

def standardize_frame(frame, target_width=640, target_height=480):
    """Resize and pad the frame to reach the target dimensions."""
    h, w = frame.shape[:2]
    scale = min(target_width/w, target_height/h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h))
    result = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    x_offset, y_offset = (target_width - new_w) // 2, (target_height - new_h) // 2
    result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return result

def detect_tools(frame, color_ranges):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detected_tools = {}

    for tool_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_tools[tool_name] = []
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                detected_tools[tool_name].append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, tool_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame, detected_tools

def initialize_tool_counts(frame):
    _, detected_tools = detect_tools(frame, color_ranges)
    return {tool: {'total': len(detections), 'in_field': len(detections), 'in_use': 0, 'discarded': 0} 
            for tool, detections in detected_tools.items()}

def update_tool_counts(tool_counts, detected_tools_field, detected_tools_discard):
    for tool, counts in tool_counts.items():
        field_count = len(detected_tools_field.get(tool, []))
        discard_count = len(detected_tools_discard.get(tool, []))
        
        # Update tool field count
        if field_count != counts['in_field']:
            difference = counts['in_field'] - field_count
            counts['in_use'] += difference
            counts['in_field'] = field_count
            log_entry = f"{tool}: {abs(difference)} {'removed from' if difference > 0 else 'returned to'} tool field. In field: {field_count}, In use: {counts['in_use']}"
            logging.info(log_entry)
            log_entries.appendleft(log_entry)
        
        # Update discard count
        if discard_count > counts['discarded']:
            difference = discard_count - counts['discarded']
            counts['in_use'] -= difference
            counts['discarded'] = discard_count
            log_entry = f"{tool}: {difference} discarded. In use: {counts['in_use']}, Discarded: {discard_count}"
            logging.info(log_entry)
            log_entries.appendleft(log_entry)

def display_tool_counts(frame, tool_counts):
    y_offset = 30
    for tool, counts in tool_counts.items():
        text = f"{tool}: Total: {counts['total']}, Field: {counts['in_field']}, Use: {counts['in_use']}, Discarded: {counts['discarded']}"
        cv2.putText(frame, text, (10, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 30
    return frame

def add_camera_label(frame, label):
    cv2.putText(frame, label, (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return frame

def create_log_display(width, height):
    log_display = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(log_display, "Live Log", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    y_offset = 60
    for entry in log_entries:
        cv2.putText(log_display, entry, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y_offset += 30
        if y_offset > height - 30:
            break
    
    return log_display

# Video writers for saving the output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out0 = cv2.VideoWriter('output_tool_field.avi', fourcc, 20.0, (640, 480))
out1 = cv2.VideoWriter('output_discard.avi', fourcc, 20.0, (640, 480))
out2 = cv2.VideoWriter('output_camera_3.avi', fourcc, 20.0, (640, 480))

logging.info("Starting tool tracking system")

# Initialize tool counts
ret, initial_frame = cam0.read()
if not ret:
    logging.error("Failed to grab initial frame from tool field camera")
    exit(1)
initial_frame = standardize_frame(initial_frame)
tool_counts = initialize_tool_counts(initial_frame)
logging.info(f"Initial tool counts: {tool_counts}")

while True:
    ret0, frame0 = cam0.read()
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret0 and not ret1 and not ret2:
        logging.error("All cameras failed to grab frames")
        break

    if not ret0:
        frame0 = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame0, "Tool Field Camera Failed", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        frame0 = standardize_frame(frame0)

    if not ret1:
        frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame1, "Discard Camera Failed", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        frame1 = standardize_frame(frame1)

    if not ret2:
        frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame2, "Camera 3 Failed", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        frame2 = standardize_frame(frame2)

    frame0, detected_tools_field = detect_tools(frame0, color_ranges)
    frame1, detected_tools_discard = detect_tools(frame1, color_ranges)
    frame2, detected_tools_additional = detect_tools(frame2, color_ranges)

    update_tool_counts(tool_counts, detected_tools_field, detected_tools_discard)

    frame2 = display_tool_counts(frame2, tool_counts)

    frame0 = add_camera_label(frame0, "Tool Field")
    frame1 = add_camera_label(frame1, "Discard Area")
    frame2 = add_camera_label(frame2, "Camera 3")

    log_display = create_log_display(640, 480)

    # Stack the frames in a 2x2 grid: frame0 (Tool Field), frame1 (Discard Area), frame2 (Camera 3), and log display
    top_row = np.hstack((frame0, frame1))
    bottom_row = np.hstack((frame2, log_display))
    combined_frame = np.vstack((top_row, bottom_row))

    cv2.imshow('Tool Tracking System', combined_frame)

    # Save the frames
    out0.write(frame0)
    out1.write(frame1)
    out2.write(frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cam0.release()
cam1.release()
cam2.release()
out0.release()
out1.release()
out2.release()
cv2.destroyAllWindows()
