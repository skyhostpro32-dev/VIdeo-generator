import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import tempfile
import os
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Text To Video Generator",
    layout="centered"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color:white;
}

h1{
    text-align:center;
    color:#38bdf8;
    font-size:3rem !important;
}

.stButton>button{
    width:100%;
    background:linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
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

st.title("🎬 AI Text To Video Generator")

st.write("Generate AI videos from text prompts")

# ---------------- INPUT ----------------

prompt = st.text_area(
    "Enter Video Prompt",
    height=150
)

duration = st.slider(
    "Video Duration (seconds)",
    3,
    8,
    5
)

# ---------------- IMAGE GENERATION ----------------

def generate_image(prompt, frame_num):

    # different prompt for each frame
    frame_prompt = f"{prompt} cinematic scene {frame_num}"

    url = f"https://image.pollinations.ai/prompt/{frame_prompt}"

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                timeout=120
            )

            if response.status_code == 200:

                image = Image.open(
                    BytesIO(response.content)
                )

                return image

        except:
            time.sleep(2)

    # fallback image
    fallback = Image.new(
        "RGB",
        (768, 768),
        (20, 20, 20)
    )

    return fallback

# ---------------- VIDEO GENERATION ----------------

def create_video(prompt, duration):

    fps = 1

    temp_dir = tempfile.mkdtemp()

    frames = []

    # generate frames
    for i in range(duration):

        img = generate_image(prompt, i)

        frame_path = os.path.join(
            temp_dir,
            f"frame_{i}.png"
        )

        img.save(frame_path)

        frames.append(frame_path)

        time.sleep(1)

    # first frame size
    frame = cv2.imread(frames[0])

    height, width, layers = frame.shape

    video_path = os.path.join(
        temp_dir,
        "output.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video = cv2.VideoWriter(
        video_path,
        fourcc,
        fps,
        (width, height)
    )

    # write frames
    for frame_path in frames:

        img = cv2.imread(frame_path)

        video.write(img)

    video.release()

    return video_path

# ---------------- GENERATE BUTTON ----------------

if st.button("🚀 Generate Video"):

    if prompt.strip() == "":

        st.warning("Please enter prompt")

    else:

        with st.spinner("Generating AI Video..."):

            video_path = create_video(
                prompt,
                duration
            )

            st.success(
                "✅ Video Generated Successfully!"
            )

            st.video(video_path)

            # download
            with open(video_path, "rb") as file:

                st.download_button(
                    "⬇ Download Video",
                    data=file,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
