import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import streamlit as st
from api_rewriter import rewrite_text
from api_tts import text_to_speech
from datetime import datetime
import json

# Ensure narrations folder exists
os.makedirs("narrations", exist_ok=True)


# ---------- Setup ----------
st.set_page_config(page_title="🎿 EchoVerse – AI Audiobook Creator", layout="wide")

if "past_narrations" not in st.session_state:
    st.session_state.past_narrations = []

# ---------- Custom Styles ----------
st.markdown("""
    <style>
    .sidebar-title {
        font-size: 26px;
        font-weight: bold;
        color: #00bcd4;
    }
    .sidebar-section {
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #00bcd4;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #008c9e;
    }
    .stTextArea label, .stTextInput label, .stRadio label, .stFileUploader label {
        color: #003366 !important;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown { color: #1c1c1c !important; }
    .download-btn-style button {
        background-color: #00acc1 !important;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .highlighted-word {
        background-color: yellow;
        font-weight: bold;
        animation: pulse 1s ease-in-out infinite alternate;
    }
    @keyframes pulse {
        from { background-color: #ffeb3b; }
        to { background-color: #ffc107; }
    }
    .audio-container {
        position: relative;
    }
    .themed-container {
        background: #f9f9f9;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎿 EchoVerse</div>", unsafe_allow_html=True)
    st.markdown("Welcome to your personal audiobook studio!")
    theme_choice = st.selectbox("🎨 Choose Theme", ["Default", "Pastel", "Cyberpunk", "Forest"])
    st.markdown("---")
    st.markdown("<div class='sidebar-section'><h5>📜 Past Narrations</h5></div>", unsafe_allow_html=True)
    for narration in st.session_state.past_narrations:
        st.markdown(f"🔊 *{narration['title']}*")

# ---------- Title ----------
st.markdown("""
    <h1>🎿 EchoVerse – AI Audiobook Creator</h1>
    <p style='color:#5D6D7E;'>Craft expressive audiobooks using AI tone, voice, and language</p>
""", unsafe_allow_html=True)

# ---------- Input Method ----------
st.subheader("📝 Input Section")
input_method = st.radio("Choose Input Method", ["Type/Paste Text", "Upload .txt File"], horizontal=True)

input_text = ""
if input_method == "Type/Paste Text":
    input_text = st.text_area("Enter Original Text", height=300, key="input_area")
elif input_method == "Upload .txt File":
    uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
    if uploaded_file is not None:
        input_text = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", input_text, height=300, key="file_area")

# ---------- Tone Selector ----------
st.subheader("🎭 Tone & Voice Settings")
tone = st.selectbox("Choose a Tone", ["Inspiring", "Suspenseful", "Neutral", "Romantic", "Dramatic", "Comedic", "Empathetic", "Narrative"])
voice = st.selectbox("Choose a Voice", ["Lisa (Female)", "Martin (Male)", "Sofia (Female)", "Ethan (Male)"])
language = st.selectbox("Choose a Language", ["English", "Spanish", "French", "German"])

# ---------- Rewrite & Audio Generation ----------
if st.button("✨ Rewrite and Generate Audio") and input_text:
    with st.spinner("Loading AI model... This may take a few minutes on first run"):
        with st.spinner("Rewriting using AI..."):
            rewritten = rewrite_text(input_text).strip()
            lines = rewritten.splitlines()
            filtered = [line for line in lines if not any(line.lower().startswith(k) for k in ["input:", "question:", "answer:", "response:", "--"])]
            rewritten = "\n".join(filtered).strip()

            st.session_state.latest_original = input_text
            st.session_state.latest_rewritten = rewritten

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Original Text")
        st.text_area("Original", st.session_state.latest_original, height=300, disabled=True, key="final_original")
    with col2:
        st.markdown("#### Rewritten Text")
        st.text_area("Rewritten", st.session_state.latest_rewritten, height=300, disabled=True, key="final_rewritten")

    with st.spinner("Generating Audio..."):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        title = st.text_input("Give this narration a title", f"Inspiring_Story_{timestamp}")
        result = text_to_speech(st.session_state.latest_rewritten, f"{title}.mp3", voice=voice, language=language)

        if isinstance(result, tuple):
            audio_path, subtitle_path = result
        else:
            audio_path = result
            subtitle_path = None

        st.toast("✅ Audio generated successfully! Scroll down to view or download it.", icon="🔊")
        st.audio(audio_path, format="audio/mp3")

        with open(audio_path, "rb") as audio_file:
            st.download_button("📥 Download MP3", file_name=f"{title}.mp3", data=audio_file.read(), mime="audio/mp3")

        if subtitle_path and os.path.exists(subtitle_path):
            with open(subtitle_path, "r") as f:
                subtitles = json.load(f)
            st.markdown("### ⏱ Word-by-word subtitles")
            st.json(subtitles)

        st.session_state.past_narrations.insert(0, {
            "title": title,
            "text": st.session_state.latest_original,
            "rewritten": st.session_state.latest_rewritten,
            "tone": tone,
            "voice": voice,
            "language": language,
            "audio": audio_path,
            "timestamp": timestamp
        })

# ---------- Past Narrations Section ----------
st.subheader("📚 Full Narration History")
for narration in st.session_state.past_narrations:
    with st.expander(f"🔊 {narration['title']} ({narration['tone']}, {narration['voice']}, {narration['language']})"):
        st.markdown(f"*Original Text:* {narration['text']}")
        st.markdown(f"*Rewritten Text:* {narration['rewritten']}")
        st.audio(narration["audio"], format="audio/mp3")
        with open(narration['audio'], "rb") as audio_file:
            st.download_button(label="Download", file_name=f"{narration['title']}.mp3", data=audio_file.read(), mime="audio/mp3")

# ---------- Emoji Feedback ----------
st.markdown("---")
st.markdown("## ❤ Did you enjoy the last narration?")
st.markdown("React below:")
colA, colB, colC = st.columns(3)
colA.button("😍 Love it!")
colB.button("👍 Nice!")
colC.button("🤔 Needs work")
