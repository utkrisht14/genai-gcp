# Load environment variables from a .env file
from dotenv import load_dotenv

# Import Google's GenAI SDK
from google import genai

# time is used to pause the program while waiting for video generation
import time

# os is used to read environment variables like GEMINI_API_KEY
import os


# Load variables from the .env file into the environment
# Example .env file:
# GEMINI_API_KEY=your_api_key_here
load_dotenv()


# Read the GEMINI_API_KEY from environment variables
# Note: This line only reads the key but does not store or use it.
# genai.Client() can automatically use GEMINI_API_KEY from the environment.
os.getenv("GEMINI_API_KEY")


# Create a GenAI client
# This client is used to communicate with Gemini / Veo models
client = genai.Client()


# Text prompt describing what kind of video we want to generate
prompt = "Create a 5 sec video about the history of mankind."


# Send a video generation request to the Veo model
# Video generation is a long-running operation, so it does not return the video immediately.
# Instead, it returns an operation object that we can check later.
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt
)


# Keep checking the operation status until the video is ready
# operation.done becomes True when video generation is finished
while not operation.done:
    print("Waiting for the video to be ready...")

    # Wait 10 seconds before checking again
    # This avoids checking the server continuously
    time.sleep(10)

    # Get the latest status of the operation from the API
    operation = client.operations.get(operation)


# Once the operation is done, get the first generated video from the response
# generated_videos is a list, so [0] means the first video
generated_video = operation.response.generated_videos[0]


# Download the generated video file from Google's server
client.files.download(file=generated_video.video)


# Save the downloaded video to the current working directory
# The file will be saved as generated_video.mp4
generated_video.video.save("generated_video.mp4")


# Print confirmation message
print("Video downloaded successfully!")