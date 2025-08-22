# Smooth Camera App

A modern, smooth webcam app built with Python and CustomTkinter.

## Features
- Beautiful splash screen and dark mode UI
- Loader animation and buffering when starting camera
- Capture images from your webcam
- Each capture is saved in your user's Pictures folder with a timestamp
- Developer credit always visible
- About dialog on camera stop
- Custom app icon
- Build as a standalone .exe (no terminal window)

## Screenshots

<!-- Add screenshots of the splash screen, main window, and captured images here -->

## How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Run: `python camera_app.py`

## Build as .exe
- Install PyInstaller: `pip install pyinstaller`
- Build: `pyinstaller --onefile --noconsole --icon=icon.ico camera_app.py`
- The .exe will be in the `dist` folder.

## Credits
Developed by Fozan Ahmed
