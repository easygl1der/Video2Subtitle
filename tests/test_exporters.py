"""Tests for subtitle exporters"""

import json

import pytest

from video2subs.asr_engine import TranscriptionSegment
from video2subs.exporters import SubtitleExporter


@pytest.fixture
def sample_segments():
    """Create sample transcription segments"""
    return [
        TranscriptionSegment(start=0.0, end=2.5, text="Hello world", index=1),
        TranscriptionSegment(start=2.5, end=5.0, text="This is a test", index=2),
        TranscriptionSegment(start=5.0, end=7.5, text="中文测试", index=3),
    ]


def test_export_srt(sample_segments, temp_dir):
    """Test SRT export"""
    output_path = temp_dir / "test.srt"
    SubtitleExporter.export_srt(sample_segments, output_path)
    
    assert output_path.exists()
    
    content = output_path.read_text(encoding="utf-8")
    
    # Check structure
    assert "1\n" in content
    assert "00:00:00,000 --> 00:00:02,500" in content
    assert "Hello world" in content
    
    assert "2\n" in content
    assert "00:00:02,500 --> 00:00:05,000" in content
    assert "This is a test" in content
    
    assert "3\n" in content
    assert "中文测试" in content


def test_export_json(sample_segments, temp_dir):
    """Test JSON export"""
    output_path = temp_dir / "test.json"
    SubtitleExporter.export_json(sample_segments, output_path)
    
    assert output_path.exists()
    
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "segments" in data
    assert "metadata" in data
    
    assert len(data["segments"]) == 3
    
    # Check first segment
    seg1 = data["segments"][0]
    assert seg1["index"] == 1
    assert seg1["start"] == 0.0
    assert seg1["end"] == 2.5
    assert seg1["text"] == "Hello world"
    assert seg1["char_len"] == len("Hello world")
    assert "word_len" in seg1
    
    # Check metadata
    assert data["metadata"]["total_segments"] == 3
    assert data["metadata"]["total_duration"] == 7.5


def test_export_txt(sample_segments, temp_dir):
    """Test TXT export"""
    output_path = temp_dir / "test.txt"
    SubtitleExporter.export_txt(sample_segments, output_path)
    
    assert output_path.exists()
    
    content = output_path.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    
    assert len(lines) == 3
    assert lines[0] == "Hello world"
    assert lines[1] == "This is a test"
    assert lines[2] == "中文测试"


def test_export_all(sample_segments, temp_dir):
    """Test exporting all formats"""
    output_files = SubtitleExporter.export_all(
        sample_segments, temp_dir, "output"
    )
    
    assert "srt" in output_files
    assert "json" in output_files
    assert "txt" in output_files
    
    assert output_files["srt"].exists()
    assert output_files["json"].exists()
    assert output_files["txt"].exists()


def test_timestamp_monotonicity():
    """Test that segment timestamps are validated"""
    # This is tested in ASR engine, but we verify the segments structure
    seg1 = TranscriptionSegment(start=0.0, end=2.0, text="First")
    seg2 = TranscriptionSegment(start=2.0, end=4.0, text="Second")
    
    assert seg2.start >= seg1.end
    assert seg2.end > seg2.start


def test_segment_properties():
    """Test TranscriptionSegment properties"""
    seg = TranscriptionSegment(start=1.0, end=3.5, text="Hello 世界", index=1)
    
    assert seg.duration == 2.5
    assert seg.char_len == len("Hello 世界")
    assert seg.word_len > 0
    
    seg_dict = seg.to_dict()
    assert seg_dict["start"] == 1.0
    assert seg_dict["end"] == 3.5
    assert seg_dict["text"] == "Hello 世界"
