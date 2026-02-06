"""
Export transcription results to various formats (SRT, JSON, TXT)
"""

import json
import logging
from pathlib import Path
from typing import List

from .asr_engine import TranscriptionSegment
from .utils import format_timestamp

logger = logging.getLogger(__name__)


class SubtitleExporter:
    """Export transcription segments to various subtitle formats"""

    @staticmethod
    def export_srt(segments: List[TranscriptionSegment], output_path: Path):
        """
        Export segments to SRT (SubRip) format
        
        SRT format:
        1
        00:00:00,000 --> 00:00:02,500
        First subtitle text
        
        2
        00:00:02,500 --> 00:00:05,000
        Second subtitle text
        
        Args:
            segments: List of TranscriptionSegment objects
            output_path: Path to output SRT file
        """
        logger.info(f"Exporting to SRT format: {output_path}")
        
        with open(output_path, "w", encoding="utf-8") as f:
            for segment in segments:
                # Segment index
                f.write(f"{segment.index}\n")
                
                # Timestamps
                start_time = format_timestamp(segment.start)
                end_time = format_timestamp(segment.end)
                f.write(f"{start_time} --> {end_time}\n")
                
                # Text
                f.write(f"{segment.text}\n")
                
                # Blank line separator
                f.write("\n")
        
        logger.info(f"SRT exported successfully: {len(segments)} segments")

    @staticmethod
    def export_json(segments: List[TranscriptionSegment], output_path: Path):
        """
        Export segments to JSON format
        
        JSON format:
        {
            "segments": [
                {
                    "index": 1,
                    "start": 0.0,
                    "end": 2.5,
                    "text": "First subtitle text",
                    "char_len": 19,
                    "word_len": 3
                },
                ...
            ],
            "metadata": {
                "total_segments": 10,
                "total_duration": 120.5
            }
        }
        
        Args:
            segments: List of TranscriptionSegment objects
            output_path: Path to output JSON file
        """
        logger.info(f"Exporting to JSON format: {output_path}")
        
        # Convert segments to dictionaries
        segments_data = [seg.to_dict() for seg in segments]
        
        # Calculate metadata
        total_duration = segments[-1].end if segments else 0.0
        total_chars = sum(seg.char_len for seg in segments)
        
        output_data = {
            "segments": segments_data,
            "metadata": {
                "total_segments": len(segments),
                "total_duration": round(total_duration, 3),
                "total_chars": total_chars,
            },
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON exported successfully: {len(segments)} segments")

    @staticmethod
    def export_txt(segments: List[TranscriptionSegment], output_path: Path):
        """
        Export segments to plain text format
        
        Plain text format (one line per segment):
        First subtitle text
        Second subtitle text
        ...
        
        Args:
            segments: List of TranscriptionSegment objects
            output_path: Path to output TXT file
        """
        logger.info(f"Exporting to TXT format: {output_path}")
        
        with open(output_path, "w", encoding="utf-8") as f:
            for segment in segments:
                f.write(f"{segment.text}\n")
        
        logger.info(f"TXT exported successfully: {len(segments)} segments")

    @staticmethod
    def export_all(
        segments: List[TranscriptionSegment],
        output_dir: Path,
        base_name: str = "output",
    ):
        """
        Export segments to all formats (SRT, JSON, TXT)
        
        Args:
            segments: List of TranscriptionSegment objects
            output_dir: Directory to save output files
            base_name: Base name for output files (without extension)
            
        Returns:
            Dictionary with paths to exported files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        srt_path = output_dir / f"{base_name}.srt"
        json_path = output_dir / f"{base_name}.json"
        txt_path = output_dir / f"{base_name}.txt"
        
        SubtitleExporter.export_srt(segments, srt_path)
        SubtitleExporter.export_json(segments, json_path)
        SubtitleExporter.export_txt(segments, txt_path)
        
        return {
            "srt": srt_path,
            "json": json_path,
            "txt": txt_path,
        }


class VTTExporter:
    """Export to WebVTT format (optional, for web players)"""

    @staticmethod
    def export_vtt(segments: List[TranscriptionSegment], output_path: Path):
        """
        Export segments to WebVTT format
        
        WebVTT format:
        WEBVTT
        
        00:00:00.000 --> 00:00:02.500
        First subtitle text
        
        00:00:02.500 --> 00:00:05.000
        Second subtitle text
        
        Args:
            segments: List of TranscriptionSegment objects
            output_path: Path to output VTT file
        """
        logger.info(f"Exporting to WebVTT format: {output_path}")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            
            for segment in segments:
                # Timestamps (VTT uses dots instead of commas)
                start_time = format_timestamp(segment.start).replace(",", ".")
                end_time = format_timestamp(segment.end).replace(",", ".")
                f.write(f"{start_time} --> {end_time}\n")
                
                # Text
                f.write(f"{segment.text}\n\n")
        
        logger.info(f"WebVTT exported successfully: {len(segments)} segments")
