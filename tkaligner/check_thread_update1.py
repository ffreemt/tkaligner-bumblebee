""" check thread and update pbar via QUEUE.
Used in association with myprogressbar_ui
"""
import os
import tkinter as tk
import logzero
from logzero import logger

# from queues import QUEUE, QUEUE_C
# import myprogressbar_ui_support1

# myprogressbar_ui_support.set_Tk_var()


# def check_thread_update1(thr, win, pbar):
def check_thread_update1(thr, pbar):
    """ check thread thr and update pbar via QUEUE. """

    # logger.debug(" thr.ident: %s", thr.ident)
    # pbar = win.pbar

    if thr.is_alive():
        # logger.debug("+++ check_threa_update1 %s, thr.ident: %s, ++alive++ ", thr.name, thr.ident)

        # pbar.TProgressbar1.step()

        # pbar.TProgressbar1.after(500, lambda: check_thread_update1(thr, win, pbar))

        pbar.TProgressbar1.after(500, lambda: check_thread_update1(thr, pbar))

    else:
        logger.debug("+++ check_threa_update1 %s ++not alive++ ", thr.name)

        # pbar.destroy()  # 'Pbar' object has no attribute 'destroy'

        # win.destroy()
        try:
            pbar.top.destroy()
        except Exception as exc:
            logger.error(" pbar.top.destroy() exc: %s", exc)

        # pbar.TButton1.config(state=tk.NORMAL)
        # pbar.TButton2.config(state=tk.DISABLED)
        # pbar.TButton3.config(state=tk.NORMAL)

        # windows.pbar.Cancel.config(state=tk.DISABLED)

    # pbar.TProgressbar1.destroy(): cant do this
    # logger.debug("  exit ")
