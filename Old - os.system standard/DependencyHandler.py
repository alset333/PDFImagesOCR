#!/usr/bin/env python3

import os
import sys
import platform

__author__ = "Peter Maar"
__version__ = "0.1.0"

convertCommand = 'convert'

if os.name == 'nt':
    if os.path.isfile(os.path.normpath("C:/Program Files (x86)/Tesseract-OCR/tesseract")):
        tesseractCommandCommand = os.path.normpath("C:/Program Files (x86)/Tesseract-OCR/tesseract")
    else:
        tesseractCommand = os.path.normpath("C:/Program Files/Tesseract-OCR/tesseract")
else:
    tesseractCommand = 'tesseract'

def checkTesseract():
    """Returns True if Tesseract is installed, or false if it is not"""
    if os.name == 'posix':
        code = os.system(tesseractCommand + " > /dev/null 2>&1")
    elif os.name == 'nt':
        code = os.system(tesseractCommand + " > nul 2>&1")

    if code == 0:  # Tesseract found? Typically means no errors.
        return True
    elif code == 256:  # Tesseract found? Seems to be returned on Mac if the command succeeds.
        return True
    else:  # Not found, or something went wrong
        return False


def checkImagemagick():
    """Returns True if Imagemagick is installed, or false if it is not"""
    if os.name == 'posix':
        code = os.system(convertCommand + " > /dev/null 2>&1")
    elif os.name == 'nt':
        code = os.system(convertCommand + " > nul 2>&1")

    if code == 1:  # Imagemagick found? Seems to be returned on Windows if the command succeeds
        return True
    elif code == 256:  # Imagemagick found? Seems to be returned on Mac if the command succeeds.
        return True
    else:  # Not found, or something went wrong
        return False



def installTesseract():
    """Attempt to install Tesseract automatically."""

    if platform.system() == 'Darwin': # Macintosh
        if os.system("brew > /dev/null 2>&1") == 256:  # Return code if installed
            os.system("brew install tesseract")

    elif platform.system() == 'Windows':
        None



def installImagemagick(DEBUGMODE = False):
    """Attempt to install Imagemagick automatically."""
    global convertCommand

    if platform.system() == 'Darwin':  # Macintosh
        if os.system("brew") == 256:  # Return code if installed
            os.system("brew install imagemagick")

    elif platform.system() == 'Windows':
        if DEBUGMODE:
            print("Architecture", platform.architecture())

        if platform.architecture()[0] == '64bit':
            # Use the portable version if needed, much easier than installing
            convertCommand = os.path.normpath(sys.path[0] + '/IM/ImageMagick-6.9.3-7-portable-Q16-x64/convert.exe')

        elif platform.architecture()[0] == '32bit':
            # Use the portable version if needed, much easier than installing
            convertCommand = os.path.normpath(sys.path[0] + '/IM/ImageMagick-6.9.3-7-portable-Q16-x86/convert.exe')



def dependencies(tryAgain = True, DEBUGMODE = False, ):
    """If the dependencies are already installed returns true.
    If they are not, tries to install them and returns true if it works.
    If installing them fails, returns false.
    :param tryAgain: Used by the method for recursive checking of the dependencies. Typically leave it at the default."""

    tess = checkTesseract()
    magk = checkImagemagick()

    if DEBUGMODE:
        print('tess', tess)
        print('magk', magk)

    if not tryAgain:
        if not tess:
            print("Tesseract couldn't be found or installed.")
        else:
            print("Tesseract seems good.")
        if not magk:
            print("Imagemagick couldn't be found or installed.")
        else:
            print("Imagemagick seems good.")

    if tess and magk:  # Both are installed already,
        return True

    elif tess and not magk:  # Only Tesseract is installed
        installImagemagick(DEBUGMODE = DEBUGMODE)

    elif not tess and magk:  # Only Imagemagick is installed
        installTesseract()

    else:  # Neither are installed
        # Install both
        installTesseract()
        installImagemagick(DEBUGMODE = DEBUGMODE)

    if tryAgain:  # If this is the first try, and it got this far (didn't return true)
        return dependencies(False, DEBUGMODE = DEBUGMODE)  # Try again to see if the installs worked
    else:  # Otherwise, if this is the second try, and it made it this far, they had to be 'installed' a second time, and don't seem to be working
        return False  # Just return false, indicating that it didn't work

if __name__ == '__main__':
    print(dependencies())