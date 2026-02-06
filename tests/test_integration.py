"""Integration tests"""

import pytest

# Skip these tests if running in CI without models
pytestmark = pytest.mark.skip(
    reason="Integration tests require large model downloads. Run manually with: pytest -m integration"
)


@pytest.mark.integration
def test_full_transcription_pipeline(sample_audio, temp_dir):
    """Test complete transcription pipeline"""
    from video2subs.transcribe import transcribe_video
    
    result = transcribe_video(
        source=str(sample_audio),
        output_dir=str(temp_dir),
        output_name="test_output",
        model="tiny",  # Use smallest model for testing
        language=None,
        device="cpu",
        use_yt_dlp=False,
        vad_filter=False,
        cleanup=True,
        log_level="DEBUG",
    )
    
    # Check result structure
    assert result is not None
    assert hasattr(result, "segments")
    assert hasattr(result, "output_files")
    assert hasattr(result, "metadata")
    
    # Check output files exist
    assert result.output_files["srt"].exists()
    assert result.output_files["json"].exists()
    assert result.output_files["txt"].exists()
    
    # Check metadata
    assert result.metadata["model"] == "tiny"
    assert result.metadata["segment_count"] >= 0
