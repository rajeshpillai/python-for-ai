import numpy as np
import wave

def generate_wave(filename, frequency, duration, volume, sample_rate=44100):
    # Generate time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate a sine wave at the given frequency
    wave_data = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

    # Write to a .wav file
    with wave.open(filename, 'w') as wav_file:
        # Set the wave parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        # Write the wave data
        wav_file.writeframes(wave_data.tobytes())

# Generate 'eat.wav' - A short beep sound
generate_wave("eat.wav", frequency=800, duration=0.2, volume=10000)

# Generate 'game_over.wav' - A lower, longer sound
generate_wave("game_over.wav", frequency=150, duration=0.5, volume=15000)

