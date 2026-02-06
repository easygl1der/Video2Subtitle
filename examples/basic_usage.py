#!/usr/bin/env python3
"""
Basic usage examples for video2subs
"""

from pathlib import Path

from video2subs import transcribe_video


def example_local_file():
    """Example: Transcribe a local video file"""
    print("Example 1: Transcribe local file")
    print("-" * 50)
    
    result = transcribe_video(
        source="./sample.mp4",
        output_dir="./output",
        output_name="my_subtitles",
        model="base",
        language="en",
        device="auto",
    )
    
    print(f"Generated {len(result.segments)} segments")
    print(f"Output files: {result.output_files}")
    print()


def example_with_url():
    """Example: Transcribe from URL"""
    print("Example 2: Transcribe from URL")
    print("-" * 50)
    
    result = transcribe_video(
        source="https://example.com/video.mp4",
        output_dir="./output",
        model="small",
        language="zh",
        use_yt_dlp=True,
    )
    
    # Access segments
    for i, seg in enumerate(result.segments[:3]):  # First 3 segments
        print(f"Segment {i+1}: [{seg.start:.2f}s - {seg.end:.2f}s] {seg.text}")
    print()


def example_chinese_video():
    """Example: Transcribe Chinese video with VAD"""
    print("Example 3: Chinese video with VAD")
    print("-" * 50)
    
    result = transcribe_video(
        source="./chinese_video.mp4",
        output_dir="./output",
        output_name="chinese_subs",
        model="medium",
        language="zh",
        device="cuda",  # Use GPU if available
        vad_filter=True,  # Enable VAD to filter silence
    )
    
    print(f"Total duration: {result.metadata['audio_duration']:.2f}s")
    print(f"Total segments: {result.metadata['segment_count']}")
    print()


def example_iterate_segments():
    """Example: Process segments programmatically"""
    print("Example 4: Process segments")
    print("-" * 50)
    
    result = transcribe_video(
        source="./video.mp4",
        output_dir="./output",
        model="base",
    )
    
    # Calculate statistics
    total_chars = sum(seg.char_len for seg in result.segments)
    avg_duration = sum(seg.duration for seg in result.segments) / len(result.segments)
    
    print(f"Total characters: {total_chars}")
    print(f"Average segment duration: {avg_duration:.2f}s")
    
    # Find long segments
    long_segments = [seg for seg in result.segments if seg.duration > 5.0]
    print(f"Segments longer than 5s: {len(long_segments)}")
    print()


def example_custom_output():
    """Example: Custom output handling"""
    print("Example 5: Custom output handling")
    print("-" * 50)
    
    result = transcribe_video(
        source="./video.mp4",
        output_dir="./output",
        model="base",
    )
    
    # Read and process JSON output
    import json
    json_path = result.output_files["json"]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Metadata: {data['metadata']}")
    print(f"First segment: {data['segments'][0]}")
    print()


if __name__ == "__main__":
    # Run examples (comment out as needed)
    
    # example_local_file()
    # example_with_url()
    # example_chinese_video()
    # example_iterate_segments()
    # example_custom_output()
    
    print("Examples ready to run!")
    print("Uncomment the example functions you want to test.")
