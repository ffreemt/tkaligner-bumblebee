""" palign_command. """

import os
import tkinter as tk
from queue import Empty

import logzero
from logzero import logger

from myprogressbar_ui import Mypbar
import myprogressbar_ui_support

from queue1_put import queue1_put
from queues import QUEUE_PS, QUEUE_PS0

_ = os.environ.get("ALIGNER_DEBUG")
if _ is not None and _.lower() in ["1", "true"]:
    logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
else:
    logzero.loglevel(20)
logger.debug('os.environ.get("ALIGNER_DEBUG"): %s', _)


def palign_command(self, event=None):
    """ palign_command. """
    logger.debug("palign_command")

    try:
        _ = QUEUE_PS.get_nowait()
    except Empty:
        _ = ""
    queue1_put(QUEUE_PS, _)  # restore

    # QUEUE_PS0 no longer used, paligner disabled after 1st use
    # queue1_put(QUEUE_PS0, _)  # pervious state of QUEUE_PS
    QUEUE_PS0.append(_)  # pervious state of QUEUE_PS

    # mark QUEUE_PS as "p"
    queue1_put(QUEUE_PS, "p")

    top = self.top
    # top = None

    self.pbtoplevel = tk.Toplevel(top)
    # window = tk.Toplevel(top)
    # window = tk.Toplevel(self) does not work

    # refer to open_settings_window.py

    myprogressbar_ui_support.set_Tk_var()

    # QUEUE_SPINBOX.put('*')
    # pbar = Mypbar(window)
    pbar = Mypbar(self.pbtoplevel)
    # pbar = Mypbar(self)

    # disbale cancel butt until start is clicked
    # TButton 1: Start, 2: Cancel,3: Back
    pbar.TButton1.config(state=tk.NORMAL)
    pbar.TButton3.config(state=tk.NORMAL)
    pbar.TButton2.config(state=tk.DISABLED)

    logger.debug(" disable PAlign ")
    self.sub_menu1.entryconfig("PAlign", state="disabled")
    # logger.debug(" disable Pad ")
    # self.Pad.config(state="disabled")  # cant do this with Pad (Frame)

    # window.focus_force()
    self.pbtoplevel.focus_force()
    # window.grab_set()

    logger.debug(" palign_command exit ")

    return None
