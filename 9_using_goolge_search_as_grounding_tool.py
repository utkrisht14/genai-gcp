from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

os.getenv("GEMINI_API_KEY")

client = genai.Client()

grounding_tool = types.Tool(
    google_search = types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="1 Euro into INR ?",
    config=config,
)

print(response.text)