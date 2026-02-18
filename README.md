SCAS – Smart Crowd Alert System

An AI-powered real-time crowd monitoring and alert web application that detects people and objects using YOLOv8 and classifies crowd conditions based on configurable space limits.
 Overview

SCAS (Smart Crowd Alert System) is designed to transform traditional passive CCTV monitoring into an intelligent, decision-based crowd safety system.

The system:

Detects and counts people in real time
Detects surrounding objects
Allows dynamic crowd capacity setting
Classifies crowd condition into safety levels
Provides live webcam monitoring
Supports drag-and-drop video upload
Triggers alert when crowd exceeds threshold

SCAS aims to improve safety in crowded environments by enabling proactive monitoring instead of reactive response.
 Problem Statement

Crowd management in public spaces such as festivals, railway stations, stadiums, and educational institutions often relies on manual supervision or simple people-counting systems. These systems lack real-time intelligence, dynamic threshold configuration, and automated alerts, leading to delayed action during overcrowding situations.

SCAS addresses this gap by combining AI-based object detection with an intelligent decision engine to provide actionable crowd safety insights.

Tech Stack

Frontend

streamlite
HTML
CSS
JavaScript

Backend

Python
Flask

AI Model
YOLOv8 by Ultralytics

Libraries
OpenCV
Ultralytics

Streamlite Cloud(for deployment)

Features

🔹 Choose between Webcam or Upload Video

🔹 Drag-and-drop video upload

🔹 Real-time person detection

🔹 Object detection

🔹 Configurable crowd limit

🔹 Multi-level crowd classification

🔹 Automatic siren alert when limit exceeded

🔹 Interactive web interface

🔹 Real-time bounding box visualization

How It Works

User selects:

Webcam Mode OR
Video Upload Mode
User sets crowd capacity limit

YOLOv8 model detects:
People
Objects
Decision Engine classifies status based on limit

If limit is exceeded:

Alert displayed
Siren activated
  

 Use Cases
 
College festivals
Railway stations
Airports
Political rallies
Religious gatherings
Smart city monitoring
Stadium management

Future Improvements

1.SMS alert integration
2.Heatmap-based density visualization
3.Predictive crowd growth analytics
4.Database logging and analytics dashboard
5.Edge AI deployment

 Architecture
Frontend (HTML/CSS/JS)
        ↓
Flask Backend
        ↓
YOLOv8 AI Model
        ↓
Crowd Decision Engine
        ↓
Alert System


SCAS is designed as an intelligent, scalable, and customizable crowd monitoring solution that shifts from simple surveillance to proactive crowd safety management.

It demonstrates the integration of AI, web technologies, and real-time decision-making to solve real-world safety problems.
