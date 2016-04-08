#!/usr/bin/env python3
# PDFImagesOCR.py

import PDFImagesOCRCore
import sys
import os
import tempfile
import shutil
try:
    import PyPDF2
except ImportError:
    os.system('pip3 install PyPDF2')
    try:
        import PyPDF2
    except ImportError:
        print("You need 'PyPDF2' installed to use this program.")
        exit()

__author__ = "Peter Maar"
__version__ = "0.4.0"



############# METHOD DEFINITIONS START #################

def imagesToTxt(pgCount, tp, ofp):
    """Takes the temporary path (tp) where pgCount images are stored, and OCRs them into a txt file (ofp)"""

    # OCR the images
    for i in range(pgCount): # Starting at 0, and up to (but not including) pgCount - this works since counting pages starts at 1, but the files start at 0.
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".png")
        print("Reading page", i + 1, "of", str(pgCount) + "...")
        if DEBUGMODE:
            print('tesseract "' + imagePath + '" "' + ofp + str(i) + '"')
        os.system('tesseract "' + imagePath + '" "' + ofp + str(i) + '"')

    # Combine the output files
    outfile = open(ofp, 'a')
    for i in range(pgCount):
        infile = open(ofp + str(i) + '.txt')
        outfile.write(infile.read())
        infile.close()
        os.remove(ofp + str(i) + '.txt') # Delete the file after it's been appended
    outfile.close()

    print("All pages read.")

def imagesToPDF(pgCount, tp, ofp):
    """Takes the temporary path (tp) where pgCount images are stored, and OCRs them into a pdf file (ofp)"""
    # OCR the images
    for i in range(pgCount):  # Starting at 0, and up to (but not including) pgCount - this works since counting pages starts at 1, but the files start at 0.
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".png")
        print("Reading page", i + 1, "of", str(pgCount) + "...")
        if DEBUGMODE:
            print('tesseract "' + imagePath + '" "' + ofp + str(i) + '" pdf')
        os.system('tesseract "' + imagePath + '" "' + ofp + str(i) + '" pdf')

    # Combine the output files
    merger = PyPDF2.PdfFileMerger()  # New PDF
    for i in range(pgCount):
        merger.append(ofp + str(i) + '.pdf')
        os.remove(ofp + str(i) + '.pdf')  # Delete the file after it's been appended
    merger.write(ofp)

    print("All pages read.")

########### METHOD DEFINITIONS END ######################









##################################  PREPARATIONS BEGIN  ###############################################################


# Print help text if needed
if PDFImagesOCRCore.shouldPrintHelp(sys.argv):
    print(PDFImagesOCRCore.HELPTEXT)
    exit()

# Check if the program should run in debug mode
DEBUGMODE = 'DEBUG' in sys.argv

# Check dependencies
PDFImagesOCRCore.checkDepend()

# Get Input File Location
inFilePath = os.path.normpath(sys.argv[1])

# Check the input file exists
if not os.path.isfile(inFilePath):
    print("Input file doesn't exist!")
    exit()
    
# Get Output File Location
outType = sys.argv[2].lower()
outFilePath = inFilePath[:-4] + "-OCR." + outType

if outType == 'pdf':
    ynOut = input('Searchable PDF output is still highly experimental. Proceed? (y/n)')
    if ynOut != 'y':
        print("Response did not match 'y', exiting.")
        exit()

# Check that the output file doesn't exist
if os.path.isfile(outFilePath):
    print("Output file already exists!")
    exit()

# Find & Make Temporary Location
tempPath = os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR-TempFolder")
os.mkdir(tempPath)

if DEBUGMODE:
    print('In: ' + inFilePath + '\n' + 'Out: ' + outFilePath + '\n' + 'Temp: ' + tempPath + '\n\n')


###################################  PREPARATIONS END  ################################################################








# Use ImageMagick to turn the pages into images
pageCount = PDFImagesOCRCore.pdfToImages(inFilePath, tempPath) # Pagecount is the number of pages, not the number of the last image


if outType == 'txt':
    imagesToTxt(pageCount, tempPath, outFilePath)
elif outType == 'pdf':
    imagesToPDF(pageCount, tempPath, outFilePath)
else:
    print("Unknown output type!")

    
if DEBUGMODE:
    print("Removing temporary files")
shutil.rmtree(tempPath)

print('PDFImagesOCR completed!\nOutput saved as "' + outFilePath + '".')
