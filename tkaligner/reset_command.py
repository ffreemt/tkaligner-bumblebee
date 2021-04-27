""" reset_command. """

from tkinter import messagebox

from pandas import DataFrame

import blinker
from logzero import logger

from extract_rows import extract_rows
from queue1_put import queue1_put

from queues import (QUEUE_T1, QUEUE_T2,
                    QUEUE_P1, QUEUE_P2, QUEUE_PM,
                    QUEUE_S1, QUEUE_S2, QUEUE_SM,
                    QUEUE_PA, QUEUE_SA,
                    QUEUE_PS, )

SIG_PAD = blinker.signal("pad")


def reset_command(self, event=None):
    """ reset_command.

    self is aligner
    """
    logger.debug("reset_command")
    # sys.stdout.flush()

    res = messagebox.askyesnocancel(
        f"Reset everythin?", f"This will reset everything. Continue?",
        default="no",
        icon="question"
    )

    if not res:
        return None

    len_ = 5
    _ = zip(range(1, 1 + len_), range(1 + len_, 1 + len_ + len_), [""] * len_)
    df = DataFrame(_, columns=["text1", "text2", "merit"])

    self.Table.model.df = df

    _ = extract_rows(self.Table.model.df, self.Table.row_clicked)
    SIG_PAD.send(data=_)
    self.Table.show()
    self.Table.redraw()

    for elm in (QUEUE_T1, QUEUE_T2,
                    QUEUE_P1, QUEUE_P2, QUEUE_PM,
                    QUEUE_S1, QUEUE_S2, QUEUE_SM,
                    QUEUE_PA, QUEUE_SA,
                    QUEUE_PS, ):
        queue1_put(elm, "")

    self.filename1 = ""
    self.filename2 = ""
    self.text1 = ""
    self.text2 = ""
    self.paras1 = ""
    self.paras2 = ""
    self.paras_merit = ""
    self.sents1 = ""
    self.sents2 = ""
    self.sents_merit = ""
    self.paligned = False
    self.saligned = False

    logger.debug("reset df to: %s", df)
