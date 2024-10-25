import os
import wave
import json
import openai
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import pyaudio
from dotenv import load_dotenv

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

# Load the Vosk model
# Get the absolute path of the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the model path relative to the script directory
model_path = os.path.join(script_dir, "lang-models", "vosk-lang-models", "model-en-us-small")

print(model_path)
# Initialize the Vosk model
model = Model(model_path)  # Load the model using the absolute path

def translate_text(text):
    # Prepare prompt for translation
    prompt = f"Translate '{text}' from English to Hindi."
    translated_text = ask_openai(prompt)
    print("Translated Text:", translated_text)
    
    # Convert translated text to speech
    tts = gTTS(translated_text, lang="hi")
    tts.save("translated_audio.mp3")
    os.system("mpg321 translated_audio.mp3")  # Play the audio

def real_time_transcription():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    recognizer = KaldiRecognizer(model, 16000)
    print("Listening...")

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text:
                print("Recognized Text:", text)
                translate_text(text)  # Send recognized text for translation

# Run real-time transcription and translation
real_time_transcription()
