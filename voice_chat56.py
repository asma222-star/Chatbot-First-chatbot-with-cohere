import whisper
import cohere
import sounddevice as sd
import wavio
import os
from gtts import gTTS
import playsound
import time

# ========== YOUR COHERE API KEY ==========
co = cohere.Client("xxxxxxxxxxxxx") 
# ==========================================

# 🎤 Record audio from microphone
def record_voice(filename="input.wav", duration=5, fs=44100):
    print("🎤 Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    print("✅ Recording saved as", filename)

# 🧠 Transcribe audio using local Whisper
def transcribe_audio(file_path="input.wav"):
    print("📝 Transcribing with local Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    text = result["text"].strip()
    print("You said:", text)
    return text

# 🧠 Get reply from Cohere
def get_cohere_reply(prompt):
    response = co.generate(
        model="command-light",
        prompt=prompt,
        max_tokens=100
    )
    reply = response.generations[0].text.strip()
    print("🤖 Bot:", reply)
    return reply

# 🌍 Detect Arabic text
def is_arabic(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)

# 🔊 Speak text using gTTS
def speak_text(text):
    try:
        lang = 'ar' if is_arabic(text) else 'en'
        filename = f"response_{int(time.time())}.mp3"  # unique filename
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)  # delete after playing
    except Exception as e:
        print("❌ Error speaking:", e)

# 🚀 Main chatbot loop
while True:
    record_voice()
    user_input = transcribe_audio()

    if not user_input:
        print("⚠️ No speech detected. Try again.")
        continue

    if user_input.lower() in ["bye", "exit", "stop", "خروج", "انهاء"]:
        print("👋 Goodbye!")
        break

    try:
        reply = get_cohere_reply(user_input)
        speak_text(reply)
    except cohere.errors.UnauthorizedError:
        print("❌ Invalid Cohere API key. Please check and update your key.")
        break
    except Exception as e:
        print("❌ Error during chatbot process:", e)
