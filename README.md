# bldhol-interrogation
who wants to do that manually?

## Prerequisites 

### [python3](https://www.python.org/)

### pip packages:

- pytesseract (OCR)
- PIL (image editing)
- shutil

### [adb](https://developer.android.com/studio/command-line/adb)

- must be available from command line

### [GraphicsMagick](http://www.graphicsmagick.org/)

- must be available from command line

## Running

Enable adb on device/emulator

Enter your adb device address in `sid` variable

(Actually, fix some code around it if needed. It's currently bluestacks-oriented)

Coordinates should match for any 1080p screen (bluestacks default), but if not, adjust as neeeded

Run main.py

Multi-cell drifting:

- yes: after finishing the current prisoner, go to next cell

- no: after finishing the current prisoner, get prompted for another

## Notes

- Male lux is ass. His interrogation numbers are hard to OCR due to his clothes. Might have to repeat several times.

- Bugs are present, but whatever.
