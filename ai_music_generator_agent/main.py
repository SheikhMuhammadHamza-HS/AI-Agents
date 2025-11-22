import os
import uuid
import numpy as np
import scipy.io.wavfile
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import math
import random

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent / '.env'
print(f"Looking for .env at: {env_path.absolute()}")
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# Ensure generated directory exists
GENERATED_DIR = "static/generated"
os.makedirs(GENERATED_DIR, exist_ok=True)

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY or GEMINI_API_KEY not found in .env")
    print("Available keys:", [k for k in os.environ.keys() if "API_KEY" in k])
else:
    GOOGLE_API_KEY = GOOGLE_API_KEY.strip()
    print(f"API Key found: {GOOGLE_API_KEY[:5]}...")
    genai.configure(api_key=GOOGLE_API_KEY)

# Try to load MusicGen
processor = None
model_music = None
USE_FALLBACK = False

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    import torch
    print("Loading MusicGen model... This might take a while.")
    # processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    # model_music = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    # print("MusicGen model loaded successfully!")
    # Commented out to prevent auto-download on start if user hasn't installed torch yet.
    # We will load it on demand or if explicitly installed.
    # For this demo, we will default to fallback if torch fails to import or load.
    USE_FALLBACK = True # Set to False if you have torch installed and want to use MusicGen
except ImportError:
    print("Transformers/Torch not found. Using fallback synthesizer.")
    USE_FALLBACK = True

@app.on_event("startup")
async def startup_event():
    global processor, model_music, USE_FALLBACK
    if not USE_FALLBACK:
        try:
            processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
            model_music = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
            print("MusicGen loaded.")
        except Exception as e:
            print(f"Could not load MusicGen: {e}. Switching to fallback.")
            USE_FALLBACK = True

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

class MusicRequest(BaseModel):
    prompt: str

import json
import re

def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Add some harmonics for a richer sound
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave += 0.2 * np.sin(4 * np.pi * frequency * t) # 2nd harmonic
    wave += 0.1 * np.sin(6 * np.pi * frequency * t) # 3rd harmonic
    
    # Simple ADSR Envelope
    total_samples = len(t)
    attack = int(0.1 * total_samples)
    decay = int(0.1 * total_samples)
    release = int(0.2 * total_samples)
    sustain = total_samples - attack - decay - release
    
    envelope = np.concatenate([
        np.linspace(0, 1, attack),
        np.linspace(1, 0.7, decay),
        np.full(sustain, 0.7),
        np.linspace(0.7, 0, release)
    ])
    
    if len(envelope) != len(wave):
        # Handle rounding errors
        envelope = np.resize(envelope, len(wave))
        
    return wave * envelope

def generate_fallback_music(prompt):
    sample_rate = 44100
    
    # Default melody if Gemini fails
    melody = [{"freq": 440, "duration": 0.5}, {"freq": 523.25, "duration": 0.5}]
    
    if GOOGLE_API_KEY:
        try:
            print("Asking Gemini to compose melody...")
            gemini_model = genai.GenerativeModel('gemini-2.5-flash')
            gemini_prompt = f"""
            You are a music composer. Create a simple monophonic melody for a '{prompt}' mood.
            Return ONLY a JSON array of objects, where each object has:
            - 'freq': float (frequency in Hz, e.g., 261.63 for C4, 440 for A4). Keep between 100 and 800.
            - 'duration': float (duration in seconds, e.g., 0.25, 0.5, 1.0).
            
            Total duration should be around 5-8 seconds.
            Example output: [{{"freq": 440, "duration": 0.5}}, {{"freq": 523.25, "duration": 0.5}}]
            DO NOT include markdown formatting like ```json. Just the raw JSON string.
            """
            response = gemini_model.generate_content(gemini_prompt)
            text_response = response.text.strip()
            # Clean up markdown if present
            text_response = text_response.replace("```json", "").replace("```", "")
            melody = json.loads(text_response)
            print(f"Gemini composed {len(melody)} notes.")
        except Exception as e:
            print(f"Gemini composition failed: {e}. Using random notes.")
            # Fallback to random if Gemini fails
            melody = []
            base_freq = 220 if "sad" in prompt.lower() else 440
            for _ in range(10):
                melody.append({
                    "freq": base_freq * (2 ** (random.randint(0, 12) / 12)),
                    "duration": 0.5
                })

    audio = np.array([], dtype=np.float32)
    
    for note in melody:
        freq = float(note.get("freq", 440))
        duration = float(note.get("duration", 0.5))
        # Cap duration to avoid hanging
        duration = min(duration, 2.0)
        
        wave = generate_sine_wave(freq, duration, sample_rate)
        audio = np.concatenate((audio, wave.astype(np.float32)))
        
    return audio, sample_rate

@app.post("/generate")
async def generate_music(request: MusicRequest):
    global processor, model_music, USE_FALLBACK
    
    user_prompt = request.prompt
    print(f"Received prompt: {user_prompt}")

    # Step 1: Enhance prompt using Gemini
    enhanced_prompt = user_prompt
    if GOOGLE_API_KEY:
        try:
            gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            gemini_prompt = f"You are a music composer. The user wants: '{user_prompt}'. Describe this music in 5 words (e.g. 'Sad, Piano, Slow, Minor, Ambient')."
            response = gemini_model.generate_content(gemini_prompt)
            if response.text:
                enhanced_prompt = response.text.strip()
                print(f"Enhanced prompt: {enhanced_prompt}")
        except Exception as e:
            print(f"Gemini error: {e}")

    # Step 2: Generate Music
    try:
        filename = f"{uuid.uuid4()}.wav"
        filepath = os.path.join(GENERATED_DIR, filename)
        
        if not USE_FALLBACK and processor and model_music:
            print("Using MusicGen model.")
            inputs = processor(
                text=[enhanced_prompt],
                padding=True,
                return_tensors="pt",
            )
            audio_values = model_music.generate(**inputs, max_new_tokens=256)
            sampling_rate = model_music.config.audio_encoder.sampling_rate
            audio_data = audio_values[0, 0].numpy()
            scipy.io.wavfile.write(filepath, rate=sampling_rate, data=audio_data)
        else:
            # Fallback generation
            print("Using fallback generator.")
            audio_data, sampling_rate = generate_fallback_music(user_prompt)
            # Ensure data is float32 and normalized
            audio_data = audio_data.astype(np.float32)
            scipy.io.wavfile.write(filepath, rate=sampling_rate, data=audio_data)
        
        return {
            "message": f"Generated music for: '{enhanced_prompt}'",
            "audio_url": f"/static/generated/{filename}"
        }

    except Exception as e:
        print(f"Generation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
