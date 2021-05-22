"""
quit_command.
"""
# import sys
# from pathlib import Path
import atexit

import tkinter as tk
from tkinter import messagebox

# import tkinter.ttk as ttk

import logzero
from logzero import logger

# from aligner_ui import Aligner
# import aligner_ui_support

# from extract_rows import extract_rows

# SIG_TABLE = blinker.signal("table")


def quit_command(self, event=None):  # pylint: disable=unused-argument
    """ quit_command. """
    logger.debug("quit_command")

    if event:
        logger.debug(event)
        print("\n\tThat's rough, but it works nevertheless.\n\n")
        # win = tk.Tk()
        # win.withdraw()
        # messagebox.showinfo("Oh man...", "That's rough, but it works nevertheless.")

        self.top.quit()
        # return None

    # if tkMessageBox.askokcancel(
    if messagebox.askokcancel("Quit ", "Do you really want to quit?"):
        # self.top.destroy()  # self.top is root = tk.Tk()
        # atexit.unregister(quit_command)
        self.top.quit()  # self.top is root = tk.Tk()
