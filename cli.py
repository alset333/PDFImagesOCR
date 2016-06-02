#!/usr/bin/env python3

import os, sys
import time
import ocrCore

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
        try:
            while core.running:
                print('a', core.running)  # For Codeship debugging
                time.sleep(5)
                print(core.currentTask + ': ' + core.fileName)
                core.updateTick()
                print('b', core.running)  # For Codeship debugging
        except KeyboardInterrupt:
            self.cleanExit(core)
        os.system('cat test.pdf-OCR.txt')  # For Codeship debugging
        print('sys.exit?')  # For Codeship debugging
        sys.exit()  # For Codeship debugging

    def cleanExit(self, core):
        print('\nExiting...')
        core.updateTick()
        if core.currentTask == 'converting':
            core.cnvrtSbProc.kill()  # Stop the conversion if it's running
        elif core.currentTask == 'recognising':
            core.queuedTessSubProcesses = []  # Remove all queued tesseract subprocesses so no new ones start
            for tessSubProcess in core.tessSubProcesses:
                tessSubProcess.kill()
                core.tessSubProcesses.remove(tessSubProcess)
        core.currentTask = 'finishing'  # Let it remove the folders etc
        core.updateTick()  # Trigger an update to actually remove the folders etc
        while core.running: None  # Wait for it to finish

        exit()

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
