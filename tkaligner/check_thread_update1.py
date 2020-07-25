""" check thread and update pbar via QUEUE.
Used in association with myprogressbar_ui
"""
# import os
# import tkinter as tk
from pandas import DataFrame

# import blinker

# import logzero
from logzero import logger

# from queues import QUEUE, QUEUE_C
# import myprogressbar_ui_support1

# myprogressbar_ui_support.set_Tk_var()
# SIG_FILENAMES = blinker.signal("filenames")  # handler in aligner_ui not implemented


# def check_thread_update1(thr, win, pbar):
# def check_thread_update1(thr, pbar):
def check_thread_update1(self, thr, pbar):
    """ check thread thr and update pbar via QUEUE.

    called in open1_command
    self is aligner
    """

    # logger.debug(" thr.ident: %s", thr.ident)
    # pbar = win.pbar

    if thr.is_alive():
        # logger.debug("+++ check_threa_update1 %s, thr.ident: %s, ++alive++ ", thr.name, thr.ident)

        # pbar.TProgressbar1.step()

        # pbar.TProgressbar1.after(500, lambda: check_thread_update1(thr, win, pbar))

        pbar.TProgressbar1.after(500, lambda: check_thread_update1(self, thr, pbar))

    else:  # thr no longer alive, finished aligned
        logger.debug("+++ check_threa_update1 %s ++not alive++ ", thr.name)

        # thr.filename1/2 defined in open1_command.py
        self.filename1 = thr.filename1
        self.filename2 = thr.filename2

        # thr.p_list defined in text_to_plist thr.res
        p_list = thr.p_list
        _ = DataFrame(p_list)
        logger.debug(" DataFrame(p_list).head(3): %s", _.head(3))

        self.paras1 = _[0]
        self.paras2 = _[1]
        self.paras_merit = _[2]
        self.text1 = "\n".join(self.paras1)
        self.text2 = "\n".join(self.paras2)
        self.paligned = True

        # probably to cumbersome
        # SIG_FILENAMES.sender(filename1=thr.filename1)
        # SIG_FILENAMES.sender(filename2=thr.filename2)

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

        # need a signal-slot or a QUEUE?
        # self.text1 = "\n".join(self.Table.model.df.text1)
        # self.text2 = "\n".join(self.Table.model.df.text2)

    # pbar.TProgressbar1.destroy(): cant do this
    # logger.debug("  exit ")
