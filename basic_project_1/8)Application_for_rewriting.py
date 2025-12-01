import streamlit as st
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from google import genai
import os
from docx import Document
import requests
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4

load_dotenv()

# =================================================================
# 🔥 UNICODE PDF GENERATOR (REPORTLAB — 100% SAFE)
# =================================================================
def generate_pdf_unicode(text):
    font_path = "NotoSans-Regular.ttf"
    font_url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"

    # Download font once
    if not os.path.exists(font_path):
        r = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(r.content)

    pdf_path = "rewritten.pdf"

    pdfmetrics.registerFont(TTFont("NotoSans", font_path))
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("NotoSans", 12)

    width, height = A4
    y = height - 50

    for line in text.split("\n"):
        if y < 50:  # auto new page
            c.showPage()
            c.setFont("NotoSans", 12)
            y = height - 50

        c.drawString(40, y, line)
        y -= 18

    c.save()
    return pdf_path


# =================================================================
# STREAMLIT PAGE CONFIG
# =================================================================
st.set_page_config(
    page_title="Re-write your text",
    page_icon="✍️",
    layout="centered"
)

# =================================================================
# CSS UI
# =================================================================
st.markdown("""
<style>

html, body { font-family: 'Inter', sans-serif; }

.main { padding-top: 0 !important; }

.main-header {
    text-align: center;
    padding: 0 0 1rem 0;
    font-size: 2.4rem;
    background: linear-gradient(90deg, #7F00FF, #E100FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section-card {
    background: rgba(255,255,255,0.08);
    padding: 1rem 1.2rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
}

textarea, input, select {
    border-radius: 10px !important;
}

.stButton>button {
    background: linear-gradient(90deg, #6A5ACD, #836FFF);
    color: white;
    padding: .7rem;
    border-radius: 10px;
    width: 100%;
    font-size: 1.1rem;
    border: none;
    transition: 0.2s;
}

.stButton>button:hover { transform: scale(1.03); }

.result-box, .comparison-box {
    background: #181818;
    padding: 1.3rem;
    border-radius: 12px;
    border: 1px solid #333;
}

</style>
""", unsafe_allow_html=True)

# =================================================================
# HEADER
# =================================================================
st.markdown("<div class='main-header'>✨ Re-write Your Text with Gemini ✍️</div>", unsafe_allow_html=True)

# =================================================================
# PROMPT TEMPLATE
# =================================================================
template = """
You are an advanced rewriting model.

Rewrite the text with the following requirements:

Mode: {mode}
Tone: {tone}
Dialect: {dialect}
Writing Style: {style}
Emotion/Flavor: {emotion}
Rewrite Strength: {strength}%
Output Language: {language}

Start with a warm introduction.
Preserve meaning unless the mode requires otherwise.

TEXT:
{draft}

YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft", "style", "emotion", "strength", "mode", "language"],
    template=template,
)

# =================================================================
# GEMINI CLIENT
# =================================================================
def load_LLM(api_key):
    return genai.Client(api_key=api_key)

# =================================================================
# HISTORY
# =================================================================
if "history" not in st.session_state:
    st.session_state.history = []


# =================================================================
# INPUT UI
# =================================================================

# API Key
with st.container():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("🔑 Gemini API Key")
    google_api_key = st.text_input("API Key", type="password", placeholder="Enter your Gemini API key")
    st.markdown("</div>", unsafe_allow_html=True)

# Text
with st.container():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("📝 Text to Rewrite")
    draft_input = st.text_area("Your Text", placeholder="Type or paste text...", height=150)
    if draft_input:
        st.caption(f"Words: {len(draft_input.split())} | Characters: {len(draft_input)}")
    st.markdown("</div>", unsafe_allow_html=True)

# Options
with st.container():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        option_tone = st.selectbox("Tone", ("Formal", "Informal"))
        style = st.selectbox("Writing Style", ["Default", "Poetic", "Professional", "Humorous", "Storytelling", "Academic"])
        emotion = st.selectbox("Emotion Flavor", ["None", "Romantic", "Motivational", "Sarcastic", "Emotional"])

    with col2:
        option_dialect = st.selectbox("Dialect", ("American", "British", "Hindi"))
        mode = st.selectbox("Mode", ["Rewrite", "Summarize", "Expand", "Paraphrase", "Simplify"])
        language = st.selectbox("Output Language", ["English", "Hindi", "Spanish", "Japanese", "French"])

    strength = st.slider("Rewrite Strength", 0, 100, 70)

    st.markdown("</div>", unsafe_allow_html=True)


# =================================================================
# GENERATE BUTTON
# =================================================================
if st.button("Rewrite Text ✨"):

    if not google_api_key:
        st.warning("Please enter your Gemini API Key!")
        st.stop()

    if not draft_input.strip():
        st.warning("Please enter text to rewrite!")
        st.stop()

    client = load_LLM(google_api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt.format(
            tone=option_tone,
            dialect=option_dialect,
            style=style,
            emotion=emotion,
            strength=strength,
            draft=draft_input,
            mode=mode,
            language=language
        )
    )

    rewritten_text = response.text
    st.session_state.history.append(rewritten_text)

    # Comparison
    st.subheader("📊 Side-by-Side Comparison")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Original**")
        st.markdown(f"<div class='comparison-box'>{draft_input}</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("**Rewritten**")
        st.markdown(f"<div class='comparison-box'>{rewritten_text}</div>", unsafe_allow_html=True)

    st.subheader("🔮 Final Rewritten Text")
    st.markdown(f"<div class='result-box'>{rewritten_text}</div>", unsafe_allow_html=True)

    # Downloads
    st.download_button("⬇️ Download as TXT", rewritten_text, file_name="rewritten.txt")

    doc = Document()
    doc.add_paragraph(rewritten_text)
    doc.save("rewritten.docx")
    st.download_button("⬇️ Download as DOCX", open("rewritten.docx", "rb"), file_name="rewritten.docx")

    pdf_path = generate_pdf_unicode(rewritten_text)
    st.download_button("⬇️ Download as PDF (Unicode)", open(pdf_path, "rb"), file_name="rewritten.pdf")


# =================================================================
# HISTORY
# =================================================================
if st.session_state.history:
    st.subheader("📜 Rewrite History")
    for i, txt in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"Version {len(st.session_state.history)-i}"):
            st.write(txt)
