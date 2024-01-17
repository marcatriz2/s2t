import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# Corrected file path with raw string
audio_file_path = r"C:\Users\catalin.rizea\OneDrive - Logo\Desktop\test.mp4"

# Simple rate limiting function
def rate_limited(max_per_minute):
    min_interval = 60.0 / float(max_per_minute)
    last_called = [0.0]

    def decorate(func):
        def rate_limited_function(*args, **kws):
            elapsed = time.perf_counter() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_called[0] = time.perf_counter()
            return func(*args, **kws)
        return rate_limited_function
    return decorate

@rate_limited(max_per_minute=10)
def make_api_call():
    try:
        with open(audio_file_path, "rb") as audio_file:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
    except Exception as e:
        print(f"An error occurred: {e}")

# Test the API call
for _ in range(20):
    transcript = make_api_call()
    print(transcript)

