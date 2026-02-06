"""
Audio processing module using FFmpeg
"""

import logging
import subprocess
from pathlib import Path
from typing import Optional

import ffmpeg

from .config import AUDIO_CHANNELS, AUDIO_FORMAT, AUDIO_SAMPLE_RATE, get_temp_dir

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Process audio/video files to extract and normalize audio for ASR"""

    def __init__(self):
        self.temp_dir = get_temp_dir()
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """Check if ffmpeg is available"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True,
                timeout=5,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(
                "FFmpeg is not installed or not in PATH. "
                "Please install FFmpeg: https://ffmpeg.org/download.html"
            ) from e

    def extract_audio(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Extract and normalize audio from video/audio file
        
        Converts to:
        - Sample rate: 16kHz (required by Whisper)
        - Channels: mono (1 channel)
        - Format: WAV PCM
        
        Args:
            input_path: Path to input video/audio file
            output_path: Path for output audio file (optional)
            
        Returns:
            Path to extracted audio file
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Generate output path if not provided
        if output_path is None:
            output_filename = f"{input_path.stem}_audio.{AUDIO_FORMAT}"
            output_path = self.temp_dir / output_filename

        logger.info(f"Extracting audio from {input_path.name}...")
        logger.info(
            f"Target format: {AUDIO_SAMPLE_RATE}Hz, {AUDIO_CHANNELS} channel(s), {AUDIO_FORMAT.upper()}"
        )

        try:
            # Use ffmpeg-python for cleaner API
            stream = ffmpeg.input(str(input_path))
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec="pcm_s16le",  # PCM 16-bit
                ac=AUDIO_CHANNELS,    # Mono
                ar=AUDIO_SAMPLE_RATE, # 16kHz
                format=AUDIO_FORMAT,
                loglevel="error",
            )
            
            # Overwrite output file if exists
            stream = ffmpeg.overwrite_output(stream)
            
            # Run the conversion
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"FFmpeg processing failed: {error_msg}") from e

        if not output_path.exists():
            raise RuntimeError(f"Audio extraction failed: output file not created")

        file_size = output_path.stat().st_size
        logger.info(f"Audio extracted successfully: {output_path.name} ({file_size / 1024:.1f} KB)")
        
        return output_path

    def get_audio_info(self, audio_path: Path) -> dict:
        """
        Get audio file information
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with audio info
        """
        try:
            probe = ffmpeg.probe(str(audio_path))
            audio_stream = next(
                (s for s in probe["streams"] if s["codec_type"] == "audio"),
                None,
            )
            
            if audio_stream is None:
                raise ValueError("No audio stream found in file")
            
            return {
                "duration": float(probe["format"].get("duration", 0)),
                "sample_rate": int(audio_stream.get("sample_rate", 0)),
                "channels": int(audio_stream.get("channels", 0)),
                "codec": audio_stream.get("codec_name", "unknown"),
                "bit_rate": int(audio_stream.get("bit_rate", 0)),
            }
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"Failed to get audio info: {error_msg}") from e

    def cleanup(self, path: Path):
        """Remove temporary audio file"""
        if path.exists() and path.parent == self.temp_dir:
            try:
                path.unlink()
                logger.debug(f"Cleaned up audio file: {path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {path}: {e}")
