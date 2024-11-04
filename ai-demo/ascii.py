import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)  # Use the API key from the environment

# Define the function to generate ASCII art
def generate_ascii_art(subject):
    # Create a chat completion request to generate ASCII art
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate ASCII art of a {subject}."
                }
            ],
            model="gpt-3.5-turbo"  # Or "gpt-4" if you have access
        )
        # Return the ASCII art content
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't generate the ASCII art at the moment."

# Main function to interact with the user and display ASCII art
def main():
    # Get user input for the ASCII art subject
    subject = input("Enter what you want in ASCII art (e.g., cat, tree, rocket): ")

    # Generate ASCII art based on the input
    ascii_art = generate_ascii_art(subject)

    # Display the result
    print("\nGenerated ASCII Art:\n")
    print(ascii_art)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
