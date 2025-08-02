import edge_tts
import asyncio
import os
import time

VOICE_MAP = {
    "Lisa (Female)": "en-US-JennyNeural",
    "Martin (Male)": "en-US-GuyNeural",
    "Sofia (Female)": "es-ES-ElviraNeural",
    "Ethan (Male)": "en-AU-WilliamNeural",
}

async def generate_tts(text, voice, audio_path):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    audio_buffer = bytearray()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.extend(chunk["data"])

    with open(audio_path, "wb") as audio_file:
        audio_file.write(audio_buffer)

def text_to_speech(text, filename="output.mp3", voice="Lisa (Female)", language="English"):
    voice_id = VOICE_MAP.get(voice, "en-US-JennyNeural")
    os.makedirs("narrations", exist_ok=True)

    audio_path = os.path.join("narrations", filename)

    if os.path.exists(audio_path):
        os.remove(audio_path)

    start = time.time()
    asyncio.run(generate_tts(text, voice_id, audio_path))
    print(f"⏱ TTS Generation took {time.time() - start:.2f} seconds")

    return audio_path
