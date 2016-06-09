#!/usr/bin/env python3

import os
import platform

__author__ = 'Peter Maar'
__version__ = '0.1.0'

DEBUGMODE = False


class dCheckr:
    def __init__(self):
        self.reason = ''
        # Start assuming they're ok -- set them to false later if they're not
        self.pypdf2_is_Ok       = True
        self.imagemagick_is_Ok  = True
        self.tesseract_is_Ok    = True

    def check(self):
        # PyPDF2
        self.reason += 'PyPDF2 installation is '
        if not ppf2_Ok():
            self.reason += 'not '
            self.pypdf2_is_Ok = False
        self.reason += 'Ok.\n'

        # ImageMagick
        self.reason += 'ImageMagick installation is '
        if not imgmgk_Ok():
            self.reason += 'not '
            self.imagemagick_is_Ok = False
        self.reason += 'Ok.\n'

        # Tesseract
        self.reason += 'Tesseract installation is '
        if not tess_Ok():
            self.reason += 'not '
            self.tesseract_is_Ok = False
        self.reason += 'Ok.\n'

    def dpndOk(self):
        return self.pypdf2_is_Ok and self.imagemagick_is_Ok and self.tesseract_is_Ok


def ppf2_Ok(tryInstall=True):
    try:
        import PyPDF2
        return True
    except Exception as e:
        if DEBUGMODE:
            print(e)
        if tryInstall:
            print("PyPDF2 is not installed. This may be a simple fix using PIP.\nAttempting to install PyPDF2, please wait a moment...")
            os.system('pip3 install PyPDF2')
            return ppf2_Ok(tryInstall=False)
        else:
            return False


def imgmgk_Ok():
    code   = None
    mCode  = None
    mcCode = None

    if platform.system() == 'Windows':
        mCode  = os.system('magick > NUL 2>&1')
        mcCode = os.system('magick convert > NUL 2>&1')
    else:
        code = os.system('convert > /dev/null 2>&1')

    if code == 256:  # Mac returns 256 if the command exists
        return True
    elif mCode == 0 and mcCode == 1:  # Windows returns 0 if the command 'magick' exists, and returns 1 if 'magick ___' exists, where ___ is a command
        return True

    # Success is 256 on Mac, and 0 on Windows
    return code == 256 or code == 0


def tess_Ok():
    if platform.system() == 'Windows':
        code = os.system('tesseract > NUL 2>&1')
    else:
        code = os.system('tesseract > /dev/null 2>&1')

    # Success is 256 on Mac, and 0 on Windows
    return code == 256 or code == 0

if __name__ == '__main__':
    d = dCheckr()
    d.check()

    ok = d.dpndOk()
    print('Dependencies are Ok?', ok)

    r = d.reason
    print("\nReason:\n-----")
    print(r)
    print('-----')