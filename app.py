import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import tempfile
import cv2
import numpy as np
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="AI Text to Video", layout="centered")

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color:white;
}

h1{
    text-align:center;
    color:#38bdf8;
    font-size:3rem !important;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg, #f97316, #ef4444);
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:18px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🎬 AI Text → Video Generator")
st.write("Creates simple AI-style videos from your prompt")

# ---------------- INPUT ----------------

prompt = st.text_area("Enter Video Prompt", height=150)
duration = st.slider("Video Length (seconds)", 3, 10, 5)

# ---------------- FRAME GENERATOR ----------------

def generate_frame(prompt, i):
    url = f"https://image.pollinations.ai/prompt/{prompt} scene {i}"
    response = requests.get(url, timeout=60)
    image = Image.open(BytesIO(response.content))
    return image

# ---------------- VIDEO CREATION ----------------

def create_video(prompt, duration):

    temp_dir = tempfile.mkdtemp()
    frames = []

    for i in range(duration):
        img = generate_frame(prompt, i)

        frame_path = os.path.join(temp_dir, f"frame_{i}.png")
        img.save(frame_path)

        frames.append(frame_path)

    # read first frame for size
    frame = cv2.imread(frames[0])
    height, width, layers = frame.shape

    video_path = os.path.join(temp_dir, "output.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_path, fourcc, 1, (width, height))

    for frame_path in frames:
        img = cv2.imread(frame_path)
        video.write(img)

    video.release()

    return video_path

# ---------------- BUTTON ----------------

if st.button("🚀 Generate Video"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt")

    else:
        with st.spinner("Creating AI video..."):

            video_path = create_video(prompt, duration)

            st.success("✅ Video Generated Successfully!")

            st.video(video_path)

            with open(video_path, "rb") as f:
                st.download_button(
                    "⬇ Download Video",
                    data=f,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
