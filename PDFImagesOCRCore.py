import DependencyHandler
import os

__author__ = 'Peter Maar'
__version__ = '0.1.0'

HELPTEXT = """

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
        ImageMagick is needed to convert the PDF into PNGs.
        ImageMagick's convert command must be accessible from the command line as 'convert'.
    Tesseract OCR Engine (CLI)
        The Tesseract OCR Engine is needed for reading text from the images.
        It must be accessible from the command line as 'tesseract'.

"""

def shouldPrintHelp(argv):
    return (len(argv) != 3 and len(argv) != 4) or 'help' in argv or '-h' in argv or '/?' in argv or '--help' in argv

def checkDepend():
    print("Checking dependencies...")
    if DependencyHandler.dependencies():
        print("Dependencies seem good! Proceeding.")
    else:
        print("Dependencies not detected or not working,\nand could not be installed automatically.\nPlease install and configure them.")
        exit()

def pdfToImages(ifp, tp):
    """Takes a PDF from the input-file-path (ifp), and converts it into images as 'pg-*.png' in the temporary path (tp). Returns the number of pages."""
    print("Converting PDF into images...")
    os.system('convert -density 300 "' + ifp + '" "' + os.path.normpath(tp + '/pg.png') + '"')
    files = os.listdir(tp)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    pgCount = len(files) # The number of pages is the number of files
    print("PDF Converted.")
    return pgCount