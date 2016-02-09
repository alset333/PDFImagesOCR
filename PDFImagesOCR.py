#!/usr/bin/env python3
# PDFImagesOCR.py

import sys
import os
import tempfile
import shutil

__author__ = "Peter Maar"
__version__ = "0.1.0"



##################################  PREPARATIONS BEGIN  ###############################################################

# Print help text if needed
if (len(sys.argv) != 3 and len(sys.argv) != 4) or 'help' in sys.argv or '-h' in sys.argv or '/?' in sys.argv or '--help' in sys.argv:
    print("""

NAME
    PDFImagesOCR - PDF to txt or searchable PDF

COMMAND LINE SYNTAX
    PDFImagesOCR inFile outType

PARTS/OPTIONS
    PDFImagesOCR
        Command to execute the 'PDFImagesOCR.py' file.
    inFile
        The path to the PDF input.
    outType
        Either 'txt' or 'pdf'. Specifies whether to output to a txt file,
         or to a searchable PDF file.

EXAMPLE
    In a folder with 'PDFImagesOCR.py' and 'file.pdf', output to 'file-OCR.txt':
        Unix (Mac/Linux):
            "./PDFImagesOCR.py file.pdf txt"
        Windows:
            (untested so far)

DESCRIPTION
    Converts images from a PDF into a text file or a searchable PDF.
    PDFImagesOCR requires 'ImageMagick', and the OCR Engine 'tesseract' to both be installed.
    The file output will be saved alongside the original file,
     as the original's name with '-OCR' appended to it.



REQUIREMENTS
    Python 3
        PDFImagesOCR is written to be run by Python 3.
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
    exit()

# Get Temporary Location
tempPath = os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR-TempFolder")
os.mkdir(tempPath)

if DEBUGMODE:
    print('In: ' + inFilePath + '\n' + 'Out: ' + outFilePath + '\n' + 'Temp: ' + tempPath + '\n\n')

###################################  PREPARATIONS END  ################################################################




def pdfToImages(ifp, tp):
    """Takes a PDF from the input-file-path (ifp), and converts it into images as 'pg-*.jpg' in the temporary path (tp). Returns the number of pages."""
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
    for i in range(pgCount): # Starting at 0, and up to (but not including) pgCount - this works since counting pages starts at 1, but the files start at 0.
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".jpg")
        print("Reading page", i + 1, "of", str(pgCount) + "...")
        if DEBUGMODE:
            print('tesseract "' + imagePath + '" stdout >> "' + ofp + '"')
        os.system('tesseract "' + imagePath + '" stdout >> "' + ofp + '"')
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

print('PDFImagesOCR completed!\nOutput saved as "' + outFilePath + '".')
