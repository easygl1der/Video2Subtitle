"""Tests for audio processor"""

import pytest

from video2subs.audio_processor import AudioProcessor
from video2subs.config import AUDIO_CHANNELS, AUDIO_SAMPLE_RATE


def test_audio_processor_init():
    """Test AudioProcessor initialization"""
    processor = AudioProcessor()
    assert processor is not None


def test_extract_audio(sample_audio, temp_dir):
    """Test audio extraction and normalization"""
    processor = AudioProcessor()
    
    output_path = temp_dir / "extracted.wav"
    result_path = processor.extract_audio(sample_audio, output_path)
    
    assert result_path.exists()
    assert result_path == output_path
    
    # Check audio properties
    info = processor.get_audio_info(result_path)
    assert info["sample_rate"] == AUDIO_SAMPLE_RATE
    assert info["channels"] == AUDIO_CHANNELS
    assert info["duration"] > 0


def test_get_audio_info(sample_audio):
    """Test getting audio information"""
    processor = AudioProcessor()
    info = processor.get_audio_info(sample_audio)
    
    assert "duration" in info
    assert "sample_rate" in info
    assert "channels" in info
    assert "codec" in info
    
    assert info["sample_rate"] == 16000
    assert info["channels"] == 1
    assert info["duration"] > 0


def test_extract_audio_nonexistent_file(temp_dir):
    """Test extraction with nonexistent file"""
    processor = AudioProcessor()
    
    with pytest.raises(FileNotFoundError):
        processor.extract_audio(temp_dir / "nonexistent.mp4")
