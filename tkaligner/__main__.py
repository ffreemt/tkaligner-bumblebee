""" tkinter aligner UI part.

based on  aligner_ui.py
"""

import os
import tkinter as tk

import logzero
from logzero import logger

from aligner_ui import Aligner


def tkaligner() -> None:
    """ tkinter aligner UI part
    """

    root = tk.Tk()

    # top = tk.Toplevel(root)
    # Aligner(top)

    Aligner(root)

    logger.debug("tkaligner debug ")

    root.mainloop()


if __name__ == "__main__":

    _ = os.environ.get("ALIGNER_DEBUG")
    logger.info('os.environ.get("ALIGNER_DEBUG"): %s', _)
    if _ is not None and _.lower() in ["1", "true"]:
        logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
    else:
        logzero.loglevel(20)

    tkaligner()
