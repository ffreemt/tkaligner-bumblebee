""" palign_command. """

import tkinter as tk

from logzero import logger

from myprogressbar_ui import Mypbar
import myprogressbar_ui_support


def palign_command(self, event=None):
    """ palign_command. """
    logger.debug("palign_command")

    top = self.top
    # top = None

    window = tk.Toplevel(top)
    # window = tk.Toplevel(self) does not work

    # refer to open_settings_window.py

    myprogressbar_ui_support.set_Tk_var()

    # QUEUE_SPINBOX.put('*')
    pbar = Mypbar(window)
    # pbar = Mypbar(self)

    # disbale cancel butt until start is clicked
    # TButton 1: Start, 2: Cancel,3: Back
    pbar.TButton2.config(state=tk.DISABLED)

    window.focus_force()
    window.grab_set()
    return None