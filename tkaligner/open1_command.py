"""
open1_command
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
def open1_command(self, file12="file1", event=None):  # pylint: disable=unused-argument
    """ open1. """
    logger.debug("open1_command")

    if file12 in ["file1"]:  # file1 or file2, not implemented yet
        ...

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

        # self.text1 = file.read()
        try:
            try:
                text1, _ = load_paras(file)
            except ValueError:
                text1 = load_paras(file)
        except Exception as exc:
            logger.error("exc: %s", exc)
            text1 = []

        if not " ".join(text1).strip():
            messagebox.showwarning(" Empty text", "Nothing loaded, we just exit. ")
            return None

        self.text1 = text1[:]

        logger.debug("self.text1[:3]: %s", self.text1[:3])

        # file.close()

    # detect, ask and separate
    text1 = "\n".join(self.text1)

    s_or_d = single_or_dual(text1)

    # self.text2 = ""

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
            blinker.signal("aligner").send("open1_comman", pbtoplevel="True")  # SIG_ALIGNER.send

            # update table via slot_table in text_to_plist
            # blinker.signal("table").send(df=df_data)
            # self.Table.model.df = DataFrame(p_list, columns=["text1", "text2", "merit"])

            # self.filename1 = file
            # self.filename2 = file
            # self.text1 = "\n".join(self.Table.model.df.text1)
            # self.text2 = "\n".join(self.Table.model.df.text2)

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