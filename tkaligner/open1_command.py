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
from longtime_job import longtime_job

# SIG_TABLE = blinker.signal("table")
SIG_PAD = blinker.signal("pad")


# pylint: disable=invalid-name
# self is Aligner in aligner_ui
def open1_command(self, file12="file1", event=None):  # pylint: disable=unused-argument
    """ open1. """
    logger.debug("savetmx_command")

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
            self.text1, _ = load_paras(file)
        except ValueError:
            self.text1 = load_paras(file)

        # root.wm_title(file.name + " : Zen Text Editor")
        # self.text.insert('1.0', contents)
        logger.debug("self.text1[:3]: %s", self.text1[:3])

        # file.close()

    # detect, ask and separate
    text1 = "\n".join(self.text1)

    s_or_d = single_or_dual(text1)

    # self.text2 = ""

    if len(s_or_d) == 2:
        res = messagebox.askyesnocancel(
            f"Dual-language file or not", f"Tkaligner thinks this is a dual-language {s_or_d} file. Do you want to treat it as such?",
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
            thr.start()

            # refer to paligner.py self is Aligner

            rt = self.top

            # top = Pbar(rt)  # this does not work
            top = tk.Toplevel(rt)
            pbar = Pbar(top)

            pbar.TProgressbar1.start(50)

            # check_thread_update1(thr, top, pbar)
            check_thread_update1(thr, pbar)

            # update table via slot_table in text_to_plist
            # blinker.signal("table").send(df=df_data)
            # self.Table.model.df = DataFrame(p_list, columns=["text1", "text2", "merit"])

            return

        else:  # user opts for single-lang  # left: self.text1 part
            values = self.text1

            df = self.Table.model.df
            df.columns = ["text1", "text2", "merit"]
            df = insert_column(values, df, 0)
            self.Table.model.df = df
            # left: self.text1 part
            values = self.text1

            df = self.Table.model.df
            df.columns = ["text1", "text2", "merit"]
            df = insert_column(values, df, 0)
            self.Table.model.df = df

            # reset merit
            self.Table.model.df.merit = ""
    else:
        # left: self.text1 part
        values = self.text1

        df = self.Table.model.df
        df.columns = ["text1", "text2", "merit"]
        df = insert_column(values, df, 0)
        self.Table.model.df = df

        # reset merit
        self.Table.model.df.merit = ""

        # logger.debug(self.Table.model.df)
        # data = extract_rows(self.Table.model.df, 0)

    data = extract_rows(self.Table.model.df, self.Table.row_clicked)
    logger.debug("data sent to SIG_PAD.send(data=data): %s", data)

    # SIG_TABLE.send(data=data)
    SIG_PAD.send(data=data)

    self.Table.show()
    self.Table.redraw()
