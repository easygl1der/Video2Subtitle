"""
HTTP API server for video2subs using FastAPI
"""

import logging
import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from . import __version__
from .config import AVAILABLE_MODELS, DEFAULT_MODEL
from .transcribe import transcribe_video

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="video2subs API",
    description="Offline video to subtitles transcription API",
    version=__version__,
)


# Pydantic models for API
class TranscribeURLRequest(BaseModel):
    """Request model for URL-based transcription"""
    url: str = Field(..., description="Video/audio URL")
    model: str = Field(DEFAULT_MODEL, description="Whisper model name")
    language: Optional[str] = Field(None, description="Language code (e.g., en, zh)")
    device: str = Field("auto", description="Device: auto, cpu, or cuda")
    vad_filter: bool = Field(False, description="Enable Voice Activity Detection")
    use_yt_dlp: bool = Field(True, description="Use yt-dlp for video sites")


class SegmentResponse(BaseModel):
    """Response model for a transcription segment"""
    index: int
    start: float
    end: float
    text: str
    char_len: int
    word_len: int


class TranscribeResponse(BaseModel):
    """Response model for transcription result"""
    success: bool
    segments: List[SegmentResponse]
    metadata: dict


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "video2subs API",
        "version": __version__,
        "status": "running",
        "endpoints": {
            "transcribe_url": "/transcribe/url",
            "transcribe_file": "/transcribe/file",
            "health": "/health",
            "models": "/models",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/models")
async def list_models():
    """List available Whisper models"""
    from .config import MODEL_SIZE_INFO
    
    models = []
    for model_name in AVAILABLE_MODELS:
        models.append({
            "name": model_name,
            "info": MODEL_SIZE_INFO.get(model_name, ""),
            "is_default": model_name == DEFAULT_MODEL,
        })
    
    return {"models": models}


@app.post("/transcribe/url", response_model=TranscribeResponse)
async def transcribe_from_url(request: TranscribeURLRequest):
    """
    Transcribe video/audio from URL
    
    Example:
    ```
    POST /transcribe/url
    {
        "url": "https://example.com/video.mp4",
        "model": "base",
        "language": "en"
    }
    ```
    """
    try:
        logger.info(f"Received transcription request for URL: {request.url}")
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_output_dir:
            result = transcribe_video(
                source=request.url,
                output_dir=temp_output_dir,
                output_name="transcription",
                model=request.model,
                language=request.language,
                device=request.device,
                use_yt_dlp=request.use_yt_dlp,
                vad_filter=request.vad_filter,
                cleanup=True,
                log_level="INFO",
            )
            
            # Convert segments to response format
            segments = [
                SegmentResponse(**seg.to_dict()) for seg in result.segments
            ]
            
            return TranscribeResponse(
                success=True,
                segments=segments,
                metadata=result.metadata,
            )
    
    except Exception as e:
        logger.error(f"Transcription failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transcribe/file", response_model=TranscribeResponse)
async def transcribe_from_file(
    file: UploadFile = File(..., description="Video/audio file to transcribe"),
    model: str = Form(DEFAULT_MODEL, description="Whisper model name"),
    language: Optional[str] = Form(None, description="Language code"),
    device: str = Form("auto", description="Device: auto, cpu, or cuda"),
    vad_filter: bool = Form(False, description="Enable VAD"),
):
    """
    Transcribe uploaded video/audio file
    
    Example using curl:
    ```
    curl -X POST "http://localhost:8000/transcribe/file" \\
         -F "file=@video.mp4" \\
         -F "model=base" \\
         -F "language=en"
    ```
    """
    try:
        logger.info(f"Received transcription request for file: {file.filename}")
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Create temporary output directory
            with tempfile.TemporaryDirectory() as temp_output_dir:
                result = transcribe_video(
                    source=temp_file_path,
                    output_dir=temp_output_dir,
                    output_name="transcription",
                    model=model,
                    language=language,
                    device=device,
                    use_yt_dlp=False,
                    vad_filter=vad_filter,
                    cleanup=True,
                    log_level="INFO",
                )
                
                # Convert segments to response format
                segments = [
                    SegmentResponse(**seg.to_dict()) for seg in result.segments
                ]
                
                return TranscribeResponse(
                    success=True,
                    segments=segments,
                    metadata=result.metadata,
                )
        
        finally:
            # Clean up uploaded file
            Path(temp_file_path).unlink(missing_ok=True)
    
    except Exception as e:
        logger.error(f"Transcription failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transcribe/file/download")
async def transcribe_and_download(
    file: UploadFile = File(...),
    model: str = Form(DEFAULT_MODEL),
    language: Optional[str] = Form(None),
    device: str = Form("auto"),
    format: str = Form("srt", description="Output format: srt, json, or txt"),
):
    """
    Transcribe file and return subtitle file for download
    
    Example:
    ```
    curl -X POST "http://localhost:8000/transcribe/file/download" \\
         -F "file=@video.mp4" \\
         -F "format=srt" \\
         -o output.srt
    ```
    """
    if format not in ["srt", "json", "txt"]:
        raise HTTPException(status_code=400, detail="Invalid format. Use: srt, json, or txt")
    
    try:
        logger.info(f"Received download request for file: {file.filename}")
        
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe with temporary output
            with tempfile.TemporaryDirectory() as temp_output_dir:
                result = transcribe_video(
                    source=temp_file_path,
                    output_dir=temp_output_dir,
                    output_name="transcription",
                    model=model,
                    language=language,
                    device=device,
                    use_yt_dlp=False,
                    vad_filter=False,
                    cleanup=True,
                    log_level="INFO",
                )
                
                # Return requested format file
                output_file = result.output_files[format]
                
                # Media types
                media_types = {
                    "srt": "text/plain",
                    "json": "application/json",
                    "txt": "text/plain",
                }
                
                return FileResponse(
                    path=output_file,
                    media_type=media_types[format],
                    filename=f"transcription.{format}",
                )
        
        finally:
            # Clean up uploaded file
            Path(temp_file_path).unlink(missing_ok=True)
    
    except Exception as e:
        logger.error(f"Transcription failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Run the API server
    
    Args:
        host: Host to bind to
        port: Port to listen on
        reload: Enable auto-reload for development
    """
    import uvicorn
    
    uvicorn.run(
        "video2subs.server:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run_server()
