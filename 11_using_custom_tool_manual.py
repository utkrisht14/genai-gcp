# Import the Gemini SDK
from google import genai

# Import types from Google GenAI SDK
# We use this for creating tool/function declarations and config
from google.genai import types

# Load environment variables from .env file
from dotenv import load_dotenv

# os is used to read environment variables like GEMINI_API_KEY
import os


# Load variables from the .env file into the environment
# Example .env file:
# GEMINI_API_KEY=your_api_key_here
load_dotenv()


# Read the GEMINI_API_KEY from environment variables
# This line only reads the key.
os.getenv("GEMINI_API_KEY")


# Create a Gemini client
# genai.Client() automatically checks for GEMINI_API_KEY in your environment
client = genai.Client()


# ---------------------------------------------------------
# Step 1: Define your normal Python function
# ---------------------------------------------------------
# This is your custom tool.
# Gemini can request to call this function when it needs the answer.
def calculate_discount(original_price: float, discount_percent: float) -> dict:
    """
    Calculate final price after applying discount.

    Args:
        original_price: Original product price.
        discount_percent: Discount percentage.

    Returns:
        A dictionary containing discount amount and final price.
    """

    # Calculate discount amount
    discount_amount = original_price * discount_percent / 100

    # Calculate final price after discount
    final_price = original_price - discount_amount

    # Return result as dictionary
    return {
        "original_price": original_price,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "final_price": final_price,
    }


# ---------------------------------------------------------
# Step 2: Declare the function/tool for Gemini
# ---------------------------------------------------------
# This tells Gemini:
# - function name
# - what the function does
# - what arguments it needs
#
# Important:
# Gemini does not automatically know your Python function.
# You must describe the function using FunctionDeclaration.
discount_function = types.FunctionDeclaration(
    name="calculate_discount",
    description="Calculate the final price after applying a discount percentage.",
    parameters={
        "type": "object",
        "properties": {
            "original_price": {
                "type": "number",
                "description": "The original price of the product.",
            },
            "discount_percent": {
                "type": "number",
                "description": "The discount percentage to apply.",
            },
        },
        "required": ["original_price", "discount_percent"],
    },
)


# ---------------------------------------------------------
# Step 3: Create a tool object
# ---------------------------------------------------------
# We attach our function declaration inside a Tool.
custom_tool = types.Tool(
    function_declarations=[discount_function]
)


# ---------------------------------------------------------
# Step 4: Create model config and pass the tool
# ---------------------------------------------------------
# This tells Gemini that it is allowed to use our custom tool.
config = types.GenerateContentConfig(
    tools=[custom_tool]
)


# ---------------------------------------------------------
# Step 5: Ask Gemini a question
# ---------------------------------------------------------
# Gemini will inspect the question.
# If it thinks the custom function is useful, it will return a function call.
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="A jacket costs 120 euros and has a 25 percent discount. What is the final price?",
    config=config,
)


# ---------------------------------------------------------
# Step 6: Get the function call from Gemini response
# ---------------------------------------------------------
# Gemini may return a function call instead of a direct text answer.
function_call = response.function_calls[0]


# Print what function Gemini wants to call
print("Function name Gemini wants to call:")
print(function_call.name)

print("\nArguments Gemini provided:")
print(function_call.args)


# ---------------------------------------------------------
# Step 7: Call the actual Python function yourself
# ---------------------------------------------------------
# Gemini only requests the function call.
# Your Python code must execute the function.
if function_call.name == "calculate_discount":

    # Extract arguments from Gemini's function call
    original_price = function_call.args["original_price"]
    discount_percent = function_call.args["discount_percent"]

    # Call your real Python function
    tool_result = calculate_discount(
        original_price=original_price,
        discount_percent=discount_percent,
    )

    print("\nResult from our Python function:")
    print(tool_result)


# ---------------------------------------------------------
# Step 8: Send the function result back to Gemini
# ---------------------------------------------------------
# Now Gemini can use the tool result to create a natural language answer.
final_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        # Original user question
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text="A jacket costs 120 euros and has a 25 percent discount. What is the final price?"
                )
            ],
        ),

        # Gemini's function call from the previous response
        response.candidates[0].content,

        # Our function result sent back to Gemini
        types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="calculate_discount",
                    response=tool_result,
                )
            ],
        ),
    ],
    config=config,
)


# ---------------------------------------------------------
# Step 9: Print Gemini's final answer
# ---------------------------------------------------------
print("\nFinal answer from Gemini:")
print(final_response.text)