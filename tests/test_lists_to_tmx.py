""" test lists_to_tmx. """

from pathlib import Path
import re
import pandas as pd


from logzero import logger

from tkaligner.lists_to_tmx import lists_to_tmx


def test_lists_to_tmx():
    """ test lists_to_tmx. """
    curr_dir = Path(__file__).parent
    filepath = curr_dir / "0test_aligned-s.csv"
    try:
        df = pd.read_csv(filepath, header=None, na_filter="", encoding="gbk")
    except Exception as exc:
        logger.error("exc: %s", exc)
        raise SystemError(1)

    tmx = lists_to_tmx(df[0], df[1])
    numb0 = re.findall("tuv lang=.zh-CN", tmx).__len__()
    numb1 = re.findall("tuv lang=.en-US", tmx).__len__()
    assert numb0 == numb1
