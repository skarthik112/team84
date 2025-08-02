import streamlit as st
from api_rewriter import rewrite_text
from api_tts import text_to_speech
import os
from datetime import datetime

# ---------- Setup ----------
st.set_page_config(page_title="EchoVerse – AI Audiobook Creator", layout="wide")

if "past_narrations" not in st.session_state:
    st.session_state.past_narrations = []

# ---------- Theme Logic ----------
def apply_theme(theme_name):
    if theme_name == "Glass":
        return """<style>
            html, body, .stApp {
                background: linear-gradient(135deg, #f0f0f0, #d0d0d0);
                font-family: 'Segoe UI', sans-serif;
            }
            .block-container {
                background: rgba(255, 255, 255, 0.25);
                backdrop-filter: blur(12px);
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            }
            .stTextArea textarea, .stTextInput input {
                background: rgba(255, 255, 255, 0.2) !important;
                color: #000 !important;
                border: none;
                border-radius: 12px;
                font-weight: 500;
            }
            .stButton > button {
                background: rgba(255, 255, 255, 0.25) !important;
                color: #000;
                border-radius: 10px;
                font-weight: bold;
            }
        </style>"""

    elif theme_name == "Pastel":
        return """<style>
            html, body, .stApp { background-color: #fffafc; }
            .stButton>button { background-color: #ffc1e3 !important; color: #4b0082; }
            .stTextArea textarea, .stTextInput input {
                background-color: #fff0f5 !important;
                color: #4b0082 !important;
            }
        </style>"""

    elif theme_name == "Sunlight":
        return """<style>
            html, body, .stApp { background-color: #fffbea; }
            .stButton>button { background-color: #ffe299 !important; color: #3e2723; }
            .stTextArea textarea, .stTextInput input {
                background-color: #fff8dc !important;
                color: #3e2723 !important;
            }
        </style>"""

    elif theme_name == "Forest":
        return """<style>
            html, body, .stApp { background-color: #e8f5e9; }
            .stButton>button { background-color: #4caf50 !important; color: white; }
            .stTextArea textarea, .stTextInput input {
                background-color: #dcedc8 !important;
                color: #2e7d32 !important;
            }
        </style>"""

    return ""

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("<h2>EchoVerse</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size: 0.9rem; color: #333;'>
            Create expressive, AI-generated audiobooks from any text with voice, tone, and language customization.
        </p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    theme_choice = st.selectbox("Theme", ["Default", "Glass", "Pastel", "Sunlight", "Forest"], key="theme_choice")

    # Narration History
    if st.session_state.past_narrations:
        st.markdown("### 📖 History")
        for item in st.session_state.past_narrations:
            st.markdown(f"- {item['title']} ({item.get('tone', 'N/A')}, {item.get('voice', 'N/A')}, {item.get('language', 'N/A')})")

# ---------- Apply Theme ----------
st.markdown(apply_theme(st.session_state.theme_choice), unsafe_allow_html=True)

# ---------- App Title ----------
st.markdown("""
<h1 style='text-align: center;'>EchoVerse – AI Audiobook Creator</h1>
<p style='text-align: center; color: #5D6D7E;'>Transform your text into engaging audio stories with customized tone and voice.</p>
""", unsafe_allow_html=True)

# ---------- Input Section ----------
st.subheader("📝 Narration Setup")

input_method = st.radio("Input Method", ["Type Text", "Upload .txt File"], horizontal=True)
input_text = ""
if input_method == "Type Text":
    input_text = st.text_area("Enter your text", height=200)
else:
    uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
    if uploaded_file:
        input_text = uploaded_file.read().decode("utf-8")
        st.text_area("File Preview", input_text, height=200, disabled=True)

st.markdown("### 🎭 Tone, Voice & Language")
tone = st.selectbox("Select Tone", ["Inspiring", "Suspenseful", "Dramatic", "Comedic", "Neutral"])
voice = st.selectbox("Select Voice", ["Lisa (Female)", "Martin (Male)", "Sofia (Female)", "Ethan (Male)"])
language = st.selectbox("Select Language", ["English", "Spanish", "French", "German"])

# ---------- Rewrite and Audio Generation ----------
if st.button("✨ Rewrite and Generate Audio") and input_text:
    with st.spinner("Rewriting the text..."):
        rewritten_text = rewrite_text(input_text)

    # Title and file-safe name
    title = f"{tone} Story – {datetime.now().strftime('%b %d, %H-%M')}"
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    audio_file = f"{safe_title}.mp3"

    with st.spinner("Generating Audio..."):
        audio_path = text_to_speech(rewritten_text, filename=audio_file, voice=voice, language=language)

    # Save to history
    st.session_state.past_narrations.insert(0, {
        "title": title,
        "text": input_text,
        "rewritten": rewritten_text,
        "audio": f"narrations/{audio_file}",
        "tone": tone,
        "voice": voice,
        "language": language
    })

    # Show output side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📝 Original Text")
        st.text_area("Original", input_text, height=250, disabled=True)
    with col2:
        st.markdown("### ✍ Rewritten Text")
        st.text_area("Rewritten", rewritten_text, height=250, disabled=True)

    st.audio(f"narrations/{audio_file}")
    with open(f"narrations/{audio_file}", "rb") as audio_bin:
        st.download_button("🔽 Download Audio", audio_bin.read(), file_name=audio_file, mime="audio/mpeg")

    st.download_button("📜 Download Rewritten Text", rewritten_text, file_name=f"{safe_title}.txt")

# ---------- Past Narrations ----------
if st.session_state.past_narrations:
    st.markdown("## 📚 Past Narrations")
    to_delete = None
    for i, narration in enumerate(st.session_state.past_narrations):
        with st.expander(f"🎰 {narration['title']}", expanded=False):
            st.markdown(f"*Tone:* {narration.get('tone', 'N/A')} | *Voice:* {narration.get('voice', 'N/A')} | *Language:* {narration.get('language', 'N/A')}")

            st.audio(narration["audio"])

            if os.path.exists(narration["audio"]):
                with open(narration["audio"], "rb") as audio_file:
                    st.download_button("🔽 Download Audio", audio_file.read(), file_name=os.path.basename(narration["audio"]), mime="audio/mpeg", key=f"download_audio_{i}")

            st.download_button("📜 Download Rewritten Text", narration["rewritten"], file_name=f"{narration['title']}.txt", key=f"download_txt_{i}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📝 Original Text")
                st.text_area("Original", narration["text"], height=200, disabled=True, key=f"orig_{i}")
            with col2:
                st.markdown("#### ✍ Rewritten Text")
                st.text_area("Rewritten", narration["rewritten"], height=200, disabled=True, key=f"rew_{i}")

            if st.button(f"🗑 Delete Narration", key=f"delete_{i}"):
                to_delete = i

    if to_delete is not None:
        deleted = st.session_state.past_narrations.pop(to_delete)
        if os.path.exists(deleted["audio"]):
            os.remove(deleted["audio"])
        st.success(f"Deleted: {deleted['title']}")
        st.rerun()
