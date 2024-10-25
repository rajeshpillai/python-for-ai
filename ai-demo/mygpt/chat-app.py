import os
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# Define the ask_openai function with your working code
def ask_openai(question):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": question}
        ],
        model="gpt-3.5-turbo"
    )
    return response.choices[0].message.content.strip()

# Streamlit app setup
st.title("ChatGPT-like App")
st.write("Interact with ChatGPT!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display the chat history
for user_msg, bot_msg in st.session_state["messages"]:
    st.write(f"**You**: {user_msg}")
    st.write(f"**ChatGPT**: {bot_msg}")

# Initialize session state for user input if it doesn't exist
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Temporary variable to handle user input
user_input = st.text_input("You:", value=st.session_state["user_input"], key="user_input_placeholder")

if st.button("Send"):
    if user_input:
        # Append the user's message to the chat history
        st.session_state["messages"].append((user_input, ""))

        # Get the response from OpenAI
        bot_response = ask_openai(user_input)

        # Update the last message with the bot's response
        st.session_state["messages"][-1] = (user_input, bot_response)

        # Clear user input by resetting st.session_state["user_input"]
        st.session_state["user_input"] = ""  # Reset input state
        
