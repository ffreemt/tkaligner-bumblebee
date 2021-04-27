""" check thread and update pbar via QUEUE.
Used in association with myprogressbar_ui
"""

import os
# import tkinter as tk

from tkinter import messagebox
from pandas import DataFrame

import blinker

import logzero
from logzero import logger

# from queues import QUEUE, QUEUE_C
# import myprogressbar_ui_support1
from queues import (QUEUE_PA, QUEUE_P1, QUEUE_P2, QUEUE_PM,
                    QUEUE_T1, QUEUE_T2, QUEUE_PS)
from queue1_put import queue1_put

# myprogressbar_ui_support.set_Tk_var()
# SIG_FILENAMES = blinker.signal("filenames")  # handler in aligner_ui not implemented

SIG_ALIGNER = blinker.signal('aligner')

_ = os.environ.get("ALIGNER_DEBUG")
if _ is not None and _.lower() in ["1", "true"]:
    logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
else:
    logzero.loglevel(20)
logger.debug('os.environ.get("ALIGNER_DEBUG"): %s', _)


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

    else:  # not thr.is_alive(), finished aligning
        logger.debug("+++ check_threa_update1 %s ++not alive++ ", thr.name)

        # thr.filename1/2 defined in open1_command.py
        self.filename1 = thr.filename1
        self.filename2 = thr.filename2

        # thr.p_list defined in text_to_plist thr.res
        try:
            p_list = thr.p_list
        except Exception as exc:
            logger.error("p_list = thr.p_list exc: %s", exc)
            # win.destroy()
            try:
                pbar.top.destroy()
            except Exception as exc1:
                logger.error(" pbar.top.destroy() exc: %s", exc1)

            messagebox.showerror("Bummer!", f" Oh no, sh*t happens too often: {exc} ")
            return None

        # _ = DataFrame(p_list)
        df = DataFrame(p_list)
        # logger.debug(" DataFrame(p_list).head(3): %s", df.head(3))

        self.paras1 = df[0]
        self.paras2 = df[1]
        self.paras_merit = df[2]
        # self.text1 = "\n".join(self.paras1)
        # self.text2 = "\n".join(self.paras2)

        queue1_put(QUEUE_P1, self.paras1)
        queue1_put(QUEUE_P2, self.paras2)
        queue1_put(QUEUE_PM, self.paras_merit)

        # QUEUE_T1/2 only needed for first
        # palign_command/myprogressbar1/thread
        # queue1_put(QUEUE_T1, self.text1)
        # queue1_put(QUEUE_T2, self.text2)

        self.paligned = True
        queue1_put(QUEUE_PA, True)

        # QUEUE_PS also for another purpose:
        # controls branching in check_thread_update
        # self.Table.model.df currently is paras1/2/_merit
        queue1_put(QUEUE_PS, 'p')  # update QUEUE_PS

        # cp_p
        logger.info("update: self.paras1/2/_merit, Q_P1/2/M self.text1/2, Q_T1/2 self.paligned/Q_PA ")
        logger.info("paras aligning completed.")

        # need a way to disable  "PAlign" enable "SAlign"
        # blinker.signal("PAlign")? blinker.signal("SAlign")
        # self.sub_menu1.entryconfig("PAlign", state="disabled")
        logger.debug("""send blinker.signal to aligner slot:
                {"PAlign": False, "SAlign": True,}""")
        SIG_ALIGNER.send(
            "check_thread_update1",
            **{
                "PAlign": False,
                "SAlign": True,
                "pbtoplevel": False,  # grab_release, not really needed since pbar1 will be destroyed when done?
            }
        )
        logger.debug(" <check_thread_update1> exit")

        # probably too cumbersome
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
