"""
quit_command.
"""
# import sys
# from pathlib import Path

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
    """ x_command. """
    logger.info("quit_command.py")

    if event:
        logger.debug(event)
    # if tkMessageBox.askokcancel(
    if messagebox.askokcancel("Quit ", "Do you really want to quit?"):
        # self.top.destroy()  # self.top is root = tk.Tk()
        self.top.quit()  # self.top is root = tk.Tk()

