"""
insert list/iterable to col (0, 1, 2) th column
"""
# pylint: disable=invalid-name

import os

from itertools import zip_longest
import numpy as np
import pandas as pd

import logzero
from logzero import logger

_ = os.environ.get("ALIGNER_DEBUG")
if _ is not None and (_ == "1" or _.lower() == "true"):
    logzero.loglevel(10)
else:
    logzero.loglevel(20)


def insert_column(values, df=None, col=0):
    """insert values to df's col-th column """

    if not isinstance(values, (list, tuple)):
        logger.error("Values not list nor tuple: %s", type(values))
        return None

    # len_ = len(values)
    if df is None:
        df = pd.DataFrame({"text1": [""], "text2": [""], "merit": [""]})

    try:
        col = int(col)
    except Exception as exc:
        logger.error("col = int(col) Exceptinon: %s, set to 0", exc)
        col = 0

    if col > 2:
        logger.warning("col > 2: %s, set to 0", col)
        col = 0

    columns = ["text1", "text2", "merit"]
    # gen = lambda col0, col1, col2: np.asarray([*zip_longest(df.text1, lst, df.merit, fillvalue='')], dtype=str)

    def gen_df(col0, col1, col2):
        return pd.DataFrame(
            np.asarray([*zip_longest(col0, col1, col2, fillvalue="")], dtype=str),
            columns=columns,
        )

    if col == 0:
        df = gen_df(values, df.text2, df.merit)

    if col == 1:
        df = gen_df(df.text1, values, df.merit)

    if col == 2:
        df = gen_df(df.text1, df.text2, values)

    # remove empty tail where row elements are all ""
    _ = """
    arr = np.asarray(df)
    len_ = len(arr)

    for elm in range(len_):
        if ''.join(arr[len_ - elm - 1]):
            tail = elm
            break
    else:  # all rows empty
        tail = len_

    return df[0: len_ - tail]
    # """

    # remove rows with all empty entries
    # keep = df.applymap(bool).any(axis=1)
    # drop_index = [idx for idx, elm in enumerate(keep) if not elm]
    # return df.drop(drop_index)

    # remove rows with all empty entries
    return df.replace("", np.nan).dropna(how="all").replace(np.nan, "")

def test0():
    """in insert 0"""
    df = pd.DataFrame({"text1": [""], "text2": [""], "merit": [""]})
    values = [*range(3)]

    exp = pd.DataFrame(
        np.asarray([*zip_longest(values, df.text2, df.merit, fillvalue="")]),
        columns=["text1", "text2", "merit"],
    )
    assert np.all(np.asarray(insert_column(values, df, 0)) == np.asarray(exp))


def test1():
    """in insert 0"""
    df = pd.DataFrame({"text1": [""], "text2": [""], "merit": [""]})
    values = [*range(3)]

    exp = pd.DataFrame(
        np.asarray([*zip_longest(df.text1, values, df.merit, fillvalue="")]),
        columns=["text1", "text2", "merit"],
    )
    assert np.all(np.asarray(insert_column(values, df, 1)) == np.asarray(exp))


def test2():
    """in insert 2"""
    df = pd.DataFrame({"text1": [""], "text2": [""], "merit": [""]})
    values = [*range(3)]

    exp = pd.DataFrame(
        np.asarray([*zip_longest(df.text1, df.text2, values, fillvalue="")]),
        columns=["text1", "text2", "merit"],
    )
    assert np.all(np.asarray(insert_column(values, df, 2)) == np.asarray(exp))


def test01():
    """in insert 0,1 """

    df = pd.DataFrame({"text1": [""], "text2": [""], "merit": [""]})
    values = [*range(3)]

    df1 = insert_column(values, df, 0)

    values1 = [*range(4)]

    df2_array = np.array(
        [["0", "0", ""], ["1", "1", ""], ["2", "2", ""], ["", "3", ""]], dtype=object
    )
    df2 = insert_column(values1, df1, 1)

    assert np.all(np.asarray(df2) == df2_array)


def test01a():
    """in insert 0,1 (a) """

    df = pd.DataFrame({"text1": [""], "text2": [""], "merit": [""]})
    values = [*range(3)]

    df1 = insert_column(values, df, 0)

    values1 = [*range(4)]

    df2_array = np.array(
        [["0", "0", ""], ["1", "1", ""], ["2", "2", ""], ["", "3", ""]], dtype=object
    )
    del df2_array

    df2 = insert_column(values1, df1, 1)
    # del df2

    # assert np.all(np.asarray(df2) == df2_array)

    values1 = [*range(2)]
    df2a = insert_column(values1, df2, 1)

    exp0 = np.array(
        [["0", "0", ""], ["1", "1", ""], ["2", "", ""], ["", "", ""]], dtype=object
    )

    # arr = np.asarray(df2a)
    arr = exp0
    len_ = len(arr)

    for elm in range(len_):
        if "".join(arr[len_ - elm - 1]):
            tail = elm
            break
    else:  # all rows empty
        tail = len_

    # remove last rows with ""
    exp = exp0[: len_ - tail]

    df_exp = pd.DataFrame(exp, columns=["text1", "text2", "merit"])

    assert (df_exp == df2a).all(axis=None)
