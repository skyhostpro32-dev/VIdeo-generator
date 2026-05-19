import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import tempfile
import os
import textwrap
import random

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Local AI Video Generator",
    layout="centered"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
    color:white;
}

h1{
    text-align:center;
    color:#38bdf8;
    font-size:3rem !important;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#06b6d4,#3b82f6);
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

st.title("🎬 Local AI Text → Video Generator")

st.write("Generate animated videos without any API")

# ---------------- INPUT ----------------

prompt = st.text_area(
    "Enter Video Text",
    height=150
)

duration = st.slider(
    "Video Duration",
    3,
    10,
    5
)

# ---------------- VIDEO FUNCTION ----------------

def create_video(prompt, duration):

    width = 1280
    height = 720
    fps = 24

    total_frames = duration * fps

    temp_dir = tempfile.mkdtemp()

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

    wrapped_text = textwrap.fill(
        prompt,
        width=30
    )

    try:
        font = ImageFont.truetype(
            "arial.ttf",
            50
        )
    except:
        font = ImageFont.load_default()

    # ---------------- FRAMES ----------------

    for frame_num in range(total_frames):

        # gradient background
        image = Image.new(
            "RGB",
            (width, height),
            (15, 23, 42)
        )

        draw = ImageDraw.Draw(image)

        for y in range(height):

            r = int(15 + y * 0.03)
            g = int(23 + y * 0.02)
            b = int(42 + y * 0.05)

            draw.line(
                [(0, y), (width, y)],
                fill=(r, g, b)
            )

        # ---------------- ANIMATION ----------------

        x = 80 + int(
            np.sin(frame_num * 0.05) * 40
        )

        y = 250 + int(
            np.cos(frame_num * 0.03) * 20
        )

        # glow effect
        draw.text(
            (x+3, y+3),
            wrapped_text,
            font=font,
            fill=(0,0,0)
        )

        # main text
        draw.text(
            (x, y),
            wrapped_text,
            font=font,
            fill=(255,255,255)
        )

        # convert PIL → OpenCV
        frame = cv2.cvtColor(
            np.array(image),
            cv2.COLOR_RGB2BGR
        )

        video.write(frame)

    video.release()

    return video_path

# ---------------- BUTTON ----------------

if st.button("🚀 Generate Video"):

    if prompt.strip() == "":
        st.warning("Please enter text")

    else:

        with st.spinner("Generating video..."):

            video_path = create_video(
                prompt,
                duration
            )

            st.success(
                "✅ Video Generated Successfully!"
            )

            st.video(video_path)

            with open(video_path, "rb") as file:

                st.download_button(
                    "⬇ Download Video",
                    data=file,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
