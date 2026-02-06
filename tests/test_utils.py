"""Tests for utility functions"""

import pytest

from video2subs.utils import format_timestamp, is_url, sanitize_filename


def test_is_url():
    """Test URL detection"""
    assert is_url("https://example.com/video.mp4") is True
    assert is_url("http://example.com/video.mp4") is True
    assert is_url("ftp://example.com/video.mp4") is True
    assert is_url("/path/to/video.mp4") is False
    assert is_url("video.mp4") is False


def test_format_timestamp():
    """Test SRT timestamp formatting"""
    assert format_timestamp(0.0) == "00:00:00,000"
    assert format_timestamp(1.5) == "00:00:01,500"
    assert format_timestamp(61.234) == "00:01:01,234"
    assert format_timestamp(3661.567) == "01:01:01,567"
    assert format_timestamp(0.999) == "00:00:00,999"


def test_sanitize_filename():
    """Test filename sanitization"""
    assert sanitize_filename("normal_file.mp4") == "normal_file.mp4"
    assert sanitize_filename("file:with:colons.mp4") == "file_with_colons.mp4"
    assert sanitize_filename('file<with>invalid"chars.mp4') == "file_with_invalid_chars.mp4"
    assert sanitize_filename("file/with\\slashes.mp4") == "file_with_slashes.mp4"
