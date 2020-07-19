'''
extract 3 rows
    row_clicked - 1
    row_clicked
    row_clicked + 1

df = myt.model.df
row_clicked = myt.row_clicked
df0 = extract_rows(df, row_clicked)
# df0 = extract_rows(df, 6)

index
columns
df0.insert(0, 'i', df0.index + 1)
self.data = df0.copy()
self.data.index = self.data_o.index

redraw(self)

'''
import pandas as pd
import numpy as np


def extract_rows(
    df: pd.core.frame.DataFrame,
    ref_row: int = 0,
) -> pd.core.frame.DataFrame:
    '''
    extract three rows including ref_row:
    ref_row - 1, ref_row + 2

    if ref_row = 0, preappend [''] * df.shape[1]

    if ref_row = df.shape[0] - 1, append [''] * df.shape[1]
    '''

    row_numb, col_numb = df.shape

    if ref_row < 0:
        ref_row = 0
    if ref_row > row_numb - 1:
        ref_row = row_numb - 1

    low = max(0, ref_row - 1)
    high = min(row_numb, ref_row + 2)

    pad = df[low: high].copy()
    if ref_row <= 0:
        pad0 = pd.DataFrame([[''] * col_numb], columns=pad.columns, index=[''])
        pad = pad0.append(
            pad,
            # ignore_index=1,
        )
    if ref_row >= row_numb - 1:
        pad0 = pd.DataFrame([[''] * col_numb], columns=pad.columns, index=[''])
        pad = pad.append(
            pad0,
            # ignore_index=1,
        )

    return pad


def test_0():
    ''' test 0'''
    df = pd.DataFrame(np.arange(12).reshape(6, 2))

    df0 = extract_rows(df)

    # assert np.all(df0.eq(pd.DataFrame([['', ''], [0, 1], [2, 3]])))

    exp = np.asarray([['', ''], [0, 1], [2, 3]], dtype=object)
    assert np.all(df0 == exp)


def test_1():
    ''' test 0'''
    df = pd.DataFrame(np.arange(12).reshape(6, 2))

    df0 = extract_rows(df, 1)
    assert np.all(df0.eq(pd.DataFrame([[0, 1], [2, 3], [4, 5]])))


def test_5():
    ''' test 5'''
    df = pd.DataFrame(np.arange(12).reshape(6, 2))

    df0 = extract_rows(df, 5)
    # assert np.all(df0.eq(pd.DataFrame([[8, 9], [10, 11], ['', '']])))
    assert np.all(df0.eq(np.asarray([[8, 9], [10, 11], ['', '']], dtype="object")))


def test_6():
    ''' test 6'''
    df = pd.DataFrame(np.arange(12).reshape(6, 2))

    df0 = extract_rows(df, 6)
    # assert np.all(df0.eq(pd.DataFrame([[8, 9], [10, 11], ['', '']])))
    assert np.all(df0.eq(np.asarray([[8, 9], [10, 11], ['', '']], dtype="object")))
