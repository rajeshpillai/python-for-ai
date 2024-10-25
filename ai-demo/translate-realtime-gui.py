import os
import json
import openai
import tkinter as tk
from tkinter import ttk
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import pyaudio
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

# Base path for models based on the executable directory
base_path = os.path.dirname(os.path.abspath(__file__))

# Dictionary mapping languages to their relative Vosk model paths
model_paths = {
    "en": os.path.join(base_path, "lang-models", "vosk-lang-models", "model-en-us-small"),
    "hi": os.path.join(base_path, "lang-models", "vosk-lang-models", "model-hi-small"),
    # Add other languages and corresponding model paths as needed
}

# Initialize variables
is_listening = False
is_paused = False
recognizer = None  # Recognizer will be created dynamically based on language

def load_vosk_model(language_code):
    global recognizer
    model_path = model_paths.get(language_code, "")
    if not os.path.exists(model_path):
        print(f"Model path for language '{language_code}' does not exist.")
        return
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

# Call this function whenever the source language is changed
def on_source_language_change(event=None):
    source_lang = source_lang_var.get()
    load_vosk_model(source_lang)  # Load the appropriate model based on the source language

def start_translation():
    global is_listening, is_paused
    is_listening = True
    is_paused = False
    
    # Disable Start and enable Stop, Pause
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    pause_button.config(state="normal")
    
    # Start transcription in a separate thread
    threading.Thread(target=real_time_transcription).start()

def pause_translation():
    global is_paused
    is_paused = True
    pause_button.config(state="disabled")
    start_button.config(state="normal")

def stop_translation():
    global is_listening
    is_listening = False
    
    # Re-enable Start, disable Pause and Stop
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    pause_button.config(state="disabled")

def translate_text(text):
    source_lang = languages[source_lang_var.get()]
    target_lang = languages[target_lang_var.get()]

    # Prepare prompt for translation
    prompt = f"Translate '{text}' from {source_lang} to {target_lang}."
    translated_text = ask_openai(prompt)
    target_text_var.set(translated_text)
    
    # Convert translated text to speech
    tts = gTTS(translated_text, lang=target_lang_var.get())
    tts.save("translated_audio.mp3")
    os.system("mpg321 translated_audio.mp3")

def real_time_transcription():
    global is_listening, is_paused, recognizer
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")
    while is_listening and recognizer:
        if not is_paused:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    print("Recognized Text:", text)
                    source_text_var.set(text)
                    translate_text(text)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Language mappings for UI dropdown and translation
languages = {
    "en": "English",
    "hi": "Hindi",
    # Add other languages as needed
}

# GUI Setup
root = tk.Tk()
root.title("Real-Time Language Translator")
# root.attributes("-fullscreen", True) 
root.state('normal')  # Full screen on most OS; use 'normal' if 'zoomed' doesn't work

# Configure the grid to make left and right frames equally occupy space
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Define source and target language variables for dropdowns
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
source_lang_menu.bind("<<ComboboxSelected>>", on_source_language_change)  # Bind change event

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

# Buttons for Start, Pause, and Stop
button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

start_button = ttk.Button(button_frame, text="Start Translation", command=start_translation)
start_button.grid(row=0, column=0, padx=10)

pause_button = ttk.Button(button_frame, text="Pause", command=pause_translation, state="disabled")
pause_button.grid(row=0, column=1, padx=10)

stop_button = ttk.Button(button_frame, text="Stop Translation", command=stop_translation, state="disabled")
stop_button.grid(row=0, column=2, padx=10)

# Load initial Vosk model based on the default source language
load_vosk_model(source_lang_var.get())

# Run the application
root.mainloop()
