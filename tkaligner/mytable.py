r'''

myapps\tkinter_stuff\official-example-pandastable.py

import page_gui_menu_support
from Mytable import mytable
# implement pandastable

# ----
        self.PD = Mytable(top)
        self.PD.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

if __name__ == '__main__':
    vp_start_gui()

'''
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-order, inconsistent-return-statements,
# pylint: disable=no-self-use

import os
# import logging

# from blinker import signal
import blinker

from tkinter import *  # noqa: F403, F401
from tkinter.ttk import *  # noqa: F403, F401

import pandas as pd
import numpy as np
from pandastable.core import Table
# from pandastable.data import TableModel

import logzero
from logzero import logger

from extract_rows import extract_rows

SIG_TABLE = blinker.signal('table')
SIG_PAD = blinker.signal('pad')

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())

from logzero import setup_logger
logger = setup_logger(
    name=__file__,
    level=20,
)
logger.info("hello")


class MyTable(Table):  # pylint: disable=too-many-ancestors
    """
      Custom table class inherits from Table.
      You can then override required methods
     """

    def __init__(self, parent=None, **kwargs):
        # Table.__init__(self, parent, **kwargs)
        super().__init__(parent, **kwargs)

        def handle_signal(sender, **kw):
            self.slot_table(sender, **kw)
        self.handle_signal = handle_signal  # important, not for nothing
        SIG_TABLE.connect(handle_signal)
        # in effect SIG_TABLE.connect(self.slot_table)

        self.row_clicked = None
        self.column_clicked = None

        # setup for initial open1 open2 pad
        # in open1/open2: do extract_rows and SIG_TABLE.send (imitate handle_left_click)
        self.row_clicked = 0
        self.column_clicked = 0

        self.showstatusbar = True

        # print(*args, **kwargs)
        # print('** rows cols **: ', self.rows, self.cols)

        # '''
        # pandastable default rows == 30, cols == 5?
        if self.rows == 20 and self.cols == 5:
            _ = ' ' * 40
            _ = ' ' * 60
            _ = ' ' * 1
            dataframe = pd.DataFrame({
                # 'a': range(3),
                # 'a': ['0', '1', 2],
                'text1': ['0' + _, '1', '2'],
                # 'b': range(3, 3 + 3),
                # 'b': ['3', '4', 5],
                'text2': ['3' + _, '4', '5'],
                # 'c': range(6, 6 + 3),
                # 'c': ['6', '7', 8],
                # 'merit': [0.6, 0.7, 0.8],
                'merit': ["", "", ""],
            })
            Table.__init__(self, parent, dataframe=dataframe, showstatusbar=True)

            # activate pad: imitate left click row-0 of table
            data = extract_rows(self.model.df, self.row_clicked)
            # SIG_TABLE.send('table', data=data)
            # SIG_TABLE.send(data=data)
            SIG_PAD.send(data=data)

            # self.dataframe = dataframe
            # self.show()
        # '''

        # Canvas .geometry("988x447+626+56")
        # mytable.columnwidths: {'text1': 300, 'text2': 300, 'merit': 80}
        self.columnwidths = {'text1': 430, 'text2': 430, 'merit': 80}

        self.show()

        if parent is not None:
            logger.debug("parent.winfo_width(): %s", parent.winfo_width())
            logger.debug("parent.winfo_geometry(): %s", parent.winfo_geometry())
            logger.debug("mytable.columnwidths: %s", self.columnwidths)

    def handle_left_click(self, event):
        r''' handle left click

        left-click to select
        myapps\tkinter_stuff\row_clicked_selected-pandastable.py
        pandastable source code: handle_right_click sans popmenu
        '''

        super().handle_left_click(event)

        rowclicked = self.get_row_clicked(event)

        self.row_clicked = rowclicked

        # logger.info("event: %s, type: %s", event, type(event))

        logger.debug("RowClicked: %s", rowclicked)
        rowsel = self.getSelectedRow()
        logger.debug("RowSelected: %s", rowsel)

        # left click to select
        # table.currentrow = rowclicked
        # table.setSelectedRow(rowclicked)

        # from source code handle_right_click(self, event)
        # (popmenu removed), substitute self with table

        self.delete('tooltip')
        self.rowheader.clearSelected()
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        rowclicked = self.get_row_clicked(event)
        colclicked = self.get_col_clicked(event)

        if rowclicked is None or colclicked is None:
            return None

        # color the third col
        # self.Table.setRowColors(rows=rows1, clr="#FF0000", cols=[2])
        # self.Table.update_rowcolors()
        # for elm in range(self.rows):  # slow response for long table
            # self.setRowColors(rows=elm, clr="#FF0000", cols=[2])

        # logger.info("clicked, self.rows: %s", self.rows)
        # df = self.model.df
        # idx = df.index[rows]

        # df = self.model.df
        # logger.info(" df.index: %s, df.to_dict(): %s", df.index, df.to_dict())

        # self.setRowColors(rows=list(range(self.rows)), clr="#FF0000", cols=[2])
        # self.update_rowcolors()
        # self.redraw()

        # self.setColorbyValue()  # popup

        if 0 <= rowclicked < self.rows and 0 <= colclicked < self.cols:
            self.clearSelected()
            self.allrows = False
            self.setSelectedRow(rowclicked)
            self.setSelectedCol(colclicked)
            self.drawSelectedRect(self.currentrow, self.currentcol)
            self.drawSelectedRow()

            # self.model.df.iloc[self.currentrow, self.currentcol] = 0  # clear
            # self.redraw()  # !OKOK

            # ---
            # print(self.model.df)
            # print("currentrow: ", self.currentrow)
            # print("currentcol: ", self.currentcol)

            # populate to MyPad
            # blinker?

            data = extract_rows(self.model.df, self.row_clicked)
            # SIG_TABLE.send('table', data=data)
            # SIG_TABLE.send(data=data)
            SIG_PAD.send(data=data)

            # self.setRowColors(rows=list(range(self.rows)), clr="#FF0000", cols=[2])
            # self.setRowColors(rows=[-2, -1], clr="#FF0000", cols=[2])  # does not work
    # """

    def slot_table(self, sender, **kw):
        ''' handle data for SIG_TABLE (from mypad and other sources) '''
        # logger.debug('**************Enter slot_table, received - sender: %s, kw: \n%s', sender, kw)

        # handle df from longtime_job: SIG_PAD.send('job', df=df_data)

        # logger.info(" kw: %s", kw)

        df = kw.get("df")
        if df is not None:
            columns = ["text1", "text2", "merit"]
            df = pd.DataFrame(df, columns=columns)
            if not df.shape[1] == 3:
                logger.warning(" df not three columns, something is probably wrong.")

            # logger.info("update table: %s", df)

            self.model.df = df.copy()

            # update pad
            data = extract_rows(self.model.df, self.row_clicked)
            SIG_PAD.send(data=data)
            logger.debug("data sent to SIG_PAD.send(data=data): %s", data)

            self.columnwidths = {'text1': 430, 'text2': 430, 'merit': 80}
            self.redraw()

            return

        # mypad.py sends
        # SIG_PAD.send('pad', data=self.data)

        data = kw.get('data')
        logger.debug("np.asarray(data): \n%s", np.asarray(data))
        logger.debug("data.columns \n%s", data.columns)

        ref_row = self.row_clicked
        logger.debug("++++++++++ ref_row: **%s**", ref_row)

        _ = '''
        if ref_row is None:  # table not clicked yet: 1st run
            try:
                ref_row = int(data.iloc[1, 0])  # mid-row, 1st
                logger.debug("ref_row (from pad): **%s**", ref_row)
            except Exception as exc:
                logger.error(" ref_row = int(data[1, 0]) exc: %s", exc)
                raise SystemExit(1)

        # clicked pad when nothing is there (before clicking table
        # data.iloc(range(1, 4)) columns 1,2,3
        _ = """
        try:  #
            if (data[range(1, 4)] == "").all(axis=None):
                logger.debug(" Nothing started...")
                return None
        except:
            ...
        # """
        # '''

        # data.columns [0, 1, 2, 3] changed to ["i", "text1", "text2", "merit"]
        if [*data.columns] == [0, 1, 2, 3]:
            data = data.rename(columns=dict(zip([0, 1, 2, 3], ["i", "text1", "text2", "merit"])))
        # all empty in columns ["text1", "text2", "merit"]
        # and table not clicked ever
        # if ref_row is None and (data[["text1", "text2", "merit"]] == "").all(axis=None):
        if (data[["text1", "text2", "merit"]] == "").all(axis=None):
            logger.debug(" Nothing started...")
            return None

        # no longer needed, but we leave it
        if ref_row is None or kw.get('data') is None:
            return None

        table_df = self.model.df.copy()

        logger.debug("table_df = self.model.df (head(3)): \n%s", table_df.head(3))
        logger.debug("table_df = self.model.df (tail(3)): \n%s, \ntable_df.shape: %s", table_df.tail(3), table_df.shape)

        # logger.debug(" table_df.to_dict()): \n%s", table_df.to_dict())
        logger.debug(" ref_row: %s", ref_row)
        logger.debug(" self.model.df.shape: %s", self.model.df.shape)

        if ref_row < 0:
            ref_row = 0
        if ref_row > self.model.df.shape[0] - 1:
            ref_row = self.model.df.shape[0] - 1

        if ref_row == 0:  # prepnd df_
            logger.debug(" 000 prepnd df_")
            df_ = data.iloc[1:, 1:]
            # table_df = pd.concat([df_, table_df[ref_row - 1:]], ignore_index=1)
            table_df = pd.concat([df_, table_df[2:]], ignore_index=1)
        # elif ref_row == self.model.df.shape[1] - 1:  # append df_
        elif ref_row == self.model.df.shape[0] - 1:  # append df_
            logger.debug(" 111 append df_")
            df_ = data.iloc[:2, 1:]
            # table_df = pd.concat([table_df[:ref_row - 1], df_], ignore_index=1)
            table_df = pd.concat([table_df[:ref_row - 1], df_], ignore_index=1)
        else:
            logger.debug(" 222 middle df_")
            df_ = data.iloc[:, 1:]
            table_df = pd.concat([
                table_df[:ref_row - 1],
                df_,
                table_df[ref_row + 2:]
            ], ignore_index=1)

        logger.debug('data: \n%s, \n%s', data, data.to_dict())
        logger.debug('df_: \n%s, %s', df_, df_.to_dict())
        # logger.debug('table_df: \n%s', table_df)

        logger.debug(">>>table_df = self.model.df (head(3)): \n%s", table_df.head(3))
        logger.debug(">>>table_df = self.model.df (tail(3)): \n%s, \ntable_df.shape: %s", table_df.tail(3), table_df.shape)

        #  table_df.shape: (3, 3), (6, 3) etc
        # logger.info(">>>table_df = self.model.df (tail(3)): \n%s, \ntable_df.shape: %s", table_df.tail(3), table_df.shape)  3x2

        # logger.debug(">>> table_df.to_dict()): \n%s", table_df.to_dict())

        self.model.df = table_df.copy()

        # update pad
        data = extract_rows(self.model.df, self.row_clicked)
        SIG_PAD.send(data=data)
        logger.debug("data sent to SIG_PAD.send(data=data): %s", data)

        self.redraw()
