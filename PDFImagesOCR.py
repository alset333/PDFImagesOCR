#!/usr/bin/env python3

import sys
import dependencyChecker
import platform

__author__ = 'Peter Maar'
__version__ = '0.8.0'  # Added a dependency checker

#TODO Better Windows support, check which versions of Windows have trouble -- is it only certain ones?

# OS Support Table:
#   Version |   Status
#----------------------------
#   Win-XP  |   Unsupported. Broken in multiple places
#   Win-Vst |   ?
#   Win-7   |   ?
#   Win-8   |   ?
#   Win-8.1 |   ?
#   Win-10  |   ?
#-----------------------------
#   Mac-Yos |   Full Support
#   Mac-ElC |   ?

if platform.system() == 'Windows':
    yn = ''
    while yn != 'y' and yn != 'n':
        yn = input('Windows is currently not very well supported, and the program may not function as intended or expected.\nDo you wish to continue? (y/n)\n').lower()
    if yn != 'y':
        exit()

DEBUGMODE = False

useGui = len(sys.argv) == 1  # If the only argument is the program itself, run the GUI

d = dependencyChecker.dCheckr()

d.check()

if DEBUGMODE:
    print(d.reason)

if useGui:  # Use GUI
    import gui  # Only import if needed, especially important if they're headless with no tkinter installed
    if d.dpndOk():
        g = gui.Gui()
    else:
        g = gui.Gui(reason='Error, one or more dependencies are not configured correctly.\n' + d.reason)
        exit()

elif d.dpndOk():  # Not GUI, but dependencies are fine
    import cli  # Only import if needed,
    c = cli.Cli(sys.argv)  # Run the CLI with the arguments

else:  # Not GUI, and dependencies are not fine
    print('Error, one or more dependencies are not configured correctly.\n' + d.reason)
    exit()
