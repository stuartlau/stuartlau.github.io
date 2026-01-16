#!/bin/bash
# HEIC to JPEG Converter for iPhone Photos
# Fixes black images issue caused by unsupported HEIC format

PICTURES_DIR="$HOME/Pictures"

echo "Converting HEIC files to JPEG..."

find "$PICTURES_DIR" -maxdepth 1 -name "*.HEIC" -o -name "*.heic" | while read -r heic_file; do
    jpg_file="${heic_file%.*}.jpg"
    
    if [ -f "$jpg_file" ]; then
        echo "  Already exists: $(basename "$jpg_file")"
    else
        echo "  Converting: $(basename "$heic_file")"
        sips -s format jpeg -s formatOptions best "$heic_file" --out "$jpg_file" 2>/dev/null
        
        if [ $? -eq 0 ] && [ -s "$jpg_file" ]; then
            rm "$heic_file"
            echo "    → $(basename "$jpg_file") ✓"
        else
            echo "    Failed to convert"
        fi
    fi
done

echo "Done!"
