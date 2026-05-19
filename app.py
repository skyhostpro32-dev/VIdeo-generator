import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import tempfile
from moviepy.editor import ImageClip, concatenate_videoclips

# ---------------- PAGE ----------------

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
st.write("Create short AI videos from text prompts")

# ---------------- INPUT ----------------

prompt = st.text_area("Enter Video Prompt", height=150)

duration = st.slider("Video Duration (seconds)", 3, 10, 5)

# ---------------- FRAME GENERATION ----------------

def generate_frame(prompt, i):
    url = f"https://image.pollinations.ai/prompt/{prompt} scene {i}"

    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# ---------------- VIDEO GENERATION ----------------

def create_video(prompt, duration):

    clips = []

    for i in range(duration):

        img = generate_frame(prompt, i)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img.save(temp_file.name)

        clip = ImageClip(temp_file.name).set_duration(1)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    video.write_videofile(output, fps=24, codec="libx264", audio=False)

    return output

# ---------------- BUTTON ----------------

if st.button("🚀 Generate Video"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt")

    else:
        with st.spinner("Creating AI video..."):

            video_path = create_video(prompt, duration)

            st.success("✅ Video Generated!")

            st.video(video_path)

            with open(video_path, "rb") as f:
                st.download_button(
                    "⬇ Download Video",
                    data=f,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
