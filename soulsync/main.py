from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from mood_model import detect_mood
from chakra_raga import chakra_raga_map
from speech_to_text import speech_to_text
from storyteller import generate_story_with_voice

# Base URL (Render will override)
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

app = FastAPI(title="SoulSync API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folders
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
app.mount("/stories", StaticFiles(directory="stories"), name="stories")

# Root
@app.get("/")
def home():
    return {"status": "SoulSync API running"}

# Text Mood Endpoint
@app.post("/analyze-text")
def analyze_text(data: dict):
    text = data.get("text", "")
    mood = detect_mood(text)
    info = chakra_raga_map[mood]

    return {
        "text": text,
        "mood": mood,
        "chakra": info["chakra"],
        "raga": info["raga"],
        "audio": BASE_URL + info["audio"]
    }

# Speech Mood Endpoint
@app.post("/speech-mood")
async def speech_mood(file: UploadFile = File(...)):
    file_path = file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = speech_to_text(file_path)
    mood = detect_mood(text)
    info = chakra_raga_map[mood]

    try:
        os.remove(file_path)
    except:
        pass

    return {
        "text": text,
        "mood": mood,
        "chakra": info["chakra"],
        "raga": info["raga"],
        "audio": BASE_URL + info["audio"]
    }

# Story Endpoint
@app.post("/story")
def story(data: dict):
    mood = data.get("mood", "stressed")
    story_text = generate_story_with_voice(mood)

    return {
        "story": story_text,
        "audio": BASE_URL + "/stories/story.mp3"
    }
