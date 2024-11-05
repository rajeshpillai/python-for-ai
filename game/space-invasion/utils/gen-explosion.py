# Import necessary modules
import numpy as np
from scipy.io.wavfile import write

# Parameters for the explosion sound effect
sample_rate = 44100  # Samples per second
duration = 2  # Duration in seconds
frequencies = [60, 120, 250, 400]  # Multiple frequencies to create an explosion-like effect

# Generate an explosion-like sound by combining multiple frequencies
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio = np.zeros_like(t)

# Add sine waves of different frequencies
for freq in frequencies:
    audio += 0.2 * np.sin(2 * np.pi * freq * t)

# Add some noise to make it sound more like an explosion
noise = 0.05 * np.random.normal(0, 1, len(t))
audio += noise

# Normalize the audio to prevent clipping
audio = np.clip(audio, -1, 1)

# Save the explosion sound as 'explosion.wav'
explosion_wav_path = "explosion.wav"
write(explosion_wav_path, sample_rate, (audio * 32767).astype(np.int16))

# Provide the generated audio file path
explosion_wav_path

