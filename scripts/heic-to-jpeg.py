#!/usr/bin/env python3
"""
HEIC to JPEG Converter using macOS ImageIO
Handles HDR HEIC files properly by extracting SDR data
"""

import subprocess
import os
from pathlib import Path

def heic_to_jpeg_macos(heic_path: str) -> str:
    """Convert HEIC to JPEG using macOS automator/sips"""
    heic_file = Path(heic_path)
    jpg_path = str(heic_file.with_suffix('.jpg'))
    
    # Use a more robust approach with tiffutil and sips
    tiff_path = "/tmp/temp_" + heic_file.stem + ".tiff"
    
    try:
        # Convert HEIC to TIFF first (preserves colors better)
        result = subprocess.run([
            'sips', '-m', heic_path, '--out', tiff_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(tiff_path):
            # Convert TIFF to JPEG
            subprocess.run([
                'sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', 'best',
                tiff_path, '--out', jpg_path
            ], capture_output=True)
            
            # Clean up temp file
            if os.path.exists(tiff_path):
                os.remove(tiff_path)
            
            if os.path.exists(jpg_path):
                print(f"Converted: {heic_file.name} -> {Path(jpg_path).name}")
                return jpg_path
    except Exception as e:
        print(f"Error: {e}")
    
    return ""

def batch_convert():
    """Convert all HEIC files in ~/Pictures"""
    pics_dir = Path.home() / "Pictures"
    heic_files = list(pics_dir.glob("*.HEIC")) + list(pics_dir.glob("*.heic"))
    
    if not heic_files:
        print("No HEIC files found")
        return
    
    print(f"Found {len(heic_files)} HEIC files")
    print("Converting...\n")
    
    for heic_file in sorted(heic_files):
        jpg_path = str(heic_file.with_suffix('.jpg'))
        
        # Skip if JPEG already exists and is newer
        jpg_file = Path(jpg_path)
        if jpg_file.exists() and jpg_file.stat().st_mtime > heic_file.stat().st_mtime:
            print(f"Skipped (up to date): {heic_file.name}")
            continue
        
        heic_to_jpeg_macos(str(heic_file))

if __name__ == "__main__":
    batch_convert()
