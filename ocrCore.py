#!/usr/bin/env python3

import os, sys, tempfile, shutil
import subprocess
import PyPDF2

__author__ = 'Peter Maar'
__version__ = '0.1.0'

DEBUGMODE = False


class Ocr:
    def __init__(self, filename, outtype):
        self.outType = outtype
        self.fileName = filename
        self.running = True
        self.tessSubProcesses = []
        self.cnvrtSbProc = None
        self.tempSubfolder = os.path.normpath(tempfile.gettempdir() + '/PDFImagesOCR-TempFolder-' + filename[filename.rfind(os.path.normpath('/')) + 1:-4])
        self.pgCount = 0  # Not known yet, will be set later.

        self.currentTask = 'startConvert'  # Start with starting the conversion of the PDF to PNGs

        if DEBUGMODE:
            print('ocrCore.Ocr\t\t', filename)

        os.mkdir(self.tempSubfolder)

        #

    def updateTick(self):
        if self.currentTask == 'startConvert':
            self.startConvert()
            self.currentTask = 'converting'

        elif self.currentTask == 'converting':
            if self.cnvrtSbProc.poll() is not None:  # If it has a return code, it's done converting,
                self.currentTask = 'startOcr'              # so start the OCR

        elif self.currentTask == 'startOcr':
            self.pgCount = getImageCount(self.tempSubfolder)
            self.startOcr()
            self.currentTask = 'recognising'

        elif self.currentTask == 'recognising':
            if self.ocrDone():
                self.currentTask = 'combining'

        elif self.currentTask == 'combining':
            if self.outType == 'pdf':
                combinePdfs(self.pgCount, self.tempSubfolder, self.fileName + '-OCR.pdf')
            else:
                combineTxts(self.pgCount, self.tempSubfolder, self.fileName + '-OCR.txt')
            self.currentTask = 'finishing'

        elif self.currentTask == 'finishing':
            shutil.rmtree(self.tempSubfolder)
            self.currentTask = 'finished'  # Currently the 'finished' value isn't used, but it shows the intent better
            self.running = False

    def startConvert(self):
        outImgsPath = os.path.normpath(self.tempSubfolder + '/pg.png')  # Will save as 'pg-*.png'
        self.cnvrtSbProc = subprocess.Popen(['convert -density 300 "' + self.fileName + '" "' + outImgsPath + '"'],
                                            shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        self.pgCount = getImageCount(self.tempSubfolder)

    def startOcr(self):
        if self.pgCount == 1:
            imageLoc = os.path.normpath(self.tempSubfolder + '/pg.png')  # Get the image's filename
            sbPc = subprocess.Popen(['tesseract "' + imageLoc + '" "' + imageLoc + '" ' + self.outType],  # Begin OCR
                                    shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            self.tessSubProcesses.append(sbPc)  # Append the subprocess to a list so we can keep track of it
        else:
            for i in range(self.pgCount):
                imageLoc = os.path.normpath(self.tempSubfolder + '/pg-' + str(i) + '.png')  # Get the image's filename
                sbPc = subprocess.Popen(['tesseract "' + imageLoc + '" "' + imageLoc + '" ' + self.outType],  # Begin OCR
                                           shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                self.tessSubProcesses.append(sbPc)  # Append the subprocess to a list so we can keep track of it

    def ocrDone(self):
        """True if all 'tessSubProcesses' entries are done, False otherwise."""
        done = True
        for subProc in self.tessSubProcesses:
            if subProc.poll() is None:  # The process is running if it has no return code yet
                done = False
                break
        return done

def combinePdfs(pCount, tempPath, outPath):
    if pCount == 1:
        os.rename(os.path.normpath(tempPath + '/pg.png.pdf'), outPath)
    else:
        merger = PyPDF2.PdfFileMerger()  # New PDF
        for i in range(pCount):
            pdfPath = os.path.normpath(tempPath + "/pg-" + str(i) + ".png.pdf")
            merger.append(pdfPath)
            os.remove(pdfPath)  # Delete the file after it's been appended
        merger.write(outPath)

def combineTxts(pCount, tempPath, outPath):
    if pCount == 1:
        os.rename(os.path.normpath(tempPath + '/pg.png.txt'), outPath)
    else:
        outF = open(outPath, 'a')
        for i in range(pCount):
            txtPath = os.path.normpath(tempPath + "/pg-" + str(i) + ".png.txt")
            inF = open(txtPath)
            outF.write(inF.read())
            inF.close()
            os.remove(txtPath)  # Delete the file after it's been appended
        outF.close()

def getImageCount(folder):
    files = os.listdir(folder)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    pgCount = len(files)  # The number of pages is the number of files
    return pgCount



'''


    def processFile(self):
        self.pgCount = pdfToImages(self.fileName, self.tempSubfolder)
        self.ocrImages()

    def ocrImages(self):
        for i in range(self.pgCount):
            imageLoc = os.path.normpath(self.tempSubfolder + '/pg-' + str(i) + '.png')
            subProc = subprocess.Popen(['tesseract "' + imageLoc + '" "' + imageLoc + '" ' + self.outType], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            self.tessSubProcesses.append(subProc)

    def updateRunningStatus(self):
        """To be called by the gui on 'tick' or update, otherwise, if we just used a loop with .wait()s,
        the whole program would get stuck on one ocrCore. This method checks what is running, starts the next
        step of the process if needed, and sets the 'running' variable to False when everything is done."""


        newRunningStatus = False
        for subProc in self.tessSubProcesses:
            if subProc.poll() is None:
                newRunningStatus = True
                break
        self.running = newRunningStatus




def pdfToImages(inPdfPath, outDir):
    outImgsPath = os.path.normpath(outDir + '/pg.png') # Will save as 'pg-*.png'
    os.system('convert -density 300 "' + inPdfPath + '" "' + outImgsPath + '"')
    return getImageCount(outDir)
'''