# api_tts.py

import edge_tts
import asyncio
import os

# Mapping of display names to Edge TTS voices
VOICE_MAP = {
    "Lisa (Female)": "en-US-JennyNeural",
    "Martin (Male)": "en-US-GuyNeural",
    "Sofia (Female)": "es-ES-ElviraNeural",
    "Ethan (Male)": "en-AU-WilliamNeural",
    "Ravi (Male)": "hi-IN-MadhurNeural",
    "Priya (Female)": "hi-IN-SwaraNeural",
}

# Optional for filtering language voices (for future extension)
LANGUAGE_HINTS = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
}


async def generate_tts(text, voice, filename):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(filename)


def text_to_speech(text, filename="output.mp3", voice="Lisa (Female)", language="English"):
    voice_id = VOICE_MAP.get(voice, "en-US-JennyNeural")  # fallback to Lisa
    output_path = os.path.join("narrations", filename)

    # Create narrations folder if it doesn't exist
    os.makedirs("narrations", exist_ok=True)

    # ✅ Safe async loop for Streamlit Cloud
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_tts(text, voice_id, output_path))

    return output_path
