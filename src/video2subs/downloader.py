"""
Media downloader module for handling URL downloads and local files
"""

import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests

from .config import get_temp_dir
from .utils import is_url, sanitize_filename

logger = logging.getLogger(__name__)


class MediaDownloader:
    """Handle downloading media from URLs or using local files"""

    def __init__(self, use_yt_dlp: bool = True):
        """
        Initialize MediaDownloader
        
        Args:
            use_yt_dlp: Whether to use yt-dlp for video downloading (for YouTube, etc.)
        """
        self.use_yt_dlp = use_yt_dlp
        self.temp_dir = get_temp_dir()

    def get_media(self, source: str) -> Tuple[Path, bool]:
        """
        Get media file from source (URL or local path)
        
        Args:
            source: URL or local file path
            
        Returns:
            Tuple of (Path to media file, whether it's a temp file to cleanup)
        """
        if is_url(source):
            return self._download_from_url(source), True
        else:
            local_path = Path(source)
            if not local_path.exists():
                raise FileNotFoundError(f"Local file not found: {source}")
            if not local_path.is_file():
                raise ValueError(f"Path is not a file: {source}")
            logger.info(f"Using local file: {local_path}")
            return local_path, False

    def _download_from_url(self, url: str) -> Path:
        """
        Download media from URL
        
        Args:
            url: Media URL
            
        Returns:
            Path to downloaded file
        """
        # Try yt-dlp first for video sites
        if self.use_yt_dlp and self._is_video_site(url):
            try:
                return self._download_with_ytdlp(url)
            except Exception as e:
                logger.warning(f"yt-dlp download failed: {e}, falling back to direct download")

        # Direct download for direct links
        return self._download_direct(url)

    def _is_video_site(self, url: str) -> bool:
        """Check if URL is from a known video hosting site"""
        video_sites = [
            "youtube.com",
            "youtu.be",
            "bilibili.com",
            "vimeo.com",
            "dailymotion.com",
            "twitter.com",
            "x.com",
        ]
        parsed = urlparse(url)
        return any(site in parsed.netloc for site in video_sites)

    def _download_with_ytdlp(self, url: str) -> Path:
        """
        Download video using yt-dlp
        
        Args:
            url: Video URL
            
        Returns:
            Path to downloaded file
        """
        try:
            import yt_dlp
        except ImportError:
            raise ImportError(
                "yt-dlp is required for downloading from video sites. "
                "Install it with: pip install yt-dlp"
            )

        output_template = str(self.temp_dir / "%(title)s.%(ext)s")
        
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": output_template,
            "quiet": False,
            "no_warnings": False,
            "extract_flat": False,
        }

        logger.info(f"Downloading video from {url} using yt-dlp...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        downloaded_path = Path(filename)
        if not downloaded_path.exists():
            raise FileNotFoundError(f"Downloaded file not found: {filename}")
            
        logger.info(f"Downloaded to: {downloaded_path}")
        return downloaded_path

    def _download_direct(self, url: str) -> Path:
        """
        Direct download from URL using requests
        
        Args:
            url: Direct media URL
            
        Returns:
            Path to downloaded file
        """
        logger.info(f"Downloading from {url}...")
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download from {url}: {e}")

        # Try to get filename from Content-Disposition header or URL
        filename = self._get_filename_from_response(response, url)
        output_path = self.temp_dir / filename

        # Download with progress
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        logger.debug(f"Download progress: {progress:.1f}%")

        logger.info(f"Downloaded to: {output_path}")
        return output_path

    def _get_filename_from_response(
        self, response: requests.Response, url: str
    ) -> str:
        """Extract filename from response headers or URL"""
        # Try Content-Disposition header
        if "Content-Disposition" in response.headers:
            content_disp = response.headers["Content-Disposition"]
            if "filename=" in content_disp:
                filename = content_disp.split("filename=")[-1].strip('"\'')
                return sanitize_filename(filename)

        # Try URL path
        parsed = urlparse(url)
        path = parsed.path
        if path and "/" in path:
            filename = path.split("/")[-1]
            if filename:
                return sanitize_filename(filename)

        # Default filename
        return f"downloaded_media_{os.urandom(4).hex()}.mp4"

    def cleanup(self, path: Path):
        """Remove temporary file"""
        if path.exists() and path.parent == self.temp_dir:
            try:
                path.unlink()
                logger.debug(f"Cleaned up temporary file: {path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {path}: {e}")
