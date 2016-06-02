#!/usr/bin/env python3

import sys
import dependencyChecker

__author__ = 'Peter Maar'
__version__ = '0.8.0'  # Added a dependency checker

DEBUGMODE = False

useGui = len(sys.argv) == 1  # If the only argument is the file, run the GUI

d = dependencyChecker.dCheckr()

d.check()

if DEBUGMODE:
    print(d.reason)

if useGui:  # Use GUI
    import gui  # Only import if needed, especially important if they're headless with no tkinter installed
    if d.dpndOk():
        g = gui.Gui()
    else:
        g = gui.Gui(reason=d.reason)

elif d.dpndOk():  # Not GUI, but dependencies are fine
    import cli  # Only import if needed,
    c = cli.Cli(sys.argv)  # Run the CLI with the arguments

else:  # Not GUI, and dependencies are not fine
    print(d.reason)
