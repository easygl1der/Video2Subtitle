#!/usr/bin/env python3
"""
Example HTTP API client for video2subs
"""

import json
from pathlib import Path

import requests


class Video2SubsClient:
    """Simple client for video2subs API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def transcribe_url(
        self,
        url: str,
        model: str = "base",
        language: str = None,
        device: str = "auto",
    ):
        """Transcribe video from URL"""
        endpoint = f"{self.base_url}/transcribe/url"
        
        payload = {
            "url": url,
            "model": model,
            "language": language,
            "device": device,
        }
        
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def transcribe_file(
        self,
        file_path: str,
        model: str = "base",
        language: str = None,
    ):
        """Transcribe local file"""
        endpoint = f"{self.base_url}/transcribe/file"
        
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {
                "model": model,
                "language": language or "",
            }
            
            response = requests.post(endpoint, files=files, data=data)
            response.raise_for_status()
        
        return response.json()
    
    def download_subtitle(
        self,
        file_path: str,
        output_path: str,
        format: str = "srt",
        model: str = "base",
    ):
        """Transcribe and download subtitle file"""
        endpoint = f"{self.base_url}/transcribe/file/download"
        
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {
                "format": format,
                "model": model,
            }
            
            response = requests.post(endpoint, files=files, data=data)
            response.raise_for_status()
        
        # Save to file
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"Subtitle saved to: {output_path}")
    
    def list_models(self):
        """List available models"""
        endpoint = f"{self.base_url}/models"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def health_check(self):
        """Check API health"""
        endpoint = f"{self.base_url}/health"
        response = requests.get(endpoint)
        return response.status_code == 200


def main():
    """Example usage"""
    client = Video2SubsClient()
    
    # Health check
    print("Checking API health...")
    if client.health_check():
        print("✓ API is healthy")
    else:
        print("✗ API is not responding")
        return
    
    # List models
    print("\nAvailable models:")
    models = client.list_models()
    for model in models["models"]:
        marker = " (default)" if model["is_default"] else ""
        print(f"  • {model['name']}{marker}: {model['info']}")
    
    # Example 1: Transcribe from URL
    print("\nExample 1: Transcribe from URL")
    try:
        result = client.transcribe_url(
            url="https://example.com/sample.mp4",
            model="base",
            language="en",
        )
        print(f"✓ Generated {len(result['segments'])} segments")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Example 2: Transcribe local file
    print("\nExample 2: Transcribe local file")
    try:
        result = client.transcribe_file(
            file_path="./sample.mp4",
            model="base",
            language="zh",
        )
        print(f"✓ Generated {len(result['segments'])} segments")
        
        # Print first few segments
        for seg in result["segments"][:3]:
            print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Example 3: Download subtitle file
    print("\nExample 3: Download subtitle file")
    try:
        client.download_subtitle(
            file_path="./sample.mp4",
            output_path="./output.srt",
            format="srt",
            model="base",
        )
        print("✓ Subtitle downloaded")
    except Exception as e:
        print(f"✗ Failed: {e}")


if __name__ == "__main__":
    main()
