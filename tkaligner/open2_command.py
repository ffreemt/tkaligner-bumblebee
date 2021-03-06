"""
open2_command.
"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import blinker
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
def open2_command(self, event=None):  # pylint: disable=unused-argument
    """ open2. """
    # from load_paras import load_paras

    logger.debug("<open2_command>")

    # from tkinter import filedialog
    # self.top = self
    # file = tk.filedialog.askopenfile(parent=root, mode='r', title='Select a file')

    # file = filedialog.askopenfile(parent=self.top, mode='r', title='Select a file')
    file = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(
            ("text files", "*.txt"),
            # ("pdf files", "*.pdf"),
            # ("docx files", "*.docx"),
            ("all files", "*.*"),
        ),
    )

    if file is not None:
        # self.text.delete('1.0', END)
        # self.text2 = file.read()

        try:
            try:
                text2, _ = load_paras(file)
            except ValueError:
                text2 = load_paras(file)
        except Exception as exc:
            logger.error("exc: %s", exc)
            text2 = []

        if not " ".join(text2).strip():
            messagebox.showwarning(" Empty text", "Nothing loaded, we just exit. ")
            return None

        self.text2 = text2[:]

        logger.debug("self.text2[:3]: %s", self.text2[:3])

        # file.close()

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