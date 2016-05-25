#!/usr/bin/env python3

import sys

__author__ = 'Peter Maar'
__version__ = '0.7.0'  # Added CLI. There is now a GUI _and_ a CLI.

if len(sys.argv) == 1:  # If the only argument is the file, run the GUI
    import gui  # Only import if needed, especially important if they're headless with no tkinter
    g = gui.Gui()
else:                   # If there are other arguments, run the CLI with them
    import cli  # Only import if needed,
    c = cli.Cli(sys.argv)
