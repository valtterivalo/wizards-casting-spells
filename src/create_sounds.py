import wave
import struct
import numpy as np
import os

def create_directory():
    """Create the sounds directory if it doesn't exist."""
    os.makedirs('assets/sounds', exist_ok=True)

def save_wave(file_path, samples, sample_rate=44100):
    """Save a numpy array as a WAV file."""
    # Ensure the samples are in the valid range [-1, 1]
    samples = np.clip(samples, -1, 1)
    
    # Convert to 16-bit PCM
    samples = (samples * 32767).astype(np.int16)
    
    # Create a new WAV file
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Write the audio data
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))
    
    print(f"Created sound file: {file_path}")

def generate_cast_sound():
    """Generate a sound for spell casting."""
    duration = 0.3  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Create a chirp sound (increasing frequency)
    f0 = 300
    f1 = 800
    samples = 0.5 * np.sin(2 * np.pi * (f0 + (f1 - f0) * t / duration) * t)
    
    # Apply a quick fade-out
    fade_out = np.linspace(1, 0, int(sample_rate * 0.1))
    samples[-len(fade_out):] *= fade_out
    
    save_wave('assets/sounds/cast.wav', samples, sample_rate)

def generate_spell_sound():
    """Generate a sound for spell activation."""
    duration = 0.5  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Create a more complex sound with harmonics
    f0 = 200
    samples = 0.3 * np.sin(2 * np.pi * f0 * t)
    samples += 0.2 * np.sin(2 * np.pi * f0 * 2 * t)
    samples += 0.1 * np.sin(2 * np.pi * f0 * 3 * t)
    
    # Add a bit of a magical shimmer (tremolo)
    tremolo = 1 + 0.3 * np.sin(2 * np.pi * 20 * t)
    samples *= tremolo
    
    # Apply an envelope
    envelope = np.ones_like(samples)
    attack = int(sample_rate * 0.05)
    release = int(sample_rate * 0.2)
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[-release:] = np.linspace(1, 0, release)
    samples *= envelope
    
    save_wave('assets/sounds/spell.wav', samples, sample_rate)

def generate_menu_sound():
    """Generate a sound for menu navigation."""
    duration = 0.15  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Create a simple 'blip' sound
    f0 = 500
    samples = 0.4 * np.sin(2 * np.pi * f0 * t)
    
    # Apply a quick fade-out
    envelope = np.ones_like(samples)
    envelope[-int(sample_rate * 0.05):] = np.linspace(1, 0, int(sample_rate * 0.05))
    samples *= envelope
    
    save_wave('assets/sounds/menu.wav', samples, sample_rate)

def generate_complete_sound():
    """Generate a sound for level completion."""
    duration = 1.0  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Create an ascending three-note arpeggio
    f_base = 300
    samples = np.zeros_like(t)
    
    # First note
    idx1 = int(sample_rate * 0.3)
    samples[:idx1] = 0.3 * np.sin(2 * np.pi * f_base * t[:idx1])
    
    # Second note
    idx2 = int(sample_rate * 0.6)
    samples[idx1:idx2] = 0.3 * np.sin(2 * np.pi * (f_base * 1.25) * t[idx1:idx2])
    
    # Third note (higher and with harmonics)
    samples[idx2:] = 0.2 * np.sin(2 * np.pi * (f_base * 1.5) * t[idx2:])
    samples[idx2:] += 0.1 * np.sin(2 * np.pi * (f_base * 3.0) * t[idx2:])
    
    # Apply envelopes to each note
    attack = int(sample_rate * 0.05)
    release = int(sample_rate * 0.1)
    
    # First note envelope
    env1 = np.ones(idx1)
    env1[:attack] = np.linspace(0, 1, attack)
    env1[-release:] = np.linspace(1, 0, release)
    samples[:idx1] *= env1
    
    # Second note envelope
    env2 = np.ones(idx2 - idx1)
    env2[:attack] = np.linspace(0, 1, attack)
    env2[-release:] = np.linspace(1, 0, release)
    samples[idx1:idx2] *= env2
    
    # Third note envelope
    env3 = np.ones(len(samples) - idx2)
    env3[:attack] = np.linspace(0, 1, attack)
    env3[-release:] = np.linspace(1, 0, release)
    samples[idx2:] *= env3
    
    save_wave('assets/sounds/complete.wav', samples, sample_rate)

if __name__ == "__main__":
    # Create the directory structure
    create_directory()
    
    # Generate the sound effects
    generate_cast_sound()
    generate_spell_sound()
    generate_menu_sound()
    generate_complete_sound()
    
    print("All sound effects generated successfully!") 