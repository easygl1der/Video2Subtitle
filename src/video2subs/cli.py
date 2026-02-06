"""
Command-line interface for video2subs
"""

import sys
from pathlib import Path

import click

from . import __version__
from .config import AVAILABLE_MODELS, DEFAULT_MODEL, MODEL_SIZE_INFO
from .transcribe import transcribe_video


@click.group()
@click.version_option(version=__version__, prog_name="video2subs")
def cli():
    """video2subs - Offline video to subtitles converter"""
    pass


@cli.command()
@click.argument("source", type=str)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Output directory (default: ./output)",
)
@click.option(
    "--name",
    "-n",
    type=str,
    default="output",
    help="Base name for output files (default: output)",
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(AVAILABLE_MODELS),
    default=DEFAULT_MODEL,
    help=f"Whisper model to use (default: {DEFAULT_MODEL})",
)
@click.option(
    "--language",
    "-l",
    type=str,
    default=None,
    help="Language code (e.g., en, zh, ja). Auto-detect if not specified",
)
@click.option(
    "--device",
    "-d",
    type=click.Choice(["auto", "cpu", "cuda"]),
    default="auto",
    help="Device to use for inference (default: auto)",
)
@click.option(
    "--no-ytdlp",
    is_flag=True,
    default=False,
    help="Disable yt-dlp for video downloading",
)
@click.option(
    "--vad",
    is_flag=True,
    default=False,
    help="Enable Voice Activity Detection (filters silence)",
)
@click.option(
    "--no-cleanup",
    is_flag=True,
    default=False,
    help="Keep temporary files after processing",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable verbose logging",
)
def transcribe(
    source: str,
    output: str,
    name: str,
    model: str,
    language: str,
    device: str,
    no_ytdlp: bool,
    vad: bool,
    no_cleanup: bool,
    verbose: bool,
):
    """
    Transcribe video/audio to subtitles
    
    SOURCE can be:
    - Local file path (e.g., ./video.mp4)
    - Direct URL (e.g., https://example.com/video.mp4)
    - Video site URL (e.g., YouTube URL, requires yt-dlp)
    
    Examples:
    
      # Transcribe local video
      video2subs transcribe ./sample.mp4
    
      # Transcribe with Chinese language and small model
      video2subs transcribe ./video.mp4 -l zh -m small
    
      # Transcribe from URL with custom output
      video2subs transcribe https://example.com/video.mp4 -o ./my_subs -n my_video
    
      # Use GPU acceleration
      video2subs transcribe ./video.mp4 -d cuda -m medium
    """
    try:
        log_level = "DEBUG" if verbose else "INFO"
        
        result = transcribe_video(
            source=source,
            output_dir=output,
            output_name=name,
            model=model,
            language=language,
            device=device,
            use_yt_dlp=not no_ytdlp,
            vad_filter=vad,
            cleanup=not no_cleanup,
            log_level=log_level,
        )
        
        click.echo("\n✓ Transcription completed successfully!")
        click.echo(f"\nGenerated {len(result.segments)} subtitle segments")
        click.echo("\nOutput files:")
        for format_name, file_path in result.output_files.items():
            click.echo(f"  • {format_name.upper()}: {file_path}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        click.echo("\n\nTranscription cancelled by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def models():
    """List available Whisper models and their information"""
    click.echo("Available Whisper Models:\n")
    for model_name in AVAILABLE_MODELS:
        info = MODEL_SIZE_INFO.get(model_name, "No info available")
        marker = " (default)" if model_name == DEFAULT_MODEL else ""
        click.echo(f"  • {model_name}{marker}")
        click.echo(f"    {info}\n")


@cli.command()
def info():
    """Show system and configuration information"""
    import platform
    
    import torch
    
    from .config import get_cache_dir, get_model_dir, get_temp_dir
    
    click.echo("System Information:")
    click.echo(f"  • Python: {platform.python_version()}")
    click.echo(f"  • Platform: {platform.system()} {platform.release()}")
    click.echo(f"\nCUDA Information:")
    click.echo(f"  • CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        click.echo(f"  • CUDA version: {torch.version.cuda}")
        click.echo(f"  • GPU count: {torch.cuda.device_count()}")
        click.echo(f"  • GPU name: {torch.cuda.get_device_name(0)}")
    
    click.echo(f"\nConfiguration:")
    click.echo(f"  • Cache directory: {get_cache_dir()}")
    click.echo(f"  • Model directory: {get_model_dir()}")
    click.echo(f"  • Temp directory: {get_temp_dir()}")
    
    # Check dependencies
    click.echo(f"\nDependencies:")
    try:
        import ffmpeg
        click.echo(f"  • ffmpeg-python: ✓ installed")
    except ImportError:
        click.echo(f"  • ffmpeg-python: ✗ not installed")
    
    try:
        import yt_dlp
        click.echo(f"  • yt-dlp: ✓ installed")
    except ImportError:
        click.echo(f"  • yt-dlp: ✗ not installed")
    
    try:
        import faster_whisper
        click.echo(f"  • faster-whisper: ✓ installed")
    except ImportError:
        click.echo(f"  • faster-whisper: ✗ not installed")


@cli.command()
@click.option(
    "--all",
    "cleanup_all",
    is_flag=True,
    default=False,
    help="Clean up all cache including models",
)
def cleanup(cleanup_all: bool):
    """Clean up temporary files and cache"""
    from .config import cleanup_temp_dir, get_cache_dir, get_temp_dir
    
    try:
        # Always cleanup temp directory
        temp_dir = get_temp_dir()
        cleanup_temp_dir()
        click.echo(f"✓ Cleaned up temporary directory: {temp_dir}")
        
        if cleanup_all:
            import shutil
            cache_dir = get_cache_dir()
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                click.echo(f"✓ Removed cache directory: {cache_dir}")
        else:
            click.echo("\nTo remove all cache including models, use: video2subs cleanup --all")
            
    except Exception as e:
        click.echo(f"✗ Error during cleanup: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for CLI"""
    cli()


if __name__ == "__main__":
    main()
