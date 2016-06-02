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


def ppf2_Ok():
    try:
        import PyPDF2
        return True
    except Exception as e:
        if DEBUGMODE:
            print(e)
        return False


def imgmgk_Ok():
    if platform.system() == 'Windows':
        code = os.system('convert > NUL 2>&1')
    else:
        code = os.system('convert > /dev/null 2>&1')

    # Success is 256
    return code == 256


def tess_Ok():
    if platform.system() == 'Windows':
        code = os.system('tesseract > NUL 2>&1')
    else:
        code = os.system('tesseract > /dev/null 2>&1')

    # Success is 256
    return code == 256
