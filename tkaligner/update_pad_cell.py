r'''
update pad cell
refer to  myapps\tkinter_stuff\playground\blinker_try_pad.py
'''
import tkinter as tk
import tkinter.ttk as ttk

from logzero import logger


def update_pad_cell(pad, row=0, col=0, cont=''):
    """ update pad cell. """
    def update_label(row, col, cont):
        cell = f'c{row}{col}'
        getattr(pad, cell)['text'] = cont
    def update_text(row, col, cont):
        cell = f'c{row}{col}'
        getattr(pad, cell).delete('0.0', 'end')
        getattr(pad, cell).insert('0.0', cont)

    try:
        cell = getattr(pad, f'c{row}{col}')
    except Exception as exc:
        logger.error('cell = getattr exc: %s', exc)
        return

    if isinstance(cell, (tk.Label, tk.ttk.Label)):
        # label: cell.config['text'] = or cell['text'] =
        update_label(row, col, cont)
    elif isinstance(cell, tk.Text):
        update_text(row, col, cont)
    else:
        #
        assert 0, 'Something wrong'
