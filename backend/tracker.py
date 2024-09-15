import cv2
import numpy as np
import logging
from datetime import datetime
from collections import deque
import os

class ToolTracker:
    def __init__(self, log_dir='backend/log'):
        # Initialize logging
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_filename = os.path.join(log_dir, f'tool_tracking_{timestamp}.log')

        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        
        self.log_entries = deque(maxlen=10)

        # Initialize cameras
        self.cam0 = cv2.VideoCapture(0)  # Tool field camera
        self.cam1 = cv2.VideoCapture(2)  # Discard area camera
        self.cam2 = cv2.VideoCapture(1)  # Additional camera (e.g., work area camera)

        # Tool color ranges
        self.color_ranges = {
            'Tool1': [(35, 100, 100), (85, 255, 255)],  # Neon Green
            'Tool2': [(140, 100, 100), (180, 255, 255)],  # Neon Pink
            'Tool3': [(90, 100, 100), (130, 255, 255)]   # Neon Blue
        }

        # Tool counts
        self.tool_counts = {}

    def standardize_frame(self, frame, target_width=640, target_height=480):
        """Resize and pad the frame to reach the target dimensions."""
        h, w = frame.shape[:2]
        scale = min(target_width/w, target_height/h)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h))
        result = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        x_offset, y_offset = (target_width - new_w) // 2, (target_height - new_h) // 2
        result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        return result

    def detect_tools(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        detected_tools = {}

        for tool_name, (lower, upper) in self.color_ranges.items():
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            detected_tools[tool_name] = []
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    detected_tools[tool_name].append((x, y, w, h))
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, tool_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            print(f"{tool_name}: {len(detected_tools[tool_name])} detections")

        return frame, detected_tools


        return frame, detected_tools

    def initialize_tool_counts(self, frame):
        _, detected_tools = self.detect_tools(frame)

        # Initialize tool counts with unique detections
        self.tool_counts = {}
        for tool, detections in detected_tools.items():
            # Count the unique detections of each tool
            self.tool_counts[tool] = {
                'total': len(detections),          # Total detected in the frame
                'in_field': len(detections),       # Initially, all detected are in the field
                'in_use': 0,
                'discarded': 0
            }


    def update_tool_counts(self, detected_tools_field, detected_tools_discard):
        for tool, counts in self.tool_counts.items():
            field_count = len(detected_tools_field.get(tool, []))
            discard_count = len(detected_tools_discard.get(tool, []))

            print(f"Updating counts for {tool}: field={field_count}, discard={discard_count}, in_use={counts['in_use']}")  # Debugging line

            if field_count != counts['in_field']:
                difference = counts['in_field'] - field_count
                counts['in_use'] += difference
                counts['in_field'] = field_count
                log_entry = f"{tool}: {abs(difference)} {'removed from' if difference > 0 else 'returned to'} tool field. In field: {field_count}, In use: {counts['in_use']}"
                logging.info(log_entry)
                self.log_entries.appendleft(log_entry)

            if discard_count > counts['discarded']:
                difference = discard_count - counts['discarded']
                counts['in_use'] -= difference
                counts['discarded'] = discard_count
                log_entry = f"{tool}: {difference} discarded. In use: {counts['in_use']}, Discarded: {discard_count}"
                logging.info(log_entry)
                self.log_entries.appendleft(log_entry)


    def display_tool_counts(self, frame):
        y_offset = 30
        for tool, counts in self.tool_counts.items():
            text = f"{tool}: Total: {counts['total']}, Field: {counts['in_field']}, Use: {counts['in_use']}, Discarded: {counts['discarded']}"
            cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
        return frame

    def create_log_display(self, width=640, height=480):
        log_display = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(log_display, "Live Log", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        y_offset = 60
        for entry in self.log_entries:
            cv2.putText(log_display, entry, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 30
            if y_offset > height - 30:
                break

        return log_display

    def release_resources(self):
        self.cam0.release()
        self.cam1.release()
        self.cam2.release()
        cv2.destroyAllWindows()

    # Add additional utility functions as necessary for your Flask backend

