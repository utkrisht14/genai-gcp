from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me about global warming?"
)

print(response.text)

# Print the output number of tokens
print("\n \n Total output tokens: ", response.usage_metadata.total_token_count)

print("Total prompt tokens: ", response.usage_metadata.prompt_token_count)

print("Candidate token count:", response.usage_metadata.candidates_token_count)

print("Thoughts token count:", response.usage_metadata.thoughts_token_count)