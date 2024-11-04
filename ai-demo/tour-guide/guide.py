#RUN: streamlit run guide.py

import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define the function to generate a travel guide
def generate_travel_guide(destination, preferences=""):
    try:
        # Create a prompt with the destination and preferences
        prompt = f"Create a local tour guide for {destination}. Include information on famous attractions, cultural highlights, and tips. {preferences}"
        
        # Request completion from OpenAI
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-3.5-turbo"  # Or "gpt-4" if you have access
        )
        # Return the generated travel guide
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return "Sorry, I couldn't generate the travel guide at the moment."

# Streamlit app setup
st.title("Travel Buddy and Local Tour Guide")
st.write("Enter a destination, and let your AI Travel Buddy guide you!")

# User input for destination and preferences
destination = st.text_input("Enter a travel destination (e.g., 'Paris', 'Tokyo', 'New York'):")
preferences = st.text_input("Any specific preferences? (e.g., 'food', 'history', 'adventure')")

# Generate travel guide button
if st.button("Generate Travel Guide"):
    if destination:
        # Generate the travel guide
        travel_guide = generate_travel_guide(destination, preferences)
        
        # Display the travel guide
        st.subheader(f"Your Travel Guide to {destination.title()}:")
        st.write(travel_guide)
    else:
        st.warning("Please enter a destination.")
