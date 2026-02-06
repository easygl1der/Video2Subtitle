#!/usr/bin/env python3
"""
Generate a sample audio file for testing
"""

import wave
from pathlib import Path

import numpy as np


def generate_sample_audio(output_path: Path, duration: float = 5.0):
    """
    Generate a sample audio file with sine waves
    
    Args:
        output_path: Path to save the audio file
        duration: Duration in seconds
    """
    sample_rate = 16000
    
    # Generate multiple tones
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Mix of frequencies
    audio = np.zeros_like(t)
    audio += 0.3 * np.sin(2 * np.pi * 440 * t)  # A4
    audio += 0.2 * np.sin(2 * np.pi * 554 * t)  # C#5
    audio += 0.15 * np.sin(2 * np.pi * 659 * t)  # E5
    
    # Add some silence in the middle
    silence_start = int(len(audio) * 0.4)
    silence_end = int(len(audio) * 0.6)
    audio[silence_start:silence_end] *= 0.1
    
    # Convert to 16-bit PCM
    audio_data = (audio * 32767).astype(np.int16)
    
    # Save as WAV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"Generated sample audio: {output_path}")
    print(f"Duration: {duration}s, Sample rate: {sample_rate}Hz")


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "tests" / "assets"
    output_path = output_dir / "sample_audio.wav"
    generate_sample_audio(output_path, duration=5.0)
