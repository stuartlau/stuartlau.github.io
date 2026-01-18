#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shutil

def check_ffmpeg():
    """Check if ffmpeg is installed."""
    if shutil.which('ffmpeg') is None:
        print("Error: ffmpeg is not installed. Please install it using 'brew install ffmpeg'")
        sys.exit(1)

def convert_mov_to_mp4(file_path, delete_original=True, crf=23):
    """Convert a single MOV file to MP4."""
    # Determine output filename
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(directory, base_name + ".mp4")

    if os.path.exists(output_path):
        print(f"Skipping {filename}: {os.path.basename(output_path)} already exists.")
        return

    print(f"Converting {filename} to MP4...")
    
    # FFmpeg command
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-vcodec', 'libx264',
        '-crf', str(crf),
        '-preset', 'medium',
        '-acodec', 'aac',
        '-movflags', '+faststart',
        '-loglevel', 'error', # Suppress verbose output
        '-stats', # Show progress
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully converted: {output_path}")
        
        # Calculate space savings
        original_size = os.path.getsize(file_path)
        new_size = os.path.getsize(output_path)
        saved = original_size - new_size
        saved_mb = saved / (1024 * 1024)
        print(f"Space saved: {saved_mb:.2f} MB ({(saved/original_size)*100:.1f}%)")

        if delete_original:
            os.remove(file_path)
            print(f"Deleted original file: {file_path}")
            
    except subprocess.CalledProcessError:
        print(f"Error converting {file_path}")
        if os.path.exists(output_path):
            os.remove(output_path) # Clean up partial file

def main():
    parser = argparse.ArgumentParser(description="Convert MOV files to MP4 to save space.")
    parser.add_argument("path", help="File or directory path to process", default=".", nargs="?")
    # Changed default to True (store_false means passing --keep sets it to False)
    parser.add_argument("--keep", action="store_false", dest="delete", help="Keep original MOV files (default is to delete)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    parser.add_argument("--crf", type=int, default=23, help="CRF value for quality (default: 23). Lower is better quality, higher is smaller size.")
    
    parser.set_defaults(delete=True)
    
    args = parser.parse_args()
    
    check_ffmpeg()
    
    target_path = os.path.abspath(args.path)
    
    if os.path.isfile(target_path):
        if target_path.lower().endswith('.mov'):
            convert_mov_to_mp4(target_path, args.delete, args.crf)
        else:
            print("Error: Targeted file is not a .mov file")
    elif os.path.isdir(target_path):
        if args.recursive:
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    if file.lower().endswith('.mov'):
                        convert_mov_to_mp4(os.path.join(root, file), args.delete, args.crf)
        else:
            for file in os.listdir(target_path):
                if file.lower().endswith('.mov'):
                    convert_mov_to_mp4(os.path.join(target_path, file), args.delete, args.crf)
    else:
        print(f"Error: Path not found: {target_path}")

if __name__ == "__main__":
    main()
