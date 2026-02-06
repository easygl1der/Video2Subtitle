"""
Utility functions for video2subs
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger("video2subs")


def is_url(path: str) -> bool:
    """Check if the given path is a URL"""
    return path.startswith(("http://", "https://", "ftp://"))


def is_video_file(path: Path) -> bool:
    """Check if the file is a video file based on extension"""
    from .config import VIDEO_EXTENSIONS, AUDIO_EXTENSIONS
    return path.suffix.lower() in VIDEO_EXTENSIONS or path.suffix.lower() in AUDIO_EXTENSIONS


def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def sanitize_filename(name: str) -> str:
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "_")
    return name[:255]  # Limit filename length


def ensure_output_dir(output_path: Optional[Path] = None) -> Path:
    """Ensure output directory exists"""
    if output_path is None:
        output_path = Path.cwd() / "output"
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
