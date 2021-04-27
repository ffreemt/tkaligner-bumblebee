"""
open2_command.
"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import blinker
# import pyperclip
import logzero
from logzero import logger

# pylint: disable=wrong-import-position, import-error
# from aligner_ui import Aligner
# import aligner_ui_support

from load_paras import load_paras
from insert_column import insert_column
from extract_rows import extract_rows

from queue1_put import queue1_put
from queues import QUEUE_T2, QUEUE_P2

SIG_PAD = blinker.signal("pad")


# pylint: disable=
def paste2_command(self, event=None):  # pylint: disable=unused-argument
    """ paste2_command. """
    # from load_paras import load_paras

    logger.debug("<paste2_command>")

    # text2 = pyperclip.copy().strip()
    try:
        win = tk.Tk()
        win.withdraw()
        text2 = win.clipboard_get().strip()
    except Exception as exc:
        logger.error(" text2 = tk.Tk().clipboard_get() exc: %s", exc)
        text2 = str(exc)

    if not text2.strip():
        messagebox.showwarning(" Nothing in the clipboard ", "Copy something to the system clipbaord first and try again.")
        return None
    file = "clipboard2.txt" 
    
    # convert to para list
    # text2 = re.split(r"[\r\n]+", text2)
    text2 = [elm for elm in text2.splitlines() if elm.strip()]

    self.text2 = text2[:]

    logger.debug(" from clipboard self.text2[:3]: %s", self.text2[:3])

    # values = self.text2.split('\n')
    values = self.text2

    df = self.Table.model.df
    df.columns = ["text1", "text2", "merit"]
    df = insert_column(values, df, 1)

    # reset merit column to all ""
    df = insert_column([""] * df.shape[0], df, 2)
    # # cp_load_text2

    self.Table.model.df = df

    # reset merit
    # self.Table.model.df.merit = ""

    # logger.debug(self.Table.model.df)
    logger.debug("self.Table.model.df[:3]: %s", self.Table.model.df[:3])
    # send self.Table.model.df[:3] to PAD
    # SIG_TABLE.send(data=self.Table.model.df[:3])

    # data = extract_rows(self.model.df, self.row_clicked)
    # pretend row 0 clicked
    # data = extract_rows(self.Table.model.df, 0)

    data = extract_rows(self.Table.model.df, self.Table.row_clicked)
    # logger.debug("data sent to SIG_TABLE.send(data=data): %s", data)
    logger.debug("data sent to SIG_TABLE.send(data=data): %s", data)

    # SIG_TABLE.send(data=data)
    # update pad via slot_pad
    SIG_PAD.send(data=data)

    self.Table.show()
    self.Table.redraw()

    self.filename2 = file
    logger.debug(" setting filename2 *%s* and QUEUE_T2 self.text2[:3] %s", self.filename2, self.text2[:3])

    queue1_put(QUEUE_T2, self.text2)
    queue1_put(QUEUE_P2, self.text2)

    if self.text1 and self.text2:
        self.sub_menu1.entryconfig("PAlign", state="normal")
        logger.debug(""" enabling PAlign: logger.debug(" enabling PAlign ") """)