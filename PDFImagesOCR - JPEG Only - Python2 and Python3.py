#!/usr/bin/env python
# PDFImagesOCR.py

__author__ = "Peter Maar"
__version__ = "0.1.0"

import sys
import os
import tempfile
import shutil

#  Print help text depending on args
if (len(sys.argv) != 3 and len(sys.argv) != 4) or sys.argv[1] == '-h' or sys.argv[1] == '/h' or sys.argv[1] == '--help' or sys.argv[1] == 'help' or sys.argv[1] == '-?' or sys.argv[1] == '?' or sys.argv[1] == '/?':
    print("""
NAME
    PDFImagesOCR - PDF to txt or searchable PDF

COMMAND LINE SYNTAX
    PDFImagesOCR-FilePath inFile outType

PARTS/OPTIONS
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
    PDFImagesOCR requires the 'tesseract' CLI OCR engine.
    The file output will be saved alongside the original file,
     as the original's name with '-OCR' appended to it.



REQUIREMENTS
    Python 2 or 3
        PDFImagesOCR is written to be run by Python 2 or Python 3.
    Tesseract OCR Engine (CLI)
        The Tesseract OCR Engine is needed for reading text from the images.
        It must be accessible from the command line as 'tesseract'.
""")
    exit()



def getImages3():
    # Code modified from: http://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html
    # Extract JPGs from PDFs. Quick and dirty.

    pdf = open(sys.argv[1], "rb").read()

    startmark = b"\xff\xd8"
    startfix = 0
    endmark = b"\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find(b"endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")
         
        istart += startfix
        iend += endfix
        if debugMode:
            print("JPG %d from %d to %d" % (njpg, istart, iend))
        else:
            print("Extracting page", njpg + 1)
        jpg = pdf[istart:iend]
        jpgfile = open(os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/jpg%d.jpg" % njpg), "wb")
        jpgfile.write(jpg)
        jpgfile.close()
         
        njpg += 1
        i = iend

    return njpg


def getImages2():
    # Code modified from: http://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html
    # Extract JPGs from PDFs. Quick and dirty.

    pdf = file(sys.argv[1], "rb").read()

    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find("stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find("endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")
         
        istart += startfix
        iend += endfix
        if debugMode:
            print("JPG %d from %d to %d" % (njpg, istart, iend))
        else:
            print("Extracting page " + str(njpg + 1))
        jpg = pdf[istart:iend]
        jpgfile = file(os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/jpg%d.jpg" % njpg), "wb")
        jpgfile.write(jpg)
        jpgfile.close()
         
        njpg += 1
        i = iend

    return njpg


outExt = sys.argv[2].lower()
if outExt != 'txt' and outExt != 'pdf':
    print("Invalid output type argument. Expected 'txt' or 'pdf'")
    exit()


outfilename = sys.argv[1][:-4] + "-OCR." + outExt  # [:-4] removes extension
if os.path.isfile(outfilename):
    print("Output file '" + outfilename + "' already exists!")
    exit()

if 'DEBUG' in sys.argv:
    debugMode = True
else:
    debugMode = False


if not os.path.isfile(os.path.normpath(sys.argv[1])):
    print("Error! File not found!")
    exit()    


os.mkdir(os.path.normpath(tempfile.gettempdir() + '/PDFImagesOCR'))


v = sys.version_info[0]

if v == 3:
    jpgCount = getImages3()
else:
    jpgCount = getImages2()


if outExt == 'txt':  # If txt output
    for i in range(jpgCount):
        if debugMode:
            print("tesseract \"" + os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/jpg" + str(i) + ".jpg\"") + " stdout >> \"" + outfilename + "\"")
        else:
            print("Reading page " + str(i + 1))
        os.system("tesseract \"" + os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/jpg" + str(i) + ".jpg\"") + " stdout >> \"" + outfilename + "\"")
else:  # If searchable pdf output
    for i in range(jpgCount):
        if debugMode:
            print("tesseract \"" + os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/jpg" + str(i) + ".jpg\"") + " stdout pdf >> \"" + os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/page" + str(i) + ".pdf\""))
        else:
            print("Reading page " + str(i + 1))
        os.system("tesseract \"" + os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/jpg" + str(i) + ".jpg\"") + " stdout pdf >> \"" + os.path.normpath(tempfile.gettempdir() + "/PDFImagesOCR/page" + str(i) + ".pdf\""))
    #TODO save all in one pdf
            

    
shutil.rmtree(os.path.normpath(tempfile.gettempdir() + '/PDFImagesOCR'))

print("File saved as '" + outfilename + "'")
