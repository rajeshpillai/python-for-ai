import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define the function to generate a social media caption
def generate_caption(description, style="funny"):
    try:
        # Create a prompt with the description and style
        prompt = f"Create a {style} social media caption for a photo described as '{description}'. Keep it under 150 characters."
        
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
        # Return the generated caption
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return "Sorry, I couldn't generate a caption at the moment."

# Streamlit app setup
st.title("Creative AI for Social Media Captions")
st.write("Upload a photo and let AI generate a catchy caption!")

# File uploader
uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Get description and caption style from user
    description = st.text_input("Describe the photo (e.g., 'sunset at the beach')")
    style = st.selectbox("Select the style of the caption", ["funny", "romantic", "inspirational", "motivational"])

    if st.button("Generate Caption"):
        if description:
            # Generate the caption
            caption = generate_caption(description, style)
            # Display the caption
            st.subheader("Generated Caption:")
            st.write(caption)
        else:
            st.warning("Please enter a description of the photo.")
