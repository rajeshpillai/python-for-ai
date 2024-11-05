import numpy as np
from scipy.io.wavfile import write

# Parameters for the laser sound effect
sample_rate = 44100  # Samples per second
duration = 1  # Duration in seconds
frequency_start = 800.0  # Starting frequency in Hz
frequency_end = 1200.0  # Ending frequency in Hz

# Generate a chirp-like laser sound (linearly increasing frequency)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
frequency = np.linspace(frequency_start, frequency_end, int(sample_rate * duration))
audio = 0.5 * np.sin(2 * np.pi * frequency * t)  # 0.5 to reduce the volume

# Save the laser sound as 'laser.wav'
laser_wav_path = "laser.wav"
write(laser_wav_path, sample_rate, (audio * 32767).astype(np.int16))

# Provide the generated audio file path
laser_wav_path

