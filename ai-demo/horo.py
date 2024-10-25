import os
from openai import OpenAI

from dotenv import load_dotenv
# Load environment variables from the .env file

load_dotenv()
# Get the OpenAI API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(
	api_key=api_key,  # Use the API key from the environment
)


# Define the ask_openai function
def ask_openai(question):
    # Create a chat completion request using the OpenAI client
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gpt-3.5-turbo"  # Or "gpt-4" if you have access
    )
    # Return the assistant's reply
    return response.choices[0].message.content.strip()

def horoscope():
    # Get user input for name and birth month
    name = input("Enter your name: ")
    month = input("Enter your birth month: ")

    # Create a question for the horoscope
    question = f"Generate a fun, personalized horoscope for {name} born in {month}."

    # Get the horoscope from OpenAI
    horoscope_result = ask_openai(question)

    # Print the result
    print("\nYour Horoscope:")
    print(horoscope_result)

# Call the horoscope function
horoscope()

