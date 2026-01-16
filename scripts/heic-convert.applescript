(*
HEIC to JPEG Converter for iPhone HDR Photos
Uses macOS Preview app with proper color profile conversion
*)

on run argv
    set inputFile to item 1 of argv
    set outputFile to inputFile & ".jpg"
    
    tell application "Preview"
        activate
        open inputFile
        
        -- Wait for file to open
        delay 1
        
        -- Export as JPEG
        tell application "System Events"
            keystroke "e" using {command down, option down, shift down}
            delay 0.5
        end tell
        
        -- Close the window
        tell application "System Events"
            keystroke "w" using {command down}
        end tell
    end tell
end run
