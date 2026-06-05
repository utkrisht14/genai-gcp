from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

os.getenv("GEMINI_API_KEY")

client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Tell me about global warming?",
)

for chunk in response:
    print(chunk.text, end="")
