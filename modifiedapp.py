import streamlit as st
import cv2
from ultralytics import YOLO
import sqlite3
import datetime
import tempfile
import os
import time

# --- CLOUD OPTIMIZATIONS (1GB RAM LIMIT) ---
SKIP_FRAMES = 3          # Process every 3rd frame (User requested)
INFERENCE_SIZE = 320     # Lower YOLO inference resolution (User requested)
DISPLAY_SIZE = (640, 360) # Target display/process resolution (User requested)
ALERT_COOLDOWN = 2       # Prevent spamming alerts

# Database setup
conn = sqlite3.connect('crowd_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS alerts (timestamp TEXT, count INTEGER, status TEXT)')
conn.commit()

# Session State for efficient tracking
if 'frame_count' not in st.session_state:
    st.session_state.frame_count = 0
if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0
if 'last_status' not in st.session_state:
    st.session_state.last_status = "NORMAL"

st.set_page_config(page_title="AI Crowd Guard", layout="wide")
st.title("🛡️ Smart Crowd Monitoring System")

# Alarm sound with cooldown
def play_alarm():
    current_time = time.time()
    if current_time - st.session_state.last_alert_time > ALERT_COOLDOWN:
        try:
            st_alarm.audio("alarm.mp3", autoplay=True)
            st.session_state.last_alert_time = current_time
        except:
            pass

# Sidebar
st.sidebar.header("System Controls")
mode = st.sidebar.radio("Input Source", ("Webcam", "Video File", "Log History"))
limit = st.sidebar.slider("Set Crowd Limit", 0, 50, 5)

# Placeholders
st_count = st.sidebar.empty()
st_status = st.empty()  
st_alarm = st.empty()   

# Load model ONCE
@st.cache_resource
def load_model():
    # Use the lightweight nano model
    return YOLO("yolov8n.pt")

model = load_model()

# Process frame
def process_frame(frame, st_frame):
    if frame is None:
        return

    st.session_state.frame_count += 1
    
    # Skip frames to save CPU/RAM
    if st.session_state.frame_count % SKIP_FRAMES != 0:
        # For skipped frames, display raw RGB to keep video feeling smooth
        raw_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_raw = cv2.resize(raw_rgb, DISPLAY_SIZE)
        st_frame.image(resized_raw, use_column_width=True)
        return

    # Resize frame before detection to save memory
    frame_resized = cv2.resize(frame, DISPLAY_SIZE)
    
    # Run AI with low imgsz for efficiency
    results = model(frame_resized, imgsz=INFERENCE_SIZE, verbose=False)

    person_count = 0
    if results and len(results) > 0 and results[0].boxes is not None:
        person_count = int(sum(
            1 for b in results[0].boxes.cls
            if model.names[int(b)] == 'person'
        ))

    st_count.metric("People Detected", person_count)

    if person_count > limit:
        st_status.error(f"🚨 ALERT: {person_count} People Detected! (Limit: {limit})")
        play_alarm()

        # Only log once per crowded event to save database resources
        if st.session_state.last_status == "NORMAL":
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('INSERT INTO alerts VALUES (?, ?, ?)', (now, person_count, "CROWDED"))
            conn.commit()
            st.session_state.last_status = "CROWDED"
    else:
        st_status.success(f"✅ Status: Normal ({person_count} people)")
        st_alarm.empty()
        st.session_state.last_status = "NORMAL"

    # Convert YOLO output to RGB and display
    annotated_frame = results[0].plot()
    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    st_frame.image(annotated_frame, use_column_width=True)


# Webcam mode
if mode == "Webcam":
    st.warning("Webcam may not work on cloud deployments.")
    run = st.checkbox("Start Live Stream")
    st_frame = st.empty()
    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        process_frame(frame, st_frame)
    cap.release()


# Video file mode
elif mode == "Video File":
    uploaded = st.file_uploader("Upload MP4 Video", type=['mp4'])
    if uploaded:
        # Manage file in temp storage, then release immediately
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded.read())
        cap = cv2.VideoCapture(tfile.name)
        st_frame = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            process_frame(frame, st_frame)

        cap.release()
        os.unlink(tfile.name)


# Log history
elif mode == "Log History":
    st.header("📋 System Log History")
    data = c.execute('SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 25').fetchall()
    if data:
        st.table(data)
    else:
        st.info("No logs found yet.")
