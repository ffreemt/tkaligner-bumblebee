""" salign_command. """

import os
import tkinter as tk
from queue import Empty

import logzero
from logzero import logger

from myprogressbar_ui import Mypbar
import myprogressbar_ui_support

from queue1_put import queue1_put
from queues import QUEUE_PS, QUEUE_PS0, QUEUE_DF

_ = os.environ.get("ALIGNER_DEBUG")
if _ is not None and _.lower() in ["1", "true"]:
    logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
else:
    logzero.loglevel(20)
logger.debug('os.environ.get("ALIGNER_DEBUG"): %s', _)


def salign_command(self, event=None):
    """ salign_command. """
    logger.info("salign_command")

    try:
        _ = QUEUE_PS.get_nowait()
    except Empty:
        _ = ""
    queue1_put(QUEUE_PS, _)  # restore

    # send model.df to QUEUE_DF
    logger.debug("sending Table.model.df to QUEUE_DF")
    QUEUE_DF.append(self.Table.model.df)

    # QUEUE_PS0 pervious state of QUEUE_PS
    QUEUE_PS0.append(_)  # pervious state of QUEUE_PS

    # this is only for selecting check_thread_update
    queue1_put(QUEUE_PS, "s")

    top = self.top
    # top = None

    self.pbtoplevel = tk.Toplevel(top)
    # window = tk.Toplevel(top)
    # window = tk.Toplevel(self) does not work

    # refer to open_settings_window.py

    myprogressbar_ui_support.set_Tk_var()

    # QUEUE_SPINBOX.put('*')
    # pbar = Mypbar(self)
    # pbar = Mypbar(window)
    pbar = Mypbar(self.pbtoplevel)

    # disable Spinbox
    pbar.Spinbox1.config(state=tk.DISABLED)

    # disbale cancel butt until start is clicked
    # TButton1: Start, 2: Cancel,3: Back
    pbar.TButton2.config(state=tk.DISABLED)

    # window.focus_force()
    # window.grab_set()
    self.pbtoplevel.grab_set()

    logger.debug(" salign_command exit ")

    return None
