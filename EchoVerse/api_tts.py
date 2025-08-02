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

    # Create narrations folder if not exists
    os.makedirs("narrations", exist_ok=True)

    # Run the async TTS
    asyncio.run(generate_tts(text, voice_id, output_path))

    return output_path

# # api_tts.py

# import edge_tts
# import asyncio

# # Mapping of display names to actual Edge TTS voice names
# VOICE_MAP = {
#     "Lisa (Female)": "en-US-JennyNeural",
#     "Martin (Male)": "en-US-GuyNeural",
#     "Sofia (Female)": "es-ES-ElviraNeural",
#     "Ethan (Male)": "en-AU-WilliamNeural",
#     "Ravi (Male)": "hi-IN-MadhurNeural",
#     "Priya (Female)": "hi-IN-SwaraNeural",
# }

# LANGUAGE_HINTS = {
#     "English": "en-US",
#     "Hindi": "hi-IN",
#     "Telugu": "te-IN",
#     "Spanish": "es-ES",
#     "French": "fr-FR",
#     "German": "de-DE",
# }

# async def generate_tts(text, voice, filename):
#     communicate = edge_tts.Communicate(text=text, voice=voice)
#     await communicate.save(filename)

# def text_to_speech(text, filename="output.mp3", voice="Lisa (Female)", language="English"):
#     voice_id = VOICE_MAP.get(voice, "en-US-JennyNeural")  # fallback to Lisa
#     output_path = f"narrations/{filename}"  # Save to folder
#     asyncio.run(generate_tts(text, voice_id, output_path))
#     return output_path

# # import pyttsx3

# # def text_to_speech(text, filename="output.wav", voice="Lisa (Female)", language="English"):
# #     engine = pyttsx3.init()
    
# #     voices = engine.getProperty("voices")
    
# #     # Voice selection based on label
# #     selected_voice = None
# #     for v in voices:
# #         # Match based on label or fallback to gender/lang keyword
# #         if voice.lower().split()[0] in v.name.lower() or voice.lower().split()[0] in v.id.lower():
# #             selected_voice = v.id
# #             break
# #     if selected_voice:
# #         engine.setProperty('voice', selected_voice)
    
# #     # Optional language-based rate control
# #     if language.lower() == "english":
# #         engine.setProperty('rate', 180)
# #     elif language.lower() == "hindi":
# #         engine.setProperty('rate', 150)
# #     else:
# #         engine.setProperty('rate', 170)

# #     engine.save_to_file(text, filename)
# #     engine.runAndWait()
# #     return filename
