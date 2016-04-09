#!/usr/bin/env python3
# PDFImagesOCR.py

import PDFImagesOCRCore
import sys
import os
import tempfile
import shutil
import time


__author__ = "Peter Maar"
__version__ = "0.5.0"



############# METHOD DEFINITIONS START #################

def imagesToTxt(pgCount, tp, offp):
    """Takes the temporary path (tp) where pgCount images are stored, and OCRs them into a txt file (offp)"""

    # OCR the images
    for i in range(pgCount): # Starting at 0, and up to (but not including) pgCount - this works since counting pages starts at 1, but the files start at 0.
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".png")
        print("Reading page", i + 1, "of", str(pgCount) + "...")
        if DEBUGMODE:
            print('tesseract "' + imagePath + '" "' + imagePath + '"')
        os.system('tesseract "' + imagePath + '" "' + imagePath + '"')

    # Combine the output files
    outfile = open(offp, 'a')
    for i in range(pgCount):
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".png")
        infile = open(imagePath + '.txt')
        outfile.write(infile.read())
        infile.close()
        os.remove(imagePath + '.txt') # Delete the file after it's been appended
    outfile.close()

    print("All pages read.")

def imagesToPDF(pgCount, tp, offp):
    """Takes the temporary path (tp) where pgCount images are stored, and OCRs them into a pdf file (offp)"""
    # OCR the images
    for i in range(pgCount):  # Starting at 0, and up to (but not including) pgCount - this works since counting pages starts at 1, but the files start at 0.
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".png")
        print("Reading page", i + 1, "of", str(pgCount) + "...")
        if DEBUGMODE:
            print('tesseract "' + imagePath + '" "' + imagePath + '" pdf')
        os.system('tesseract "' + imagePath + '" "' + imagePath + '" pdf')

    # Combine the output files
    merger = PyPDF2.PdfFileMerger()  # New PDF
    for i in range(pgCount):
        imagePath = os.path.normpath(tp + "/pg-" + str(i) + ".png")
        merger.append(imagePath + '.pdf')
        os.remove(imagePath + '.pdf')  # Delete the file after it's been appended
    merger.write(offp)

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
outType = sys.argv[2].lower() # 'txt' or 'pdf'
outFileFullPath = inFilePath[:-4] + "-OCR." + outType # the dir path + the filename
outFileDir = outFileFullPath[:outFileFullPath.rfind(os.path.normpath('/'))] + os.path.normpath('/') # the output directory
fileName = outFileFullPath[outFileFullPath.rfind(os.path.normpath('/')) + 1:-8] # the output filename

# Import PyPDF2 if needed.
if outType == 'pdf':
    try:
        import PyPDF2
    except ImportError:
        os.system('pip3 install PyPDF2')
        try:
            import PyPDF2
        except ImportError:
            print("You need 'PyPDF2' installed to output to PDF from this program. Please install it.")
            exit()

    ynOut = input('Searchable PDF output is still highly experimental. Proceed? (y/n)')
    if ynOut != 'y':
        print("Response did not match 'y', exiting.")
        exit()

# Check that the output file doesn't exist
if os.path.isfile(outFileFullPath):
    print("Output file already exists!")
    exit()

# Find & Make Temporary Location
if not os.path.isdir(os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR-TempFolder")): # If the main temp path isn't there
    os.mkdir(os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR-TempFolder")) # Make it

# Make temp path for this specific instance
tempPath = os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR-TempFolder/" + fileName + '-' + str(time.time())) + os.path.normpath('/') # Add in the starting time to help prevent conflicts if multiple instances are run
os.mkdir(tempPath)

if DEBUGMODE:
    print('In: ' + inFilePath + '\n' +
          'Output File: ' + outFileFullPath + '\n' +
          'Output Directory: ' + outFileDir + '\n' +
          'File name: ' + fileName + '\n' +
          'Temp: ' + tempPath + '\n\n')


###################################  PREPARATIONS END  ################################################################






# Use ImageMagick to turn the pages into images
pageCount = PDFImagesOCRCore.pdfToImages(inFilePath, tempPath) # Pagecount is the number of pages, not the number of the last image


if outType == 'txt':
    imagesToTxt(pageCount, tempPath, outFileFullPath)
elif outType == 'pdf':
    imagesToPDF(pageCount, tempPath, outFileFullPath)
else:
    print("Unknown output type!")

    
if DEBUGMODE:
    print("Removing temporary files")
shutil.rmtree(tempPath)

print('PDFImagesOCR completed!\nOutput saved as "' + outFileFullPath + '".')
