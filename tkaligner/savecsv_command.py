""" savecsv_command."""

import os
from pathlib import Path
from pandas import DataFrame

from tkinter import messagebox
import logzero
from logzero import logger
# from loguru import logger as logger1

from bee_aligner.gen_filename import gen_filename
from bee_aligner.common_prefix import common_prefix

from queue import Empty
from queue1_put import queue1_put
from queues import (QUEUE_PA, QUEUE_SA,
                    QUEUE_P1, QUEUE_P2, QUEUE_S1, QUEUE_S2,
                    QUEUE_PM, QUEUE_SM)

logger = logzero.setup_logger(name=__file__, level=10)

_ = os.environ.get("ALIGNER_DEBUG")
logger.info('os.environ.get("ALIGNER_DEBUG"): %s', _)
if _ is not None and _.lower() in ["1", "true"]:
    logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
else:
    logzero.loglevel(20)


def savecsv_command(self, event=None) -> None:
    """ savecsv_command.
    self is aligner
    self.Table.model.df: DataFrame of interest

    self.filename1, self.filename2

    """

    # check QUEUE_PA QUEUE_SA
    try:
        self.paligned = QUEUE_PA.get_nowait()
        queue1_put(QUEUE_PA, self.paligned)
    except Empty:
        self.paligned = False
    try:
        self.saligned = QUEUE_SA.get_nowait()
        queue1_put(QUEUE_SA, self.saligned)
    except Empty:
        self.saligned = False

    if QUEUE_P1.qsize():
        self.paras1 = QUEUE_P1.get_nowait()
        queue1_put(QUEUE_P1, self.paras1)
    if QUEUE_P2.qsize():
        self.paras2 = QUEUE_P2.get_nowait()
        queue1_put(QUEUE_P2, self.paras2)
    if QUEUE_PM.qsize():
        self.paras_merit = QUEUE_PM.get_nowait()
        queue1_put(QUEUE_PM, self.paras_merit)
    if QUEUE_S1.qsize():
        self.sents1 = QUEUE_S1.get_nowait()
        queue1_put(QUEUE_S1, self.sents1)
    if QUEUE_S2.qsize():
        self.sents2 = QUEUE_S2.get_nowait()
        queue1_put(QUEUE_S2, self.sents2)
    if QUEUE_SM.qsize():
        self.sents_merit = QUEUE_SM.get_nowait()
        queue1_put(QUEUE_SM, self.sents_merit)

    filename1 = self.filename1
    filename2 = self.filename2

    if not (filename1 and filename2):
        logger.info(" filename1: %s, filename2: %s not loaded", filename1, filename2)
        message = f"filename1: *{filename1}*, filename2: *{filename2}* not loaded"
        messagebox.showwarning(title="Not ready", message=message)
        return None

    logger.debug("file1: %s", filename1)
    logger.debug("file2: %s", filename2)

    prefix = common_prefix(
        [
            Path(filename1).stem,
            Path(filename2).stem,
        ]
    )
    csvfile_p = gen_filename(f"{prefix}aligned-p.csv")
    csvfile_s = gen_filename(f"{prefix}aligned-s.csv")
    path_ = Path(filename1).parent
    csvfile_p = f"{path_ / csvfile_p}"
    csvfile_s = f"{path_ / csvfile_s}"

    msg = "\n"
    logger.debug(" self.saligned %s, self.paligned %s", self.saligned, self.paligned)

    logger.debug(" self.paras1: %s, self.paras2: %s", self.paras1, self.paras2)
    if self.paligned:
        df_ = DataFrame({
            "text1": self.paras1,
            "text2": self.paras2,
            "merit": self.paras_merit
        })
        df_.to_csv(csvfile_p, index=False, header=False, encoding="gbk")
        logger.info(" Aligned paras saved to %s", csvfile_p)
        msg += " Aligned paras saved to %s\n" % csvfile_p

    logger.debug(" self.sents1: %s, self.sents2: %s", self.sents1, self.sents2)

    if self.saligned:
        df_ = DataFrame({
            "text1": self.sents1,
            "text2": self.sents2,
            "merit": self.sents_merit
        })
        df_.to_csv(csvfile_s, index=False, header=False, encoding="gbk")
        logger.info(" Aligned sents saved to %s", csvfile_s)
        msg += " Aligned sents saved to %s" % csvfile_s

    msg = msg.strip()
    if msg:
        messagebox.showinfo(title="File(s) saved", message=msg)

    logger.debug("csvfile: %s, %s", csvfile_p, csvfile_s)

    logger.info("savecsv_command")
