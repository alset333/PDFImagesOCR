#!/usr/bin/env python3

import os, tempfile, shutil
import time
import subprocess, multiprocessing

__author__ = 'Peter Maar'
__version__ = '0.1.0'

DEBUGMODE = False

# Each ocrCore will run a maximum of number of 'tesseract' processes equal to 3/4 the number of logical processors.
# This helps ensure the computer stays responsive while recognising large PDFs.
# Do be cautious though, as you may have multiple ocrCores despite this, causing the computer to slow regardless.
maxTessSubProcesses = 3 * multiprocessing.cpu_count() // 4


class Ocr:
    def __init__(self, filename, outtype):
        self.outType = outtype
        self.fileName = filename
        self.running = True
        self.tessSubProcesses = []
        self.queuedTessSubProcesses = []
        self.cnvrtSbProc = None
        self.tempSubfolder = os.path.normpath(tempfile.gettempdir() + '/PDFImagesOCR-TempFolder-' + str(time.time()) + filename[filename.rfind(os.path.normpath('/')) + 1:-4])  # time.time() helps for if two filenames are the same
        self.pgCount = 0  # Not known yet, will be set later.

        self.currentTask = 'startConvert'  # Start with starting the conversion of the PDF to PNGs

        if DEBUGMODE:
            print('ocrCore.Ocr\t\t', filename)

        os.mkdir(self.tempSubfolder)

    def updateTick(self):
        if self.currentTask == 'startConvert':
            self.startConvert()
            self.currentTask = 'converting'

        elif self.currentTask == 'converting':
            if self.cnvrtSbProc.poll() is not None:  # If it has a return code, it's done converting,
                self.currentTask = 'queueOcr'              # so start the OCR

        elif self.currentTask == 'queueOcr':
            self.pgCount = getImageCount(self.tempSubfolder)
            self.queueOcr()
            self.currentTask = 'recognising'

        elif self.currentTask == 'recognising':
            self.updateTessSubProcesses()
            if len(self.tessSubProcesses) == 0:  # When they're all done, go on to the next task
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

    def queueOcr(self):
        """Queues the tesseract subprocesses as commands in a list"""
        if self.pgCount == 1:
            imageLoc = os.path.normpath(self.tempSubfolder + '/pg.png')  # Get the image's filename
            self.queuedTessSubProcesses.append(['tesseract "' + imageLoc + '" "' + imageLoc + '" ' + self.outType])  # Append the subprocess to a list so we can keep track of it
        else:
            for i in range(self.pgCount):
                imageLoc = os.path.normpath(self.tempSubfolder + '/pg-' + str(i) + '.png')  # Get the image's filename
                self.queuedTessSubProcesses.append(['tesseract "' + imageLoc + '" "' + imageLoc + '" ' + self.outType])  # Append the subprocess to a list so we can keep track of it

    def updateTessSubProcesses(self):
        """Keeps up to the maximum tesseract subprocesses running and removes completed 'tessSubProcesses' entries."""
        if DEBUGMODE:
            print(self.queuedTessSubProcesses, '\n', self.tessSubProcesses)
        for command in self.queuedTessSubProcesses:
            if len(self.tessSubProcesses) < maxTessSubProcesses:
                self.queuedTessSubProcesses.remove(command)  # Remove the command from the queue
                sbPc = subprocess.Popen(command, shell=True, stdin=None,  # Run the command
                                        stdout=None, stderr=None, close_fds=True)
                self.tessSubProcesses.append(sbPc)
            else:
                break

        for subProc in self.tessSubProcesses:
            if subProc.poll() is not None:  # The process is running if it has no return code yet,
                                            # so this is true if it's not running
                self.tessSubProcesses.remove(subProc)


def combinePdfs(pCount, tempPath, outPath):
    import PyPDF2
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
