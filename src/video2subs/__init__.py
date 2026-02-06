"""
video2subs: Offline video to subtitles converter
"""

__version__ = "0.1.0"

from .transcribe import transcribe_video

__all__ = ["transcribe_video", "__version__"]
