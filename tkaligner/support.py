"""
aligner_ui_support.py

def onAbout(event=None):
    print("aligner_ui_support.onAbout")
    sys.stdout.flush()

def onHowto(event=None):
    print("aligner_ui_support.onHowto")
    sys.stdout.flush()
"""
# pylint: disable=missing-docstring

import os
import sys
from pathlib import Path
from itertools import zip_longest

import tkinter as tk
from tkinter import messagebox
from textwrap import TextWrapper

import blinker
import logzero
from logzero import logger

from __init__ import __version__

# from bee_aligner.color_table_applymap import color_table_applymap

# from extract_rows import extract_rows

SIG_TABLE = blinker.signal("table")

_ = """  # comment this to set debug for this file
from logzero import setup_logger
logger = setup_logger(
    name=__file__,
    level=10,
)
logger.debug("hello")
# """


def on_howto(event=None):  # pylint: disable=unused-argument
    # print("aligner_ui_support.onAbout")
    # sys.stdout.flush()
    msg = """
        In brief

        1. Load files or paste content from system clipbaord: from menu/File (or use shortcuts Ctrl-O and Ctrl-N)

        2. Para-Align: from menu/Edit (shortcut Ctrl-P)
            * When the popup windows shows up: adjust Threshold from the spinbox and click Start
            * Manipulate the upper table to your satisfaction
            * Click Back to return

        3. Sent-Align: from menu/Edit (shortcut Ctrl-S)
            * Manipulate the upper table to your satisfaction: Use Ctr-A/Ctr-C/Ctr-X/Ctr-X (Select-All/Copy/Cut/Paste) in the upper table for editing.

        4. Save as csv, TMX ot xlsx: from menu/File (shortcuts: Ctrl-T or Ctrl-L)

        Consult the readme file in Chinese included in the package or join qq-group 316287378 to ask questions you may have.

    """
    width = 50
    tr0 = TextWrapper(
        width=width,
        replace_whitespace=False,
        # drop_whitespace=False,
        initial_indent="",
        subsequent_indent=" " * 3,
    )

    tr1 = TextWrapper(
        width=width,
        replace_whitespace=False,
        # drop_whitespace=False,
        initial_indent=" " * 5,
        subsequent_indent=" " * 7,
    )

    msg_v = [elm.strip() for elm in msg.splitlines() if elm.strip()]

    # map_v = [tr0.fill] * 3 + [tr1.fill] * 3 + [tr0.fill] + [tr1.fill] + [tr0.fill] * 3
    # map_ = lambda x, y: map(lambda e: e[0](e[1]), zip_longest(x, y))  # noqa: E731
    # msg_lst = map_(map_v, msg_v)
    # msg = "\n\n".join(msg_lst)

    msg = "\n\n".join(tr1.fill(elm) if elm.startswith("*") else tr0.fill(elm) for elm in msg_v)

    # top = tk.Toplevel()

    top = tk.Tk()
    top.withdraw()
    iconpath = Path(__file__).parent / "align.ico"
    top.iconbitmap(default=iconpath)
    # top.iconbitmap(default="align.ico")
    messagebox.showinfo("Howto", msg, parent=top)


def on_about(event=None):  # pylint: disable=unused-argument
    # print("aligner_ui_support.onHowto")
    sys.stdout.flush()
    msg = """
        An aligner for translation memory and parallel corpora

        Brought to you from mu's desk (@qq41947782) in cyberspace, last edited on 1 Nov. 2019 and 30 Jul. 2020

        © 2020 mu All Rights Reserved
    """
    width = 50
    tr0 = TextWrapper(
        width=width,
        replace_whitespace=False,
        # drop_whitespace=False,
        initial_indent="",
        subsequent_indent=" " * 0,
    )

    msg_v = [elm.strip() for elm in msg.splitlines() if elm.strip()]
    map_v = [tr0.fill] * 3

    map_ = lambda x, y: map(lambda e: e[0](e[1]), zip(x, y))  # noqa: E731
    msg_lst = map_(map_v, msg_v)
    msg = "\n\n".join(msg_lst)

    # top = tk.Toplevel()
    top = tk.Tk()
    top.withdraw()
    iconpath = Path(__file__).parent / "align.ico"
    top.iconbitmap(default=iconpath)
    # top.iconbitmap(default="align.ico")
    # messagebox.showinfo(f"About Tkalinger v.0.0.6a", msg, parent=top)
    messagebox.showinfo(f"About Tkalinger {__version__}", msg, parent=top)
