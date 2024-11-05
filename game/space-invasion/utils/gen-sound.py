import numpy as np
from scipy.io.wavfile import write

# Parameters for the WAV file
sample_rate = 44100  # Samples per second
duration = 10  # Duration in seconds
frequency = 440.0  # Frequency in Hz (A4 note)

# Generate a sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio = 0.5 * np.sin(2 * np.pi * frequency * t)  # 0.5 to reduce the volume

# Save the sine wave as 'background.wav'
background_wav_path = "background.wav"
write(background_wav_path, sample_rate, (audio * 32767).astype(np.int16))

# Provide the generated audio file path
background_wav_path

