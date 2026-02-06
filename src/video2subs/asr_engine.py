"""
ASR (Automatic Speech Recognition) engine using faster-whisper
"""

import logging
from pathlib import Path
from typing import Iterator, List, Optional

from faster_whisper import WhisperModel

from .config import DEFAULT_MODEL, get_model_dir

logger = logging.getLogger(__name__)


class TranscriptionSegment:
    """Represents a transcription segment with timing and text"""

    def __init__(
        self,
        start: float,
        end: float,
        text: str,
        index: int = 0,
    ):
        self.start = start
        self.end = end
        self.text = text.strip()
        self.index = index

    @property
    def duration(self) -> float:
        """Duration of the segment in seconds"""
        return self.end - self.start

    @property
    def char_len(self) -> int:
        """Character length of the text"""
        return len(self.text)

    @property
    def word_len(self) -> int:
        """Word count (approximation for Chinese/English mixed text)"""
        # Simple word count: split by spaces for English, count chars for CJK
        words = self.text.split()
        # Count CJK characters separately
        cjk_chars = sum(1 for char in self.text if "\u4e00" <= char <= "\u9fff")
        return len(words) + cjk_chars

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "index": self.index,
            "start": round(self.start, 3),
            "end": round(self.end, 3),
            "text": self.text,
            "char_len": self.char_len,
            "word_len": self.word_len,
        }

    def __repr__(self) -> str:
        return f"Segment({self.start:.2f}s - {self.end:.2f}s: {self.text[:30]}...)"


class ASREngine:
    """ASR engine using faster-whisper for offline transcription"""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str = "auto",
        compute_type: str = "auto",
        download_root: Optional[Path] = None,
    ):
        """
        Initialize ASR engine
        
        Args:
            model_name: Whisper model name (tiny, base, small, medium, large-v2, large-v3)
            device: Device to use ("cpu", "cuda", or "auto")
            compute_type: Computation type ("int8", "float16", "float32", or "auto")
            download_root: Directory to store models
        """
        self.model_name = model_name
        
        # Auto-detect device
        if device == "auto":
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Auto-detected device: {device}")
        
        self.device = device
        
        # Auto-select compute type based on device
        if compute_type == "auto":
            if device == "cuda":
                compute_type = "float16"  # Best for GPU
            else:
                compute_type = "int8"  # Best for CPU
            logger.info(f"Auto-selected compute type: {compute_type}")
        
        self.compute_type = compute_type
        
        # Set model download directory
        if download_root is None:
            download_root = get_model_dir()
        self.download_root = download_root
        
        logger.info(f"Initializing faster-whisper model: {model_name}")
        logger.info(f"Device: {device}, Compute type: {compute_type}")
        logger.info(f"Model cache directory: {download_root}")
        
        # Load model
        try:
            self.model = WhisperModel(
                model_name,
                device=device,
                compute_type=compute_type,
                download_root=str(download_root),
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model: {e}") from e

    def transcribe(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        initial_prompt: Optional[str] = None,
        vad_filter: bool = False,
        vad_parameters: Optional[dict] = None,
    ) -> List[TranscriptionSegment]:
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to audio file (WAV, 16kHz recommended)
            language: Language code (e.g., "en", "zh", "ja"). None for auto-detection
            initial_prompt: Optional prompt to guide the transcription
            vad_filter: Enable Voice Activity Detection to filter out silence
            vad_parameters: VAD parameters (threshold, min_speech_duration, etc.)
            
        Returns:
            List of TranscriptionSegment objects
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info(f"Transcribing audio: {audio_path.name}")
        if language:
            logger.info(f"Language: {language}")
        else:
            logger.info("Language: auto-detect")

        try:
            segments, info = self.model.transcribe(
                str(audio_path),
                language=language,
                initial_prompt=initial_prompt,
                vad_filter=vad_filter,
                vad_parameters=vad_parameters,
                beam_size=5,
                word_timestamps=False,  # Set to True if word-level timestamps needed
            )

            # Convert to list and create TranscriptionSegment objects
            result_segments = []
            for idx, segment in enumerate(segments):
                result_segments.append(
                    TranscriptionSegment(
                        start=segment.start,
                        end=segment.end,
                        text=segment.text,
                        index=idx + 1,
                    )
                )

            logger.info(f"Transcription completed: {len(result_segments)} segments")
            logger.info(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")
            
            # Validate and fix timestamps
            result_segments = self._validate_timestamps(result_segments)
            
            return result_segments

        except Exception as e:
            raise RuntimeError(f"Transcription failed: {e}") from e

    def _validate_timestamps(
        self, segments: List[TranscriptionSegment]
    ) -> List[TranscriptionSegment]:
        """
        Validate and ensure timestamps are monotonically increasing
        
        Args:
            segments: List of segments
            
        Returns:
            Validated segments
        """
        if not segments:
            return segments

        # Check for monotonicity and fix if needed
        for i in range(1, len(segments)):
            if segments[i].start < segments[i - 1].end:
                logger.warning(
                    f"Segment {i} start time ({segments[i].start:.2f}s) "
                    f"is before previous end ({segments[i - 1].end:.2f}s), adjusting..."
                )
                segments[i].start = segments[i - 1].end

            if segments[i].end <= segments[i].start:
                logger.warning(
                    f"Segment {i} end time <= start time, adjusting..."
                )
                segments[i].end = segments[i].start + 0.1  # Minimum 100ms duration

        return segments

    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "compute_type": self.compute_type,
            "download_root": str(self.download_root),
        }
