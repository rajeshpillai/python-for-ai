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

def ask_openai(question):
    # Create a chat completion request using the OpenAI client
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access to it
    )
    # Return the assistant's reply
    return response.choices[0].message.content.strip()

def main():
    print('Jarvis: Hello there!')

    while True:
        user_input = input('you: ').strip()

        if user_input.lower() == 'hi':
            print('Jarvis: Hi, how can I help you?')

        elif user_input.lower() == 'who are you':
            print('Jarvis: I am your chatbot... now powered by OpenAI!')

        elif user_input.lower() == 'how are you':
            print('Jarvis: I am doing great... hope you are enjoying your day.')

        else:
            print('Jarvis: Let me think...')
            bot_response = ask_openai(user_input)
            print(f'Jarvis: {bot_response}')

        continue_input = input('Jarvis: Do you want to continue? (yes/no): ').strip().lower()
        if continue_input == 'no':
            print('Jarvis: Goodbye!')
            break

if __name__ == "__main__":
    main()

