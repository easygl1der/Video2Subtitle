"""
Main transcription workflow
"""

import logging
from pathlib import Path
from typing import List, Optional

from .asr_engine import ASREngine, TranscriptionSegment
from .audio_processor import AudioProcessor
from .config import DEFAULT_MODEL
from .downloader import MediaDownloader
from .exporters import SubtitleExporter
from .utils import ensure_output_dir, setup_logging

logger = logging.getLogger(__name__)


class TranscriptionResult:
    """Container for transcription results"""

    def __init__(
        self,
        segments: List[TranscriptionSegment],
        output_files: dict,
        metadata: dict,
    ):
        self.segments = segments
        self.output_files = output_files
        self.metadata = metadata

    def __repr__(self) -> str:
        return (
            f"TranscriptionResult("
            f"segments={len(self.segments)}, "
            f"files={list(self.output_files.keys())})"
        )


def transcribe_video(
    source: str,
    output_dir: Optional[str] = None,
    output_name: str = "output",
    model: str = DEFAULT_MODEL,
    language: Optional[str] = None,
    device: str = "auto",
    use_yt_dlp: bool = True,
    vad_filter: bool = False,
    cleanup: bool = True,
    log_level: str = "INFO",
) -> TranscriptionResult:
    """
    Main function to transcribe video/audio to subtitles
    
    Args:
        source: Video/audio URL or local file path
        output_dir: Output directory for subtitle files
        output_name: Base name for output files (without extension)
        model: Whisper model name (tiny, base, small, medium, large-v2, large-v3)
        language: Language code (e.g., "en", "zh"). None for auto-detection
        device: Device to use ("cpu", "cuda", "auto")
        use_yt_dlp: Use yt-dlp for downloading from video sites
        vad_filter: Enable Voice Activity Detection
        cleanup: Clean up temporary files after processing
        log_level: Logging level
        
    Returns:
        TranscriptionResult object with segments and output file paths
    """
    # Setup logging
    setup_logging(log_level)
    logger.info("=" * 60)
    logger.info("Starting video-to-subtitles transcription")
    logger.info("=" * 60)
    logger.info(f"Source: {source}")
    logger.info(f"Model: {model}")
    logger.info(f"Language: {language or 'auto-detect'}")
    logger.info(f"Device: {device}")
    
    # Prepare output directory
    if output_dir is None:
        output_dir = Path.cwd() / "output"
    output_dir = ensure_output_dir(Path(output_dir))
    logger.info(f"Output directory: {output_dir}")

    # Temporary files to cleanup
    temp_files = []

    try:
        # Step 1: Download/get media file
        logger.info("\n[Step 1/4] Getting media file...")
        downloader = MediaDownloader(use_yt_dlp=use_yt_dlp)
        media_path, is_temp = downloader.get_media(source)
        if is_temp:
            temp_files.append(media_path)
        logger.info(f"Media file: {media_path}")

        # Step 2: Extract and normalize audio
        logger.info("\n[Step 2/4] Extracting audio...")
        processor = AudioProcessor()
        audio_path = processor.extract_audio(media_path)
        temp_files.append(audio_path)
        
        # Get audio info
        audio_info = processor.get_audio_info(audio_path)
        logger.info(f"Audio duration: {audio_info['duration']:.2f} seconds")

        # Step 3: Run ASR transcription
        logger.info("\n[Step 3/4] Running ASR transcription...")
        asr_engine = ASREngine(model_name=model, device=device)
        segments = asr_engine.transcribe(
            audio_path,
            language=language,
            vad_filter=vad_filter,
        )
        
        if not segments:
            logger.warning("No speech detected in audio!")
            segments = []

        # Step 4: Export to subtitle formats
        logger.info("\n[Step 4/4] Exporting subtitles...")
        output_files = SubtitleExporter.export_all(
            segments, output_dir, output_name
        )

        # Collect metadata
        metadata = {
            "source": source,
            "model": model,
            "language": language,
            "device": device,
            "audio_duration": audio_info["duration"],
            "segment_count": len(segments),
        }

        logger.info("\n" + "=" * 60)
        logger.info("Transcription completed successfully!")
        logger.info("=" * 60)
        logger.info(f"Total segments: {len(segments)}")
        logger.info("Output files:")
        for format_name, file_path in output_files.items():
            logger.info(f"  - {format_name.upper()}: {file_path}")

        return TranscriptionResult(
            segments=segments,
            output_files=output_files,
            metadata=metadata,
        )

    except Exception as e:
        logger.error(f"\nTranscription failed: {e}", exc_info=True)
        raise

    finally:
        # Cleanup temporary files
        if cleanup and temp_files:
            logger.info("\nCleaning up temporary files...")
            for temp_file in temp_files:
                try:
                    if temp_file.exists():
                        temp_file.unlink()
                        logger.debug(f"Removed: {temp_file}")
                except Exception as e:
                    logger.warning(f"Failed to remove {temp_file}: {e}")
