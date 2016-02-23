#!/usr/bin/env python3
# PDFImagesOCR-multi.py

import sys
import os
import tempfile
import shutil
import subprocess

__author__ = "Peter Maar"
__version__ = "0.2.0"

yn = input("""
WARNING! THIS PROGRAM IS A EXPERIMENTAL VERSION AND COULD BE DANGEROUS!
This is the 'multi' version of PDFImagesOCR. This version attempts to process multiple images at once.
This software has only been tested on Mac OSX Yosemite.
While it is stated in the license, I will reiterate that this software is provided 'as is' and I have no liability for any issues or damage(s) it causes.
It is recommended you are skilled with Python 3, tesseract, ImageMagick, and OSX, and that you have read the source code of this Python program before using this program.
If you wish to continue, please enter below 'I wish to continue despite the risks':\n
""")
if yn != 'I wish to continue despite the risks':
    print('You did not enter \'I wish to continue despite the risks\'. Program exiting.')
    exit()
else:
    print("Okay, I hope you know what you are doing!")

          
##################################  PREPARATIONS BEGIN  ##########################################

# Print help text if needed
if (len(sys.argv) != 3 and len(sys.argv) != 4) or 'help' in sys.argv or '-h' in sys.argv or '/?' in sys.argv or '--help' in sys.argv:
    print("""

NAME
    PDFImagesOCR-multi - PDF to txt or searchable PDF

COMMAND LINE SYNTAX
    PDFImagesOCR-multi inFile outType

PARTS/OPTIONS
    PDFImagesOCR-multi
        Command to execute the 'PDFImagesOCR-multi.py' file.
    inFile
        The path to the PDF input.
    outType
        Either 'txt' or 'pdf'. Specifies whether to output to a txt file,
         or to a searchable PDF file.

EXAMPLE
    In a folder with 'PDFImagesOCR-multi.py' and 'file.pdf', output to 'file-OCR.txt':
        Unix (Mac/Linux):
            "./PDFImagesOCR-multi.py file.pdf txt"
        Windows:
            (untested so far)           

DESCRIPTION
    Converts images from a PDF into a text file or a searchable PDF.
    PDFImagesOCR-multi requires 'ImageMagick', and the OCR Engine 'tesseract' to both be installed.
    The file output will be saved alongside the original file,
     as the original's name with '-OCR' appended to it.



REQUIREMENTS
    Python 3
        PDFImagesOCR-multi is written to be run by Python 3.
    ImageMagick (CLI)
        ImageMagick is needed to convert the PDF into JPEGs.
        ImageMagick's convert command must be accessible from the command line as 'convert'.
    Tesseract OCR Engine (CLI)
        The Tesseract OCR Engine is needed for reading text from the images.
        It must be accessible from the command line as 'tesseract'.

""")
    exit()

# Check if the program should run in debug mode
DEBUGMODE = 'DEBUG' in sys.argv

# Get Input File Location
inFilePath = os.path.normpath(sys.argv[1])
if not os.path.isfile(inFilePath):
    print("Input file doesn't exist!")
    exit()
    
# Get Output File Location
outType = sys.argv[2].lower()
outFilePath = inFilePath[:-4] + "-OCR." + outType
if os.path.isfile(outFilePath):
    print("Output file already exists!")
    print(outFilePath)
    exit()

# Get Temporary Location
tempPath = os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR-multi-TempFolder")
os.mkdir(tempPath)

if DEBUGMODE:
    print('In: ' + inFilePath + '\n' + 'Out: ' + outFilePath + '\n' + 'Temp: ' + tempPath + '\n\n')
    yn = input("Proceed? (y/n)\n")
    if yn.lower() != 'y':
        print("Exiting")
        exit()
###################################  PREPARATIONS END  ###########################################




def pdfToImages(ifp, tp):
    """Takes a PDF from the input file-path (ifp), and converts it into images as 'pg-*.jpg' in the temporary path (tp). Returns the number of pages."""
    print("Converting PDF into images...")
    os.system('convert -density 300 "' + ifp + '" "' + os.path.normpath(tp + '/pg.jpg') + '"')
    files = os.listdir(tp)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    pgCount = len(files) # The number of pages is the number of files
    print("PDF Converted.")
    return pgCount

def imagesToTxt(pgCount, tp, ofp):
    """Takes the temporary path (tp) where pgCount images are stored, and OCRs them into a txt file (ofp)"""
    procList = []  # List of 'subprocess.Popen's
    for i in range(pgCount): # Starting at 0, and up to (but not including) pgCount - this works since counting pages starts at 1, but the files start at 0.
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".jpg")
        print("Reading page", i + 1, "of", str(pgCount) + "...")
        if DEBUGMODE:
            print("""subprocess.Popen(['tesseract "' + imagePath + '" stdout >> "' + ofp[:-4] + str(i) + '"'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)""")
        proc = subprocess.Popen(['tesseract "' + imagePath + '" stdout >> "' + ofp[:-4] + str(i) + '"'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        procList.append(proc)

    for p in procList:  # Waits for all subprocesses to be done.
        p.wait()  # If the process isn't done yet, the program will stay at this line until it does.

    for i in range(pgCount):

        if DEBUGMODE:
            if os.name == 'posix': # If Linux or Mac OS X
                print('cat "' + ofp[:-4] + str(i) + '" >> "' + ofp + '"')
            else:  # If Windows #TODO find out if there are other non-posix OSes that we should take into account
                print('type "' + ofp[:-4] + str(i) + '" >> "' + ofp + '"')

        if os.name == 'posix':  # If Linux or Mac OS X
            os.system('cat "' + ofp[:-4] + str(i) + '" >> "' + ofp + '"')
        else:  # If Windows #TODO find out if there are other non-posix OSes that we should take into account
            os.system('type "' + ofp[:-4] + str(i) + '" >> "' + ofp + '"')
        os.remove(ofp[:-4] + str(i))
    
    print("All pages read.")


# Use ImageMagick to turn the pages into images
pageCount = pdfToImages(inFilePath, tempPath) # Pagecount is the number of pages, not the number of the last image


if outType == 'txt':
    imagesToTxt(pageCount, tempPath, outFilePath)
else:
    print("Unknown output type!")

    
if DEBUGMODE:
    print("Removing temporary files")
shutil.rmtree(tempPath)

print('PDFImagesOCR-multi completed!\nOutput saved as "' + outFilePath + '".')

