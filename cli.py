#!/usr/bin/env python3

import os, sys
import ocrCore
import time

__author__ = 'Peter Maar'
__version__ = '0.1.0'  # First separate CLI

DEBUGMODE = False

helpText = \
"""
NAME
    PDFImagesOCR - OCRs PDFs to text

SYNOPSIS
    PDFImagesOCR inFile outType

DESCRIPTION
    A utility that uses OCR to convert a PDF file to a text file or a searchable PDF

OPTIONS
    inFile
        The path to the 'input' file to process.

    outType
        The type of output to produce.
        'pdf' for a searchable PDF
        'txt' for a text file

"""

helpArgs = ['help', 'HELP', '-h', '/h', '-?', '/?', '--help']


class Cli:
    def __init__(self, args):
        if DEBUGMODE:
            print(args)
        printHelpTextAndExitIfNeeded(args)
        inFile = os.path.normpath(args[1])
        outType = args[2]
        core = ocrCore.Ocr(inFile, outType)
        while core.running:
            print('a', core.running)
            time.sleep(5)
            print(core.currentTask + ': ' + core.fileName)
            core.updateTick()
            print('b', core.running)
        print('sys.exit?')
        sys.exit()


def printHelpTextAndExitIfNeeded(args):
    # If the wrong number of args are given, show help and exit
    argCount = len(args)
    if argCount != 3:  # The program, the input file, and the output type
        print("Invalid number of arguments")
        print(helpText)
        sys.exit()

    # If a help argument is given, show help and exit
    for arg in args:
        if arg in helpArgs:
            print(helpText)
            sys.exit()

    if args[2] != 'pdf' and args[2] != 'txt':
        print("Invalid output type: ", args[2])
        print(helpText)
        sys.exit()
