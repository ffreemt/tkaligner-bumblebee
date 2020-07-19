#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.1
#  in conjunction with Tcl version 8.6
#    Jul 16, 2020 10:19:26 PM CST  platform: Windows NT

import sys

# from threading import Thread
# from textwrap import dedent
from pathlib import Path
# import blinker
# from blinker import signal

from tkinter import filedialog
from tkinter import messagebox

import blinker
import logzero
from logzero import logger

from insert_column import insert_column
from load_paras import load_paras

from myprogressbar_ui import Mypbar
import myprogressbar_ui_support
from longtime_job import longtime_job

from mypad import MyPad  # mypad_ui.tcl/py?
from mytable import MyTable
from queues import QUEUE_SPINBOX
from extract_rows import extract_rows

# to update table when loading files with open1 open2
SIG_TABLE = blinker.signal('table')

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import aligner_ui_support
from queue1_put import queue1_put
from support import on_howto, on_about  # savetmx_command

from open1_command import open1_command
from open2_command import open2_command
from savetmx_command import savetmx_command
from savetsv_command import savetsv_command
from quit_command import quit_command

from palign_command import palign_command
from salign_command import salign_command
from reset_command import reset_command


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()

    w = tk.Toplevel (root)
    top = Aligner (w)

    # top = Aligner (root)
    # aligner_ui_support.init(root, top)

    logger.debug('vp_start_gui debug ')

    root.mainloop()

