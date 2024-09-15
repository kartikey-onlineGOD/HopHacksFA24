from flask import Flask, Response, send_from_directory
from flask_cors import CORS
from tracker import ToolTracker
import cv2
import numpy as np
from flask import jsonify
import os 



app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

tracker = ToolTracker()

def generate_frames():
    while True:
        ret0, frame0 = tracker.cam0.read()
        ret1, frame1 = tracker.cam1.read()
        ret2, frame2 = tracker.cam2.read()

        if not ret0 or not ret1 or not ret2:
            break

        # Reduce frame size by 50%
        frame0 = cv2.resize(frame0, (0, 0), fx=0.5, fy=0.5)
        frame1 = cv2.resize(frame1, (0, 0), fx=0.5, fy=0.5)
        frame2 = cv2.resize(frame2, (0, 0), fx=0.5, fy=0.5)

        frame0 = tracker.standardize_frame(frame0)
        frame1 = tracker.standardize_frame(frame1)
        frame2 = tracker.standardize_frame(frame2)

        frame0, detected_tools_field = tracker.detect_tools(frame0)
        frame1, detected_tools_discard = tracker.detect_tools(frame1)

        if not hasattr(tracker, 'tool_counts_initialized'):
            tracker.initialize_tool_counts(frame0)
            tracker.tool_counts_initialized = True


        tracker.update_tool_counts(detected_tools_field, detected_tools_discard)
        frame2 = tracker.display_tool_counts(frame2)

        log_display = tracker.create_log_display()

        top_row = np.hstack((frame0, frame1))
        bottom_row = np.hstack((frame2, log_display))
        combined_frame = np.vstack((top_row, bottom_row))

        # Reduce the final combined frame size by 50%
        combined_frame = cv2.resize(combined_frame, (0, 0), fx=0.5, fy=0.5)

        ret, buffer = cv2.imencode('.jpg', combined_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/logs')
def get_logs():
    logs = list(tracker.log_entries) 
    return jsonify(logs)

@app.route('/tool_counts')
def get_tool_counts():
    return jsonify(tracker.tool_counts)

@app.route('/latest_log')
def get_latest_log():
    log_dir = 'backend/log'
    files = os.listdir(log_dir)
    if not files:
        return jsonify({'status': 'No log files available'}), 404

    # Get the latest log file
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(log_dir, f)))
    log_file_path = os.path.join(log_dir, latest_file)

    return send_from_directory(log_dir, latest_file, as_attachment=True)


@app.route('/reinitialize_tool_counts', methods=['POST'])
def reinitialize_tool_counts():
    if tracker.cam0.isOpened():  # Ensure the camera is open and working
        ret0, frame0 = tracker.cam0.read()
        if ret0:
            tracker.initialize_tool_counts(frame0)  # Reinitialize tool counts
            return jsonify({'status': 'Tool counts reinitialized successfully'}), 200
    return jsonify({'status': 'Failed to reinitialize tool counts'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)