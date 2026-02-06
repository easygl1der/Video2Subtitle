"""
Configuration and constants for video2subs
"""

import os
from pathlib import Path
from typing import Optional

# Default directories
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "video2subs"
DEFAULT_MODEL_DIR = DEFAULT_CACHE_DIR / "models"
DEFAULT_TEMP_DIR = DEFAULT_CACHE_DIR / "temp"

# Audio processing settings
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_FORMAT = "wav"

# Supported video extensions
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm", ".m4v"}

# Supported audio extensions
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}

# Default whisper model
DEFAULT_MODEL = "base"
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]

# Model size info (approximate)
MODEL_SIZE_INFO = {
    "tiny": "~75 MB, fastest, lowest accuracy",
    "base": "~145 MB, fast, good for most cases",
    "small": "~465 MB, balanced speed/accuracy",
    "medium": "~1.5 GB, slower, better accuracy",
    "large-v2": "~3 GB, slowest, best accuracy",
    "large-v3": "~3 GB, slowest, best accuracy (latest)",
}


def get_cache_dir() -> Path:
    """Get cache directory, create if not exists"""
    cache_dir = Path(os.environ.get("VIDEO2SUBS_CACHE_DIR", DEFAULT_CACHE_DIR))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_model_dir() -> Path:
    """Get model directory, create if not exists"""
    model_dir = Path(os.environ.get("VIDEO2SUBS_MODEL_DIR", DEFAULT_MODEL_DIR))
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir


def get_temp_dir() -> Path:
    """Get temporary directory, create if not exists"""
    temp_dir = Path(os.environ.get("VIDEO2SUBS_TEMP_DIR", DEFAULT_TEMP_DIR))
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def cleanup_temp_dir():
    """Clean up temporary directory"""
    temp_dir = get_temp_dir()
    if temp_dir.exists():
        import shutil
        for item in temp_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
