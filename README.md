# HopHacks Fall 2024 Project

**Author:** Kartikey Pandey and Manas Munjial
**Date:** September 2024

## Project Description: Multi-Spatial Tool Tracking System for Surgical Safety

### Overview
This project addresses the critical issue of surgical and procedural errors, a leading cause of patient harm in the U.S. healthcare system. Each year, medical errors harm millions of patients and result in 250,000 deaths, costing billions of dollars. Our tool-tracking system, designed specifically for operating rooms, ensures real-time monitoring of surgical tools using computer vision and data tracking.

### Problem Statement
Surgical errors often occur due to mismanagement or loss of tools during procedures, leading to retained surgical instruments or delays that can jeopardize patient safety. By tackling the problem of misplaced tools, this project aims to minimize errors that can directly contribute to patient harm.

### Solution
The tool-tracking system utilizes cameras and neon-colored markers to monitor the movement of instruments. The system provides a real-time log of tools in use, in the field, and discarded, helping to prevent errors such as instruments being left inside patients. Additionally, it allows medical staff to reinitialize tool counts at any time, further ensuring accuracy.

### Why It Matters
With technology-driven solutions, this project reduces the margin for human error in surgical environments, directly aligning with one of the five leading patient safety challenges: procedural and surgical errors. It not only enhances tool accountability but also creates a safer operating room environment, potentially saving lives and reducing costs associated with post-surgical complications.

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
