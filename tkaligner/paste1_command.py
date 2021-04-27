"""
paste1_command
"""

# import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pandas import DataFrame

import blinker
from threading import Thread
# import logzero
from logzero import logger

# from myprogressbar1_ui import Mypbar
from myprogressbar1_ui import Pbar
from check_thread_update1 import check_thread_update1

from load_paras import load_paras
from insert_column import insert_column
from extract_rows import extract_rows

# from bee_aligner.plist_to_slist import plist_to_slist
from bee_aligner.single_or_dual import single_or_dual
from bee_aligner.text_to_plist import text_to_plist
# from longtime_job import longtime_job

from queue1_put import queue1_put
from queues import QUEUE_T1, QUEUE_P1

SIG_PAD = blinker.signal("pad")


# pylint: disable=invalid-name
# self is Aligner in aligner_ui
def paste1_command(self, file12="file1", event=None):  # pylint: disable=unused-argument
    """ paste1. """
    logger.debug("paste1_command")


    # text2 = pyperclip.copy().strip()
    # text1 = pyperclip.copy().strip()
    try:
        win = tk.Tk()
        win.withdraw()
        text1 = win.clipboard_get().strip()
    except Exception as exc:
        logger.error(" text1 = tk.Tk().clipboard_get() exc: %s", exc)
        text1 = str(exc)

    if not text1.strip():
        messagebox.showwarning(" Nothing in the clipboard ", "Copy something to the system clipbaord first and try again.")
        return None
    file = "clipboard1.txt"

    # convert to para list
    # text1 = re.split(r"[\r\n]+", text1)
    text1 = [elm for elm in text1.splitlines() if elm.strip()]

    self.text1 = text1[:]

    logger.debug("self.text1[:3]: %s", self.text1[:3])

    # detect, ask and separate
    # text1 = "\n".join(self.text1)

    s_or_d = single_or_dual(text1)

    if len(s_or_d) == 2:  # dualtext
        res = messagebox.askyesnocancel(
            f"Dual-language file or not", f"Tkaligner thinks this is a dual-language {s_or_d} file. Do you want to treat it as such? (If you press Yes, it will take about two minutes to process the file.)",
            default="yes",
            icon="question"
        )

        logger.debug(" res = messagebox.askyesnocancel: res %s" , res)

        if res is None:
            return

        if res:  # handle bilingual text
            # bumblebee_aligner st-bee-aligner.py
            # p_list = text_to_plist(src_file, langs=s_or_d)

            # may need an indeterminate progressbar
            # p_list = text_to_plist(text1, langs=s_or_d)
            thr = Thread(
                target=text_to_plist,
                args=(text1,),
                # kwargs=dict(langs=s_or_d),
                kwargs={"langs": s_or_d},
                # target=longtime_job,
                # kwargs={"counter": 16},
                # name='job_thr',
            )
            thr.stop = False  # type: ignore

            # prepare for check_thread_update1
            # to set self.filename1/2 when successfully run
            thr.filename1 = file  # type: ignore
            thr.filename2 = file  # type: ignore

            thr.start()

            # refer to paligner.py self is Aligner

            rt = self.top

            # top = Pbar(rt)  # this does not work
            top = tk.Toplevel(rt)
            pbar = Pbar(top)

            pbar.TProgressbar1.start(50)

            # check_thread_update1(thr, top, pbar)
            # check_thread_update1(thr, pbar)
            check_thread_update1(self, thr, pbar)

            # disable Pad editing
            blinker.signal("aligner").send("paste1_comman", pbtoplevel="True")  # SIG_ALIGNER.send

            return None

        else:  # user opts for single-lang  # left: self.text1 part
            values = self.text1

            df = self.Table.model.df
            df.columns = ["text1", "text2", "merit"]
            df = insert_column(values, df, 0)

            # reset merit column to all ""
            df = insert_column([""] * df.shape[0], df, 2)
            # cp_load_text1

            self.Table.model.df = df
            # left: self.text1 part
            # self.filename1 = file

    else:  # single-lang, normal
        # left: self.text1 part
        values = self.text1

        df = self.Table.model.df
        df.columns = ["text1", "text2", "merit"]
        df = insert_column(values, df, 0)

        # reset merit column
        # self.Table.model.df.merit = ""
        df = insert_column([""] * df.shape[0], df, 2)
        # cp_load_text1

        self.Table.model.df = df

        # logger.debug(self.Table.model.df)
        # data = extract_rows(self.Table.model.df, 0)

    data = extract_rows(self.Table.model.df, self.Table.row_clicked)
    logger.debug("data sent to SIG_PAD.send(data=data): %s", data)

    # SIG_TABLE.send(data=data)
    SIG_PAD.send(data=data)

    self.Table.show()
    self.Table.redraw()

    self.filename1 = file

    # logger.debug(" setting filename1 and QUEUE_T1")
    # logger.debug(" setting filename1 *%s* and QUEUE_T2", self.filename1)
    logger.debug(" setting filename1 *%s* and QUEUE_T1 self.text1[:3] %s", self.filename1, self.text1[:3])

    queue1_put(QUEUE_T1, self.text1)
    queue1_put(QUEUE_P1, self.text1)

    if self.text1 and self.text2:
        self.sub_menu1.entryconfig("PAlign", state="normal")
        logger.debug(""" enabling PAlign: logger.debug(" enabling PAlign ") """)