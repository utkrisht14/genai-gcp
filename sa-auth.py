from pathlib import Path
import os

from dotenv import load_dotenv
from google.genai import Client
from google.oauth2.service_account import Credentials


load_dotenv()

SERVICE_ACCOUNT_FILE = Path("keys.json")

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
MODEL_NAME = os.getenv("MODEL_NAME")

missing_values = [
    name
    for name, value in {
        "PROJECT_ID": PROJECT_ID,
        "REGION": REGION,
        "MODEL_NAME": MODEL_NAME,
    }.items()
    if not value
]

if missing_values:
    raise RuntimeError(
        "Missing required environment variable(s): "
        + ", ".join(missing_values)
    )

if not SERVICE_ACCOUNT_FILE.exists():
    raise FileNotFoundError(
        f"Service account file not found: {SERVICE_ACCOUNT_FILE.resolve()}"
    )

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = Client(
    vertexai=True,
    project=PROJECT_ID,
    location=REGION,
    credentials=credentials,
)

response = client.models.generate_content(
    model=MODEL_NAME,
    contents="What is the color of an apple?",
)

print("Model Response:\n", response.text)