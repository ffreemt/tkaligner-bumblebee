"""
load_paras
"""

import os
from typing import List

from pathlib import Path
import chardet
import logzero
from logzero import logger

_ = os.environ.get("ALIGNER_DEBUG")
if _ is not None and (_ == "1" or _.lower() == "true"):
    logzero.loglevel(10)
else:
    logzero.loglevel(20)


def load_paras(filepath: str) -> List[str]:
    """
    load paras
    """

    try:
        text = Path(filepath).read_text("utf-8")
    except UnicodeDecodeError:
        try:
            text = Path(filepath).read_text("gbk")
        except UnicodeDecodeError:  # pylint: disable=try-except-raise
            encoding = chardet.detect(Path(filepath).read_bytes()[:5000]).get(
                "encoding"
            )
            text = Path(filepath).read_text(encoding)
            # rid of some strange chars
            text = text.replace("\u3000", "")
    except Exception as exc:
        logger.error("Path.readtext() exc: %s, return **[]** ", exc)
        # raise SystemExit(1)
        return []

    return [elm.strip() for elm in text.split("\n") if elm.strip()]
