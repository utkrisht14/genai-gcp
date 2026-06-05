import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

os.getenv("GEMINI_API_KEY")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me ancient human civilization?",
    config = types.GenerateContentConfig(
        system_instruction="You are a history professor.")
)

print(response.text)