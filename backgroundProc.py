#!/usr/bin/env python3

import os
import sys
import time

__author__ = 'Peter Maar'
__version__ = '0.1.0'

############### CONFIGURATION CONSTANTS. SET THESE AS ABSOLUTE PATHS MATCHING YOUR SYSTEM'S CONFIGURATION ###############
DOWNLOADS_PATH = """/Users/petermaar/Downloads"""
PDFImagesOCR_PATH = """/Users/petermaar/Google Drive/Sync With Desktop App/10th Grade/Python/PythonMaarPeter/Semester 2/Final Project/PDFImagesOCR/PDFImagesOCR.py"""
#######################################################################################################

DEBUGMODE = False

downloadsFolder = os.path.normpath(DOWNLOADS_PATH)
programLoc = os.path.normpath(PDFImagesOCR_PATH)


if not (os.path.isdir(downloadsFolder) and os.path.isfile(programLoc) and (programLoc.endswith('/PDFImagesOCR.py') or programLoc.endswith('\PDFImagesOCR.py'))):
    print("Error, invalid configuration constants.")
    print("Edit the configuration constants in backgroundProc.py in the directory:\n", sys.path[0])
    exit()


def makeSearchablePdfOf(inPdf):
    command = '"' + programLoc + '" "' + inPdf + '" pdf'
    os.system(command)

def makeTxtOf(inPdf):
    command = '"' + programLoc + '" "' + inPdf + '" txt'
    os.system(command)


# Run the loop

while True:
    currentFiles = os.listdir(downloadsFolder)  # Files currently in downloads folder

    currentPdfNames = []  # PDFs currently in downloads folder
    for file in currentFiles:
        if file[-4:] == '.pdf' and file[-8:] != '-OCR.pdf':  # It must be a pdf, but not one we've already processed
            currentPdfNames.append(file)

    if DEBUGMODE:
        print('currentNames', currentPdfNames)

    currentPdfs = []
    for pdf in currentPdfNames:
        currentPdfs.append(os.path.normpath(downloadsFolder + '/' + pdf))

    if DEBUGMODE:
        print('currentPdfs', currentPdfs)

    for pdf in currentPdfs:
        searchPdfPath = pdf + '-OCR.pdf'
        if not os.path.isfile(searchPdfPath):
            print('PDF --> Searchable PDF\n', pdf)
            makeSearchablePdfOf(pdf)

        txtPath = os.path.normpath(pdf + '-OCR.txt')
        if not os.path.isfile(txtPath):
            print('PDF --> txt\n', pdf)
            makeTxtOf(pdf)

    time.sleep(5)
