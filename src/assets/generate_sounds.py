import pygame
import numpy as np
import os
import wave
import struct

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def generate_tone(freq, duration, volume=0.5):
    """Generate a simple tone with the given frequency."""
    # Calculate buffer size
    buffer_size = int(44100 * duration)
    buf = np.zeros((buffer_size, 2), dtype=np.int16)
    max_sample = 2**(16 - 1) - 1
    
    # Generate a sine wave
    t = np.linspace(0, duration, buffer_size, False)
    tone = np.sin(2 * np.pi * freq * t) * max_sample * volume
    
    # Apply fade in/out
    fade_samples = int(44100 * 0.05)  # 50ms fade
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    # Apply fades (making sure we don't exceed array bounds)
    if len(tone) > fade_samples:
        tone[:fade_samples] *= fade_in
    if len(tone) > fade_samples:
        tone[-fade_samples:] *= fade_out
    
    # Convert to 16-bit data
    buf[:, 0] = tone.astype(np.int16)
    buf[:, 1] = tone.astype(np.int16)
    
    return buf

def save_wav(buf, filename):
    """Save a buffer to a WAV file."""
    # Open the WAV file
    with wave.open(filename, 'wb') as wav_file:
        # Set parameters
        nchannels = 2
        sampwidth = 2  # 16-bit
        framerate = 44100
        nframes = len(buf)
        
        # Set WAV file parameters
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))
        
        # Convert the numpy array to bytes and write to file
        for i in range(nframes):
            wav_file.writeframes(struct.pack('<h', buf[i][0]))  # Left channel
            wav_file.writeframes(struct.pack('<h', buf[i][1]))  # Right channel

def generate_cast_sound():
    """Generate a sound for casting a spell element."""
    buf = generate_tone(440, 0.2)  # A4 note
    return buf

def generate_spell_sound():
    """Generate a sound for when a spell is activated."""
    # Start with a higher frequency sound that shifts down
    buffer_size = int(44100 * 0.5)
    buf = np.zeros((buffer_size, 2), dtype=np.int16)
    max_sample = 2**(16 - 1) - 1
    
    t = np.linspace(0, 0.5, buffer_size, False)
    # Start at 880Hz (A5) and glide down to 440Hz (A4)
    freq = np.linspace(880, 440, buffer_size)
    
    tone = np.sin(2 * np.pi * freq * t) * max_sample * 0.5
    
    # Apply fade in/out
    fade_samples = int(44100 * 0.05)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    # Apply fades (making sure we don't exceed array bounds)
    if len(tone) > fade_samples:
        tone[:fade_samples] *= fade_in
    if len(tone) > fade_samples:
        tone[-fade_samples:] *= fade_out
    
    buf[:, 0] = tone.astype(np.int16)
    buf[:, 1] = tone.astype(np.int16)
    
    return buf

def generate_menu_sound():
    """Generate a menu selection sound."""
    buf = generate_tone(660, 0.1)  # E5 note
    return buf

def generate_level_complete_sound():
    """Generate a level complete fanfare."""
    # Create a short 3-note sequence
    notes = [440, 554, 660]  # A4, C#5, E5
    duration = 0.15
    buffer_size = int(44100 * duration * 3)
    buf = np.zeros((buffer_size, 2), dtype=np.int16)
    max_sample = 2**(16 - 1) - 1
    
    for i, note in enumerate(notes):
        note_buffer_size = int(44100 * duration)
        t = np.linspace(0, duration, note_buffer_size, False)
        tone = np.sin(2 * np.pi * note * t) * max_sample * 0.5
        
        # Apply fade in/out
        fade_samples = int(44100 * 0.02)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        # Apply fades (making sure we don't exceed array bounds)
        if len(tone) > fade_samples:
            tone[:fade_samples] *= fade_in
        if len(tone) > fade_samples:
            tone[-fade_samples:] *= fade_out
        
        # Add to buffer at the right position
        start_idx = int(i * 44100 * duration)
        end_idx = min(int((i + 1) * 44100 * duration), buffer_size)
        
        # Make sure we don't go beyond buffer boundaries
        samples_to_copy = min(len(tone), end_idx - start_idx)
        buf[start_idx:start_idx + samples_to_copy, 0] = tone[:samples_to_copy].astype(np.int16)
        buf[start_idx:start_idx + samples_to_copy, 1] = tone[:samples_to_copy].astype(np.int16)
    
    return buf

def save_sounds():
    """Generate and save all sound effects."""
    sounds = {
        'cast.wav': generate_cast_sound(),
        'spell.wav': generate_spell_sound(),
        'menu.wav': generate_menu_sound(),
        'complete.wav': generate_level_complete_sound()
    }
    
    # Make sure the directory exists
    sound_dir = os.path.dirname(os.path.abspath(__file__)) + '/sounds'
    os.makedirs(sound_dir, exist_ok=True)
    
    # Save each sound
    for filename, buf in sounds.items():
        try:
            filepath = os.path.join(sound_dir, filename)
            save_wav(buf, filepath)
            print(f"Saved sound to {filepath}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")

if __name__ == "__main__":
    save_sounds()
    print("Sound generation complete.") 