w = None
def create_Aligner(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Aligner(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Aligner (w)
    aligner_ui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Aligner():
    global w
    w.destroy()
    w = None

class Aligner:
    def __init__(self, top=None):
        super().__init__()
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self.top = top
        iconpath = Path(__file__).parent / "align.ico"
        top.iconbitmap(str(iconpath))
        self.spinbox = ''
        # QUEUE_SPINBOX.put('*')
        queue1_put(QUEUE_SPINBOX, '*')

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {Segoe UI} -size 9"

        # top.geometry("988x447+626+56")
        top.geometry("980x625+25+25")
        top.minsize(120, 1)
        top.maxsize(1284, 781)
        top.resizable(1, 1)
        top.title("Tkaligner")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.FramePad = tk.Frame(top)
        self.FramePad.place(relx=0.0, rely=0.0, relheight=0.5, relwidth=1.0)
        self.FramePad.configure(relief='groove')
        self.FramePad.configure(borderwidth="2")
        self.FramePad.configure(relief="groove")
        self.FramePad.configure(background="#d9d9d9")
        self.FramePad.configure(highlightbackground="#d9d9d9")
        self.FramePad.configure(highlightcolor="black")

        # self.Pad = aligner_ui_support.Custom(self.FramePad)
        self.Pad = MyPad(self.FramePad)
        self.Pad.c01.configure(wrap="word")
        self.Pad.c02.configure(wrap="word")
        self.Pad.c11.configure(wrap="word")
        self.Pad.c12.configure(wrap="word")
        self.Pad.c21.configure(wrap="word")
        self.Pad.c22.configure(wrap="word")

        self.Pad.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

        self.FrameTable = tk.Frame(top)
        self.FrameTable.place(relx=0.0, rely=0.5, relheight=0.5, relwidth=1.0)
        self.FrameTable.configure(relief='groove')
        self.FrameTable.configure(borderwidth="2")
        self.FrameTable.configure(relief="groove")
        self.FrameTable.configure(background="#d9d9d9")
        self.FrameTable.configure(highlightbackground="#d9d9d9")
        self.FrameTable.configure(highlightcolor="black")

        # self.Table = aligner_ui_support.Custom(self.FrameTable)
        self.Table = MyTable(self.FrameTable)
        self.Table.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Table.show()

        self.menubar = tk.Menu(top,font=font9,bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.sub_menu = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkDefaultFont",
                foreground="#000000",
                label="File")
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+O",
                background="#d9d9d9",
                # command=aligner_ui_support.self.open1_command,
                # command=self.open1_command,
                command=lambda: open1_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="Open1",
                underline=0)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+P",
                background="#d9d9d9",
                # command=aligner_ui_support.self.open2_command,
                # command=self.open2_command,
                command=lambda: open2_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="Open2",
                underline=1)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+T",
                background="#d9d9d9",
                # command=aligner_ui_support.self.savetsv_command,
                # command=self.savetsv_command,
                command=lambda: savetsv_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="SaveTsv",
                underline=4)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+M",
                background="#d9d9d9",
                # command=aligner_ui_support.self.savetmx_command,
                # command=self.savetmx_command,
                command=lambda: savetmx_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="SaveTMX",
                underline=5)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl-Q",
                background="#d9d9d9",
                # command=self.quit_command,
                command=lambda: quit_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="Quit",
                underline=0)
        self.sub_menu1 = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu1,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkDefaultFont",
                foreground="#000000",
                label="Edit")
        self.sub_menu1.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+P",
                background="#d9d9d9",
                # command=self.palign_command,
                command=lambda: palign_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="PAlign",
                underline=0)
        self.sub_menu1.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+S",
                background="#d9d9d9",
                # command=self.salign_command,
                command=lambda: salign_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="SAlign",
                underline=0)
        self.sub_menu1.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+R",
                background="#d9d9d9",
                # command=self.reset_command,
                command=lambda: reset_command(self),
                font="TkDefaultFont",
                foreground="#000000",
                label="Reset",
                underline=0)
        self.sub_menu12 = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu12,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkDefaultFont",
                foreground="#000000",
                label="Help")
        self.sub_menu12.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl+H",
                background="#d9d9d9",
                command=on_howto,
                font="TkDefaultFont",
                foreground="#000000",
                label="Howto",
                underline=0)
        self.sub_menu12.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                accelerator="Ctrl-I",
                background="#d9d9d9",
                command=on_about,
                font="TkDefaultFont",
                foreground="#000000",
                label="About",
                underline=0)

        self.sub_menu.bind_all('<Control-Key-h>',lambda e:on_howto(e))
        self.sub_menu.bind_all('<Control-Key-i>',lambda e:on_about(e))

        # self.sub_menu.bind_all('<Control-Key-o>',lambda e: self.open1_command(e))
        self.sub_menu.bind_all('<Control-Key-o>',lambda e: open1_command(self, event=e))
        # self.sub_menu.bind_all('<Control-Key-p>',lambda e: self.open2_command(e))
        self.sub_menu.bind_all('<Control-Key-p>',lambda e: open2_command(self, event=e))
        # self.sub_menu.bind_all('<Control-Key-t>',lambda e: self.savetsv_command(e))
        self.sub_menu.bind_all('<Control-Key-t>',lambda e: savetsv_command(self, event=e))
        # self.sub_menu.bind_all('<Control-Key-m>',lambda e: self.savetmx_command(e))
        self.sub_menu.bind_all('<Control-Key-m>',lambda e: savetmx_command(self, event=e))
        # self.sub_menu.bind_all('<Control-Key-q>',lambda e: self.quit_command(e))
        self.sub_menu.bind_all('<Control-Key-q>',lambda e: quit_command(self, event=e))

        self.sub_menu.bind_all('<Control-Key-p>',lambda e: palign_command(self, event=e))
        self.sub_menu.bind_all('<Control-Key-s>',lambda e: salign_command(self, event=e))
        self.sub_menu.bind_all('<Control-Key-r>',lambda e: reset_command(self, event=e))

    def open1_command(self, event=None):
        from load_paras import load_paras

        logger.debug('<open1_command>')
        # from tkinter import filedialog
        # self.top = self
        # file = tk.filedialog.askopenfile(parent=root, mode='r', title='Select a file')

        # file = filedialog.askopenfile(parent=self.top, mode='r', title='Select a file')
        file = filedialog.askopenfilename(title='Select a file', filetypes = (
            ("text files", "*.txt"),
            ("pdf files", "*.pdf"),
            ("docx files", "*.docx"),
            ("all files", "*.*"),
        ))

        if file != None:
            # self.text.delete('1.0', END)

            # self.text1 = file.read()
            try:
                self.text1, _ = load_paras(file)
            except:
                self.text1 = load_paras(file)

            # root.wm_title(file.name + " : Zen Text Editor")
            # self.text.insert('1.0', contents)
            logger.debug('self.text1[:3]: %s', self.text1[:3])

            # file.close()

        # values = self.text1.split('\n')
        values = self.text1

        df = self.Table.model.df
        df.columns = ['text1', 'text2', 'merit']
        df = insert_column(values, df, 0)
        self.Table.model.df = df

        # logger.debug(self.Table.model.df)
        # data = extract_rows(self.Table.model.df, 0)
        data = extract_rows(self.Table.model.df, self.Table.row_clicked)

        logger.debug("data sent to SIG_TABLE.send(data=data): %s", data)

        SIG_TABLE.send(data=data)

        self.Table.show()
        self.Table.redraw()

    def open2_command(self, event=None):
        # from load_paras import load_paras

        logger.debug('<open2_command>')

        # from tkinter import filedialog
        # self.top = self
        # file = tk.filedialog.askopenfile(parent=root, mode='r', title='Select a file')

        # file = filedialog.askopenfile(parent=self.top, mode='r', title='Select a file')
        file = filedialog.askopenfilename(title='Select a file', filetypes = (
            ("text files", "*.txt"),
            # ("pdf files", "*.pdf"),
            # ("docx files", "*.docx"),
            ("all files", "*.*"),
        ))

        if file != None:
            # self.text.delete('1.0', END)
            # self.text2 = file.read()

            try:
                self.text2, _ = load_paras(file)
            except:
                self.text2 = load_paras(file)

            # root.wm_title(file.name + " : Zen Text Editor")
            # self.text.insert('1.0', contents)

            logger.debug('self.text2[:3]: %s', self.text2[:3])

            # file.close()

        # values = self.text2.split('\n')
        values = self.text2

        df = self.Table.model.df
        df.columns = ['text1', 'text2', 'merit']
        df = insert_column(values, df, 1)
        self.Table.model.df = df

        # logger.debug(self.Table.model.df)
        logger.debug("self.Table.model.df[:3]: %s", self.Table.model.df[:3])
        # send self.Table.model.df[:3] to PAD
        # SIG_TABLE.send(data=self.Table.model.df[:3])

        # data = extract_rows(self.model.df, self.row_clicked)
        # pretend row 0 clicked
        # data = extract_rows(self.Table.model.df, 0)

        data = extract_rows(self.Table.model.df, self.Table.row_clicked)
        logger.debug("data sent to SIG_TABLE.send(data=data): %s", data)

        SIG_TABLE.send(data=data)

        self.Table.show()
        self.Table.redraw()

    def palign_command(self, event=None):

        logger.debug('palign_command')

        top = self.top
        # top = None

        window = tk.Toplevel(top)
        # window = tk.Toplevel(self) does not work

        # refer to open_settings_window.py

        myprogressbar_ui_support.set_Tk_var()

        # QUEUE_SPINBOX.put('*')
        pbar = Mypbar(window)
        # pbar = Mypbar(self)

        # disbale cancel butt until start is clicked
        # TButton1: Start, 2: Cancel,3: Back
        pbar.TButton2.config(state=tk.DISABLED)

        window.focus_force()
        window.grab_set()
        return None

    def quit_command(self, event=None):
        logger.debug('quit_command')
        if event:
            logger.debug(event)
        # if tkMessageBox.askokcancel(
        if messagebox.askokcancel(
            "Quit ","Do you really want to quit?"
        ):
            self.top.destroy()  # self.top is root = tk.Tk()

            # logger.debug(" after self.top.destroy_window()")
            # import sys
            # sys.exit()

            # self.top = None
            # refer to aligner_ui_support.destroy_window
            # refer to vp_start_gui in aligner_ui.py

            # aligner_ui_support.destroy_window()

    def reset_command(self, event=None):
            logger.info('reset_command')
            # sys.stdout.flush()

    def salign_command(self, event=None):

        logger.debug('salign_command')

        top = self.top
        # top = None

        window = tk.Toplevel(top)
        # window = tk.Toplevel(self) does not work

        # refer to open_settings_window.py

        myprogressbar_ui_support.set_Tk_var()

        # QUEUE_SPINBOX.put('*')
        pbar = Mypbar(window)
        # pbar = Mypbar(self)

        # disbale cancel butt until start is clicked
        # TButton1: Start, 2: Cancel,3: Back
        pbar.TButton2.config(state=tk.DISABLED)

        window.focus_force()
        window.grab_set()
        return None

    def savetmx_command(self, event=None):
        logger.info('savetmx_command')
        sys.stdout.flush()

    def savetsv_command(self, event=None):
        logger.info('savetsv_command')
        # sys.stdout.flush()


if __name__ == '__main__':
    import os
    _ = os.environ.get("ALIGNER_DEBUG")
    logger.info('os.environ.get("ALIGNER_DEBUG"): %s', _)
    if _ is not None and (_ == '1' or _.lower() == 'true'):
        logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
    else:
        logzero.loglevel(20)
    vp_start_gui()




