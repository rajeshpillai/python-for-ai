import os
import json
import openai
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# Define the ask_openai function with the structure you provided
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

# Load languages from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
languages_file_path = os.path.join(current_dir, "languages.json")

with open(languages_file_path, "r") as file:
    languages = json.load(file)

# Initialize the recognizer with adjusted settings
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

# Function to capture and translate speech
def translate_speech():
    source_lang = source_lang_var.get()
    target_lang = target_lang_var.get()
    
    try:
        # Capture speech
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            spoken_text = recognizer.recognize_google(audio, language=source_lang)
            print(f"Recognized Text ({languages[source_lang]}): {spoken_text}")
            source_text_var.set(spoken_text)
        
        # Translate text with OpenAI
        prompt = f"Translate '{spoken_text}' from {languages[source_lang]} to {languages[target_lang]}."
        translated_text = ask_openai(prompt)
        target_text_var.set(translated_text)
        
        # Convert translated text to speech
        tts = gTTS(translated_text, lang=target_lang)
        tts.save("translated_audio.mp3")
        playsound("translated_audio.mp3")
        os.remove("translated_audio.mp3")

    except sr.UnknownValueError:
        source_text_var.set("Could not understand audio. Please try again.")
    except sr.RequestError as e:
        source_text_var.set(f"Could not request results; {e}")
    except Exception as e:
        target_text_var.set(f"Translation error: {e}")

# Create the main application window
root = tk.Tk()
root.title("Language Translator")
root.geometry("500x300")

# Language selection dropdowns
source_lang_var = tk.StringVar(value="en")
target_lang_var = tk.StringVar(value="hi")  # Default to Hindi

# Left dropdown for source language
ttk.Label(root, text="Source Language").grid(row=0, column=0, padx=10, pady=10)
source_lang_menu = ttk.Combobox(root, textvariable=source_lang_var, values=list(languages.keys()))
source_lang_menu.grid(row=1, column=0, padx=10)
source_lang_menu.set("en")

# Right dropdown for target language
ttk.Label(root, text="Target Language").grid(row=0, column=1, padx=10, pady=10)
target_lang_menu = ttk.Combobox(root, textvariable=target_lang_var, values=list(languages.keys()))
target_lang_menu.grid(row=1, column=1, padx=10)
target_lang_menu.set("hi")  # Set Hindi as the default target language

# Text fields for source and translated text
source_text_var = tk.StringVar()
target_text_var = tk.StringVar()

ttk.Label(root, text="Recognized Text").grid(row=2, column=0, padx=10, pady=10)
source_text_label = ttk.Label(root, textvariable=source_text_var, wraplength=200, relief="solid", padding=5)
source_text_label.grid(row=3, column=0, padx=10, pady=5)

ttk.Label(root, text="Translated Text").grid(row=2, column=1, padx=10, pady=10)
target_text_label = ttk.Label(root, textvariable=target_text_var, wraplength=200, relief="solid", padding=5)
target_text_label.grid(row=3, column=1, padx=10, pady=5)

# Button to start translation
translate_button = ttk.Button(root, text="Translate Speech", command=translate_speech)
translate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
