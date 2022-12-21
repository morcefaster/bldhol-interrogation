# bldhol-interrogation
who wants to do that manually?

## Prerequisites 


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

Coordinates should match for any 1080p screen (bluestacks default), but if not, adjust as neeeded

Run main.py

Multi-cell drifting:

- yes: after finishing the current prisoner, go to next cell

- no: after finishing the current prisoner, get prompted for another
