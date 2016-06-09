#!/usr/bin/env python3

from tkinter.filedialog import *
import platform
import ocrCore

__author__ = 'Peter Maar'
__version__ = '0.1.0'

DEBUGMODE = False


class Gui:
    def __init__(self, reason=None):
        """The GUI. If sent an error 'reason', it will display the reason and not load anything else."""
        if platform.system() == 'Darwin':
            os.system("""sleep 1 && osascript -e 'tell app "Python" to activate' &""")  # Seems to get stuck forever for some reason, but doesn't seem to be running? either way '&' isn't a good solution but it seems to be the easiest by far

        self.root = Tk()  # Tk object
        self.root.title("PDFImagesOCR")
        self.qdFlnms = []  # 'Queued' filenames
        self.ocrCores = []  # Objects for the files being processed
        self.outtype = 'pdf'

        # Canvases
        self.buttonCanvas = Canvas(self.root)
        self.buttonCanvas.pack()

        self.mainCanvas = Canvas(self.root)
        self.mainCanvas.pack()

        # Buttons
        self.exitButton = Button(self.buttonCanvas, text='Exit', command=self.cleanExit)
        self.exitButton.pack()

        if reason is not None:  # If it was sent a reason, something is wrong with the dependencies
            self.reasonLabel = Label(self.mainCanvas, text=reason)
            self.reasonLabel.pack()
            self.root.mainloop()  # Start the mainloop. The window will open, and none of the following code will run

        self.openFilesButton = Button(self.buttonCanvas, text='Open/Add Files', command=self.openFiles)
        self.openFilesButton.pack()

        self.processFilesButton = Button(self.buttonCanvas, text='Process Open Files', command=self.processFiles)
        self.processFilesButton.pack()

        self.outtype_stringvar = StringVar()
        self.outtype_stringvar.set('Output as txt (currently PDF)')
        self.outTypeButton = Button(self.buttonCanvas, textvariable=self.outtype_stringvar, command=self.toggleOutType)
        self.outTypeButton.pack()

        self.filenamesText = StringVar()
        self.filenamesLabel = Label(self.mainCanvas, textvariable=self.filenamesText)
        self.filenamesLabel.pack()

        self.updateAndCheckAll()  # Call the first time -- it will use '.after' to
        #                           call itself automatically after the first call


        self.root.mainloop()

    def cleanExit(self):
        for core in self.ocrCores:
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


    def toggleOutType(self):
        if self.outtype_stringvar.get() == 'Output as PDF (currently txt)':
            self.outtype_stringvar.set('Output as txt (currently PDF)')
            self.outtype = 'pdf'
        else:
            self.outtype_stringvar.set('Output as PDF (currently txt)')
            self.outtype = 'txt'

    def updateAndCheckAll(self):
        self.tickCores()

        self.updFnms()

        self.updFnmsDisp()

        self.root.after(500, self.updateAndCheckAll)

    def tickCores(self):
        """Calls 'updateTick()' on all the cores to update what they're doing."""
        for core in self.ocrCores:
            core.updateTick()

    def updFnms(self):
        """Updates the files loaded/running"""
        for ocrCore in self.ocrCores:  # Cycle through them
            if not ocrCore.running:  # If they are not processing it, remove the object
                self.ocrCores.remove(ocrCore)

    def updFnmsDisp(self):
        """Updates the files shown"""
        self.filenamesText.set('')  # Clear current text

        if len(self.qdFlnms) > 0:  # If there are filenames in the queue
            for name in self.qdFlnms:  # Cycle through them to display them
                self.filenamesText.set(self.filenamesText.get() + name + '\n')  # Add filename
            self.filenamesText.set(self.filenamesText.get()[:-1])  # Remove trailing '\n'
        else:  # Otherwise, report there are no queued files
            self.filenamesText.set('No files currently queued.')

        # Add spacing
        self.filenamesText.set(self.filenamesText.get() + '\n\n')

        if len(self.ocrCores) > 0:  # If there are filenames in the queue
            for ocrCore in self.ocrCores:  # Cycle through them to display them
                self.filenamesText.set(self.filenamesText.get() + ocrCore.currentTask + ': ' + ocrCore.fileName + '\n')  # Add filename
            self.filenamesText.set(self.filenamesText.get()[:-1])  # Remove trailing '\n'
        else:  # Otherwise, report there are no queued files
            self.filenamesText.set(self.filenamesText.get() + 'No files currently being processed.')

    def openFiles(self):
        # Open the files
        fls = askopenfiles(filetypes=[('PDF', "*.pdf")])
        if DEBUGMODE:
            print(fls)

        # Get the names and close the file objects
        for file in fls:
            if file.name not in self.qdFlnms:  # Only add it if it's not already in the list
                self.qdFlnms.append(file.name)
            file.close()

    def processFiles(self):
        # Process the files
        for filename in self.qdFlnms:
            self.ocrCores.append(ocrCore.Ocr(filename, self.outtype))

        self.qdFlnms = []
