import speech_recognition as sr
from pydub import AudioSegment
import os

def speech_to_text(file_path):
    recognizer = sr.Recognizer()

    try:
        # Convert to wav
        if not file_path.endswith(".wav"):
            sound = AudioSegment.from_file(file_path)
            wav_path = file_path + ".wav"
            sound.export(wav_path, format="wav")
            file_path = wav_path

        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text

    except:
        return ""
