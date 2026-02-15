import streamlit as st
import cv2
from ultralytics import YOLO

# 1. Page Setup (Shows up immediately)
st.set_page_config(page_title="Crowd Monitor", layout="wide")
st.title("🛡️ Smart Crowd Monitoring System")
st.write("Status: System Ready")

# 2. Sidebar Controls
st.sidebar.header("Settings")
source = st.sidebar.selectbox("Select Input", ("Webcam", "Video"))
# Setting a limit for the crowd alert
limit = st.sidebar.slider("Crowd Limit Alert", 1, 50, 5)
run_button = st.sidebar.button("Launch System")

# 3. Load the AI Model (Cached for speed)
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# 4. The Logic (Indentation is critical here!)
if run_button:
    st.write("AI is running... (Press 'Ctrl+C' in Terminal to stop)")
    # Initialize camera (0 is default webcam)
    cap = cv2.VideoCapture(0)
    st_frame = st.empty()  # This creates the video window

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame from camera.")
            break

        # Run YOLO detection
        results = model(frame)
        
        # Draw boxes and count people
        annotated_frame = results[0].plot()
        person_count = 0
        for r in results:
            for c in r.boxes.cls:
                if model.names[int(c)] == 'person':
                    person_count += 1
        
        # Display the Count in the sidebar
        st.sidebar.metric("Current People Count", person_count)
        
        # Show warning if limit is exceeded
        if person_count > limit:
            st.sidebar.error("⚠️ CROWD LIMIT EXCEEDED!")

        # Show the video feed on the web page
        st_frame.image(annotated_frame, channels="BGR", use_container_width=True)

    cap.release()