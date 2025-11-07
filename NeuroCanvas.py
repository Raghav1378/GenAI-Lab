import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import io
import os
from dotenv import load_dotenv
import time

load_dotenv()

st.set_page_config(
    page_title="🎨 AI Image Generator",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1f1f1f, #121212);
            color: #fafafa;
        }
        .main-title {
            text-align: center;
            font-size: 2.5rem !important;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: -webkit-linear-gradient(45deg, #ff6ec4, #7873f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #c7c7c7;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }
        .image-card {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(255,255,255,0.1);
        }
        .spinner-text {
            font-style: italic;
            color: #ccc;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Image Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Qwen-Image-Lightning ⚡</div>', unsafe_allow_html=True)

st.sidebar.header("⚙️ Advanced Settings")

# Added unique keys here
style_preset = st.sidebar.selectbox(
    "🎨 Style Preset",
    ["Default", "Realistic", "Cartoon", "Cyberpunk", "Fantasy", "Studio Portrait"],
    key="style_preset"
)

size = st.sidebar.selectbox(
    "🖼️ Image Size",
    ["512x512", "768x768", "1024x1024"],
    key="image_size"
)

if "generated_images" not in st.session_state:
    st.session_state.generated_images = []

if st.sidebar.button("🗑️ Clear History", key="clear_history"):
    st.session_state.generated_images = []
    st.sidebar.success("History cleared!")

prompt = st.text_area(
    "🧠 Enter your image description:",
    placeholder="e.g. Astronaut riding a horse on Mars",
    height=100,
    key="prompt_input"
)

generate_button = st.button("🚀 Generate Image", key="generate_button")

if generate_button:
    if not prompt.strip():
        st.warning("⚠️ Please enter a description first.")
    elif not os.environ.get("HF_TOKEN"):
        st.error("🚨 Missing API key. Add your HF_TOKEN in the .env file.")
    else:
        with st.spinner("🎨 Creating your masterpiece..."):
            try:
                messages = [
                    "Summoning AI muses...",
                    "Blending light and imagination...",
                    "Painting pixels with quantum precision...",
                    "Almost there... adding final touches..."
                ]
                for msg in messages:
                    st.markdown(f"<p class='spinner-text'>{msg}</p>", unsafe_allow_html=True)
                    time.sleep(0.8)

                client = InferenceClient(
                    provider="fal-ai",
                    api_key=os.environ.get("HF_TOKEN")
                )

                full_prompt = f"{prompt}, style: {style_preset}, size: {size}"
                image = client.text_to_image(
                    full_prompt,
                    model="lightx2v/Qwen-Image-Lightning"
                )

                st.session_state.generated_images.append((prompt, image))

                st.markdown("### 🌟 Your Generated Image:")
                st.image(image, caption=f"Prompt: {prompt}", use_column_width=True)

                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button(
                    label="💾 Download Image",
                    data=buf.getvalue(),
                    file_name="generated_image.png",
                    mime="image/png",
                    key="download_button"
                )

            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")

if st.session_state.generated_images:
    st.markdown("---")
    st.markdown("## 🖼️ Recent Generations")
    cols = st.columns(2)
    for i, (desc, img) in enumerate(reversed(st.session_state.generated_images[-4:])):
        with cols[i % 2]:
            st.image(img, caption=f"{desc[:50]}...", use_column_width=True)
