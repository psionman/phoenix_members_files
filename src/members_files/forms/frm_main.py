
"""MainFrame for Phoenix Members Files."""
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

from psiutils.constants import (PAD, Pad, CSV_FILE_TYPES, DOWNLOADS_DIR,
    TXT_FILE_TYPES)
from psiutils.buttons import ButtonFrame, Button, IconButton
from psiutils.utilities import window_resize

from constants import APP_TITLE
from config import read_config
import text
from data_files import DataFile

from main_menu import MainMenu
from forms.frm_report import ReportFrame

FRAME_TITLE = APP_TITLE


class MainFrame():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.config = read_config()
        self.data_file = DataFile()
        self.data_file.read()

        member_file = ''
        bbo_include_file = ''
        bbo_names_file = ''
        bbo_att_file =''
        if 'member_file' in self.data_file.content:
            member_file = self.data_file.content['member_file']
        if 'bbo_include_file' in self.data_file.content:
            bbo_include_file = self.data_file.content['bbo_include_file']
        if 'bbo_names_file' in self.data_file.content:
            bbo_names_file = self.data_file.content['bbo_names_file']
        if 'bbo_att_file' in self.data_file.content:
            bbo_att_file = self.data_file.content['bbo_att_file']

        # tk variables
        self.member_file = tk.StringVar(value=member_file)
        self.bbo_include_file = tk.StringVar(value=bbo_include_file)
        self.bbo_names_file = tk.StringVar(value=bbo_names_file)
        self.bbo_att_file = tk.StringVar(value=bbo_att_file)

        self.show()

    def show(self):
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.title(FRAME_TITLE)

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-o>', self._process)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        main_menu = MainMenu(self)
        main_menu.create()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=8, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0
        label = ttk.Label(frame, text='Membership file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.member_file)
        entry.grid(row=row, column=1, sticky=tk.EW)

        button = IconButton(frame, text.OPEN, 'open', self._get_member_file)
        button.grid(row=row, column=2, padx=PAD, pady=Pad.S)

        row += 1
        label = ttk.Label(frame, text='BBO include file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.bbo_include_file)
        entry.grid(row=row, column=1, sticky=tk.EW)

        button = IconButton(
            frame, text.OPEN, 'open', self._get_bbo_include_file)
        button.grid(row=row, column=2, padx=PAD, pady=Pad.S)

        row += 1
        label = ttk.Label(frame, text='BBO names file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.bbo_names_file)
        entry.grid(row=row, column=1, sticky=tk.EW)

        button = IconButton(
            frame, text.OPEN, 'open', self._get_bbo_names_file)
        button.grid(row=row, column=2, padx=PAD, pady=Pad.S)

        row += 1
        label = ttk.Label(frame, text='BBO attendance file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.bbo_att_file)
        entry.grid(row=row, column=1, sticky=tk.EW)

        button = IconButton(
            frame, text.OPEN, 'open', self._get_bbo_att_file)
        button.grid(row=row, column=2, padx=PAD, pady=Pad.S)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('report', False, self._process),
            frame.icon_button('close', False, self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _get_member_file(self, *args) -> None:
        initialfile = self.member_file.get()
        initialdir = DOWNLOADS_DIR
        if initialfile:
            initialdir = Path(initialfile).parent
        member_file = filedialog.askopenfilename(
            initialdir=initialdir,
            initialfile=initialfile,
            filetypes=CSV_FILE_TYPES,
        )
        if member_file:
            self.member_file.set(member_file)
            self.data_file.content['member_file'] = member_file
            self.data_file.write()

    def _get_bbo_include_file(self, *args) -> None:
        initialfile = self.bbo_include_file.get()
        initialdir = DOWNLOADS_DIR
        if initialfile:
            initialdir = Path(initialfile).parent
        bbo_include_file = filedialog.askopenfilename(
            initialdir=initialdir,
            initialfile=initialfile,
            filetypes=TXT_FILE_TYPES,
        )
        if bbo_include_file:
            self.bbo_include_file.set(bbo_include_file)
            self.data_file.content['bbo_include_file'] = bbo_include_file
            self.data_file.write()

    def _get_bbo_names_file(self, *args) -> None:
        initialfile = self.bbo_names_file.get()
        initialdir = DOWNLOADS_DIR
        if initialfile:
            initialdir = Path(initialfile).parent
        bbo_names_file = filedialog.askopenfilename(
            initialdir=initialdir,
            initialfile=initialfile,
            filetypes=TXT_FILE_TYPES,
        )
        if bbo_names_file:
            self.bbo_names_file.set(bbo_names_file)
            self.data_file.content['bbo_names_file'] = bbo_names_file
            self.data_file.write()

    def _get_bbo_att_file(self, *args) -> None:
        initialfile = self.bbo_att_file.get()
        initialdir = DOWNLOADS_DIR
        if initialfile:
            initialdir = Path(initialfile).parent
        bbo_att_file = filedialog.askopenfilename(
            initialdir=initialdir,
            initialfile=initialfile,
            filetypes=CSV_FILE_TYPES,
        )
        if bbo_att_file:
            self.bbo_att_file.set(bbo_att_file)
            self.data_file.content['bbo_att_file'] = bbo_att_file
            self.data_file.write()

    def _process(self, *args) -> None:
        dlg = ReportFrame(self)
        self.root.wait_window(dlg.root)

    def _dismiss(self, *args) -> None:
        self.root.destroy()
