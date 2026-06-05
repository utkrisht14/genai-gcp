from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()  # It will automatically read GEMINI_API_KEY from .env

prompt = "Edit this image so that both the cat and the dog are wearing caps."

image = Image.open("cat_dog_football.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt, image],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)

    elif part.inline_data is not None:
        edited_image = part.as_image() # Convert the response to an PIL image
        edited_image.save("edited_cat_dog_football.png")
        print("Image saved to edited_cat_dog_football.png")