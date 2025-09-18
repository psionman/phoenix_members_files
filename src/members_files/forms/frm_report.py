"""ReportFrame for Phoenix Members Files."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from psiutils.constants import PAD
from psiutils.buttons import ButtonFrame, IconButton
from psiutils.utilities import window_resize
from psiutils.treeview import sort_treeview
from psiutils.widgets import separator_frame
from psiutils import text

from members_files.constants import APP_TITLE, DEFAULT_GEOMETRY
from members_files.config import read_config
from members_files.process import Compare

FRAME_TITLE = f'{APP_TITLE} - Reports'

TREE_COLUMNS = (
    ('ebu', 'EBU', 50),
    ('name', 'Name', 100),
    ('username', 'username', 50),
)


class ReportFrame():
    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.config = read_config()
        self.comparison = Compare(self.parent)
        self.include_tree = None
        self.names_tree = None
        self.copy_include_button = None
        self.copy_bbo_button = None

        duplicates = ''
        if self.comparison.duplicates:
            bbo_file = self.parent.bbo_names_file.get()
            duplicates = f'Duplicates found in {bbo_file}'

        # tk variables
        self.duplicates = tk.StringVar(value=duplicates)

        self.show()

    def show(self) -> None:
        # pylint: disable=no-member)
        root = self.root
        try:
            root.geometry(self.config.geometry[Path(__file__).stem])
        except KeyError:
            root.geometry(DEFAULT_GEOMETRY)
        root.transient(self.parent.root)
        root.title(FRAME_TITLE)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.bind('<Control-x>', self._dismiss)

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
        frame.columnconfigure(0, weight=1)

        row = 0
        label = ttk.Label(
            frame, textvariable=self.duplicates, style='red-fg.TLabel')
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        row += 1
        label = ttk.Label(frame, text='Missing from include')
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        row += 1
        self.include_tree = self._get_include_tree(frame)
        self.include_tree.grid(row=row, column=0, sticky=tk.NSEW)

        self.copy_include_button = IconButton(
            frame, text.COPY, 'copy_docs', self._copy_include, True)
        self.copy_include_button.grid(
            row=row, column=1, padx=PAD, pady=PAD, sticky=tk.N)

        self.copy_include_button.disable()
        self._populate_include_tree()

        row += 1
        separator = separator_frame(frame, '')
        separator.grid(row=row, column=0, columnspan=2,
                       sticky=tk.EW, padx=PAD)

        row += 1
        label = ttk.Label(frame, text='Missing from bbo_names')
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        row += 1
        self.names_tree = self._get_names_tree(frame)
        self.names_tree.grid(row=row, column=0, sticky=tk.NSEW)

        self.copy_bbo_button = IconButton(
            frame, text.COPY, 'copy_docs', self._copy_names, True)
        self.copy_bbo_button.grid(
            row=row, column=1, padx=PAD, pady=PAD, sticky=tk.N)
        self.copy_bbo_button.disable()
        self._populate_names_tree()
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('exit', self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _get_include_tree(self, master: tk.Frame) -> ttk.Treeview:
        """Return  a tree widget."""
        tree = ttk.Treeview(
            master,
            selectmode='browse',
            height=15,
            show='headings',
            )

        col_list = tuple(col[0] for col in TREE_COLUMNS)

        tree['columns'] = col_list
        for col in TREE_COLUMNS:
            (col_key, col_text, col_width) = (col[0], col[1], col[2])
            tree.heading(col_key, text=col_text,
                         command=lambda c=col_key:
                         sort_treeview(tree, c, False))
            tree.column(col_key, width=col_width, anchor=tk.W)
        return tree

    def _populate_include_tree(self) -> None:
        self.include_tree.delete(*self.include_tree.get_children())
        if len(self.comparison.missing_from_include) > 0:
            self.copy_include_button.enable()
        for item in self.comparison.missing_from_include.values():
            values = (
                item.ebu,
                f'{item.first_name} {item.last_name}',
                item.bbo)
            self.include_tree.insert('', 'end', values=values)

    def _copy_include(self, *args):
        dlg = messagebox.askyesno(
            '',
            'Overwrite include file?'
        )
        if not dlg:
            return

        include = []
        for member in self.comparison.members_bbo.values():
            status = ''
            if member.ebu in self.comparison.members_ebu:
                status = self.comparison.members_ebu[member.ebu].status
            if member.bbo and status == 'Member':
                include.append(member.bbo)

        path = self.parent.bbo_include_file.get()
        with open(path, 'w', encoding='utf8') as f_include:
            f_include.write('\n'.join(sorted(include)))
        self.comparison = Compare(self.parent)
        self._populate_include_tree()

    def _get_names_tree(self, master: tk.Frame) -> ttk.Treeview:
        """Return  a tree widget."""
        tree = ttk.Treeview(
            master,
            selectmode='browse',
            height=15,
            show='headings',
            )

        col_list = tuple(col[0] for col in TREE_COLUMNS)

        tree['columns'] = col_list
        for col in TREE_COLUMNS:
            (col_key, col_text, col_width) = (col[0], col[1], col[2])
            tree.heading(col_key, text=col_text,
                         command=lambda c=col_key:
                         sort_treeview(tree, c, False))
            tree.column(col_key, width=col_width, anchor=tk.W)
        return tree

    def _populate_names_tree(self) -> None:
        self.names_tree.delete(*self.names_tree.get_children())
        if len(self.comparison.missing_from_bbo) > 0:
            self.copy_bbo_button.enable()
        for item in self.comparison.missing_from_bbo.values():
            values = (
                item.ebu,
                f'{item.first_name} {item.last_name}',
                item.bbo)
            self.names_tree.insert('', 'end', values=values)

    def _copy_names(self, *args):
        dlg = messagebox.askyesno(
            '',
            'Overwrite bbo_names file?'
        )
        if not dlg:
            return

        combined = {
            **self.comparison.missing_from_bbo,
            **self.comparison.members_bbo
            }
        names = [(f'{member.bbo},'
                  f'{member.first_name},'
                  f'{member.last_name},'
                  f'{member.ebu}')
                 for member in combined.values()]

        path = self.parent.bbo_names_file.get()
        with open(path, 'w', encoding='utf8') as f_include:
            f_include.write('\n'.join(sorted(names)))
        self.comparison = Compare(self.parent)
        self._populate_names_tree()

    def _process(self, *args) -> None:
        ...

    def _dismiss(self, *args) -> None:
        self.parent.root.destroy()
