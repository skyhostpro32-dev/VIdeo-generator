import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Text to Image Generator",
    layout="centered"
)

# ---------------- UI DESIGN ----------------

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
    background:linear-gradient(90deg, #22c55e, #06b6d4);
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

st.title("🎨 AI Text → Image Generator")
st.write("Turn your prompt into a real AI image instantly")

# ---------------- INPUT ----------------

prompt = st.text_area("Enter your prompt", height=150)

# ---------------- IMAGE GENERATION FUNCTION ----------------

def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{prompt}"

    try:
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error("Failed to generate image. Try again.")
            return None

    except Exception as e:
        st.error(f"Error: {e}")
        return None

# ---------------- GENERATE BUTTON ----------------

if st.button("🚀 Generate Image"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt")

    else:
        with st.spinner("Generating AI image..."):

            image = generate_image(prompt)

            if image:
                st.success("✅ Image Generated Successfully!")
                st.image(image, use_container_width=True)

                # ---------------- DOWNLOAD ----------------
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    "⬇ Download Image",
                    data=byte_im,
                    file_name="ai_image.png",
                    mime="image/png"
                )
