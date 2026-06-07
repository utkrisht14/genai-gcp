import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

os.getenv("GEMINI_API_KEY")

client = genai.Client()

prompt = "Generate a image of a cat and a dog playing soccer together."

response = client.models.generate_content(
    model = "gemini-2.5-flash-image",
    contents = prompt,
)

# Print the response
for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("cat_dog_football.png")
        print("Image saved to cat_dog_football.png")

