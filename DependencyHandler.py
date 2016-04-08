#!/usr/bin/env python3

import os
import platform

__author__ = "Peter Maar"
__version__ = "0.1.0"

def checkTesseract():
    """Returns True if Tesseract is installed, or false if it is not"""
    if os.name == 'posix':
        code = os.system("tesseract > /dev/null 2>&1")
    elif os.name == 'nt':
        code = os.system("tesseract > nul 2>&1")

    if code == 0:  # Tesseract found? Typically means no errors.
        return True
    elif code == 256:  # Tesseract found? Seems to be returned on Mac if the command succeeds.
        return True
    else:  # Not found, or something went wrong
        return False


def checkImagemagick():
    """Returns True if Imagemagick is installed, or false if it is not"""
    if os.name == 'posix':
        code = os.system("convert > /dev/null 2>&1")
    elif os.name == 'nt':
        code = os.system("convert > nul 2>&1")

    if code == 0:  # Imagemagick found? Typically means no errors.
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



def installImagemagick():
    """Attempt to install Imagemagick automatically."""

    if platform.system() == 'Darwin':  # Macintosh
        if os.system("brew") == 256:  # Return code if installed
            os.system("brew install imagemagick")

    elif platform.system() == 'Windows':
        None


def dependencies(tryAgain = True):
    """If the dependencies are already installed returns true.
    If they are not, tries to install them and returns true if it works.
    If installing them fails, returns false.
    :param tryAgain: Used by the method for recursive checking of the dependencies. Typically leave it at the default."""

    tess = checkTesseract()
    magk = checkImagemagick()

    if tess and magk:  # Both are installed already,
        return True

    elif tess and not magk:  # Only Tesseract is installed
        installImagemagick()

    elif not tess and magk:  # Only Imagemagick is installed
        installTesseract()

    else:  # Neither are installed
        # Install both
        installTesseract()
        installImagemagick()

    if tryAgain:  # If this is the first try, and it got this far (didn't return true)
        return dependencies(False)  # Try again to see if the installs worked
    else:  # Otherwise, if this is the second try, and it made it this far, they had to be 'installed' a second time, and don't seem to be working
        return False  # Just return false, indicating that it didn't work

if __name__ == '__main__':
    print(dependencies())