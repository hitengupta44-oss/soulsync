import os
import google.generativeai as genai
from gtts import gTTS

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Ensure stories folder exists
os.makedirs("stories", exist_ok=True)

def generate_story_with_voice(mood):
    try:
        prompt = f"""
        Write a short Panchatantra-style story for a person feeling {mood}.
        Include animal characters and a moral. Keep it under 100 words.
        """

        response = model.generate_content(prompt)
        story_text = response.text.strip()

    except:
        story_text = "Once a tired deer learned to rest and breathe calmly. Slowly, peace returned. Moral: Rest heals the mind."

    # Convert story to speech
    audio_path = "stories/story.mp3"
    try:
        tts = gTTS(story_text)
        tts.save(audio_path)
    except:
        pass

    return story_text
