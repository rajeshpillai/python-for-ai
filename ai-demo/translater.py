import os
import json
import openai
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# Define the ask_openai function
def ask_openai(question):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": question}
        ],
        model="gpt-3.5-turbo"
    )
    return response.choices[0].message.content.strip()

# Load languages from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
languages_file_path = os.path.join(current_dir, "languages.json")

with open(languages_file_path, "r") as file:
    languages = json.load(file)

recognizer = sr.Recognizer()
audio_data = None  # Variable to store the recorded audio

def start_translation():
    global audio_data
    # Reset any previously recorded audio
    audio_data = None
    
    # Disable Start and enable Stop
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    
    # Start listening in a separate thread
    translation_thread = threading.Thread(target=record_audio)
    translation_thread.start()

def record_audio():
    global audio_data
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... You may speak for as long as you like. Click 'Stop' to end.")
        audio_data = recognizer.listen(source)  # No timeout or phrase limit, waits until stopped by user

def stop_translation():
    global audio_data
    # Process the audio and perform translation
    if audio_data:
        try:
            source_lang = source_lang_var.get()
            target_lang = target_lang_var.get()
            
            # Recognize the captured audio
            spoken_text = recognizer.recognize_google(audio_data, language=source_lang)
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
    
    # Re-enable Start and disable Stop
    start_button.config(state="normal")
    stop_button.config(state="disabled")

# Create the main application window
root = tk.Tk()
root.title("Language Translator")
# root.attributes("-fullscreen", True)) 
root.state('normal')  # Standard

# Language selection dropdowns
source_lang_var = tk.StringVar(value="en")
target_lang_var = tk.StringVar(value="hi")

# Left side for source language
left_frame = ttk.Frame(root, padding=10)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.columnconfigure(0, weight=1)

ttk.Label(left_frame, text="Source Language").grid(row=0, column=0, pady=5)
source_lang_menu = ttk.Combobox(left_frame, textvariable=source_lang_var, values=list(languages.keys()))
source_lang_menu.grid(row=1, column=0, pady=5, sticky="ew")
source_lang_menu.set("en")

source_text_var = tk.StringVar()
ttk.Label(left_frame, text="Recognized Text").grid(row=2, column=0, pady=5)
source_text_label = ttk.Label(left_frame, textvariable=source_text_var, wraplength=400, relief="solid", padding=10)
source_text_label.grid(row=3, column=0, pady=5, sticky="nsew")

# Right side for target language
right_frame = ttk.Frame(root, padding=10)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.columnconfigure(0, weight=1)

ttk.Label(right_frame, text="Target Language").grid(row=0, column=0, pady=5)
target_lang_menu = ttk.Combobox(right_frame, textvariable=target_lang_var, values=list(languages.keys()))
target_lang_menu.grid(row=1, column=0, pady=5, sticky="ew")
target_lang_menu.set("hi")

target_text_var = tk.StringVar()
ttk.Label(right_frame, text="Translated Text").grid(row=2, column=0, pady=5)
target_text_label = ttk.Label(right_frame, textvariable=target_text_var, wraplength=400, relief="solid", padding=10)
target_text_label.grid(row=3, column=0, pady=5, sticky="nsew")

# Buttons for Start and Stop
button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

start_button = ttk.Button(button_frame, text="Start Translation", command=start_translation)
start_button.grid(row=0, column=0, padx=10)

stop_button = ttk.Button(button_frame, text="Stop Translation", command=stop_translation, state="disabled")
stop_button.grid(row=0, column=1, padx=10)

# Run the application
root.mainloop()
