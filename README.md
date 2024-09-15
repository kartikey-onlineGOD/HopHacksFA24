# HopHacks Fall 2024 Project

**Author:** Kartikey Pandey  
**Date:** September 2024

## Project Overview

This project, developed during the **HopHacks Fall 2024 Hackathon**, is a tool tracking system designed to enhance operational safety in surgical environments. The project focuses on real-time monitoring of surgical tools using computer vision techniques, ensuring accurate accounting of tools in use, discarded, and returned to the tool tray.

## Key Features

- **Real-time Tool Tracking:** Leverages camera feeds and object detection algorithms to track the movement of surgical tools.
- **Live Monitoring:** Provides a user-friendly interface that displays the current state of tools, including tools in the field, tools in use, and discarded tools.
- **Logging and Reporting:** Logs the activities of tools, offering a detailed view of tool usage over time, aiding in post-operation analysis.
- **Frontend-Backend Integration:** The application uses a `React` frontend and `Flask` backend for smooth interaction and real-time updates.
- **Downloadable Logs:** Offers functionality to download log files for further analysis.

## Technologies Used

- **Frontend:** React.js, Tailwind CSS
- **Backend:** Flask (Python), OpenCV for image processing
- **Database:** SQLite for log storage
- **Deployment:** Docker for containerization

## How It Works

The tool tracking system captures video input from a camera and identifies tools using object detection algorithms. Each tool is marked with distinct neon-colored tape, which the system recognizes to determine whether a tool is in use, discarded, or returned. The data is processed on the backend and the live status of tools is displayed on the frontend.

## Future Enhancements

- **Enhanced Accuracy:** Improve tool recognition and tracking by integrating machine learning models such as YOLO.
- **Scalability:** Extend the system to track a larger variety of tools across multiple operating rooms.
- **Data Analysis:** Provide deeper analytics on tool usage trends for surgical teams.

## Conclusion

This project serves as a vital tool to improve surgical safety by ensuring all instruments are accounted for during operations. With real-time monitoring and accurate logging, the system reduces the risk of human error, making surgeries safer and more efficient.

**Repository:** [GitHub - HopHacks Fall 2024](https://github.com/kartikey-onlineGOD/HopHacksFA24)
