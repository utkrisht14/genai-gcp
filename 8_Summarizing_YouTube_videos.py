import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Set API key
os.getenv("GEMINI_API_KEY")

client = genai.Client()

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=types.Content(
        parts = [
            types.Part(
                file_data=types.FileData(file_uri="https://www.youtube.com/watch?v=a3IHH5boCAY")
            ),
            types.Part(text="Summarize the video in 5 sentences.")
        ]
    )
)

print(response.text)