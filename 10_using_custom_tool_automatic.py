# Import Gemini SDK
from google import genai

# Import dotenv to load API key from .env file
from dotenv import load_dotenv

# Import os to read environment variables if needed
import os


# Load environment variables from .env file
# Example .env:
# GEMINI_API_KEY=your_api_key_here
load_dotenv()


# Optional: read API key from environment
# This line is not required if you use client = genai.Client()
# because the client automatically reads GEMINI_API_KEY
os.getenv("GEMINI_API_KEY")


# Create Gemini client
client = genai.Client()


# ---------------------------------------------------------
# Step 1: Define a normal Python function
# ---------------------------------------------------------
# This function will become our custom tool.
# Gemini can call this function when needed.
def calculate_discount(original_price: float, discount_percent: float) -> dict:
    """
    Calculate final price after discount.

    Args:
        original_price: Original product price.
        discount_percent: Discount percentage.

    Returns:
        Dictionary containing discount amount and final price.
    """

    # Calculate discount amount
    discount_amount = original_price * discount_percent / 100

    # Calculate final price
    final_price = original_price - discount_amount

    # Return result
    return {
        "original_price": original_price,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "final_price": final_price,
    }


# ---------------------------------------------------------
# Step 2: Ask Gemini and pass the Python function as a tool
# ---------------------------------------------------------
# In automatic function calling, we do not manually create FunctionDeclaration.
# We directly pass the Python function in tools=[...].
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="A jacket costs 120 euros and has a 25 percent discount. What is the final price?",

    # Pass your Python function as a custom tool
    config={
        "tools": [calculate_discount]
    },
)


# ---------------------------------------------------------
# Step 3: Print the final answer
# ---------------------------------------------------------
# Gemini will call the function automatically if needed
# and then return the final natural language answer.
print(response.text)