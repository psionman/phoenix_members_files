"""ReportFrame for Phoenix Members Files."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from psiutils.constants import PAD
from psiutils.buttons import ButtonFrame, Button, IconButton
from psiutils.utilities import window_resize
from psiutils.treeview import sort_treeview
from psiutils.widgets import separator_frame
from psiutils import text

from constants import APP_TITLE, DEFAULT_GEOMETRY
from config import read_config
from process import Compare
# import text

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
        self.allowed_tree = None
        self.names_tree = None
        duplicates = ''
        if self.comparison.duplicates:
            bbo_file = self.parent.bbo_names_file.get()
            duplicates = f'Duplicates found in {bbo_file}'

        # tk variables
        self.duplicates = tk.StringVar(value=duplicates)

        self.show()

    def show(self) -> None:
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
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        row = 0
        label = ttk.Label(
            frame, textvariable=self.duplicates, style='red-fg.TLabel')
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        row += 1
        label = ttk.Label(frame, text='Missing from allowed')
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        row += 1
        self.allowed_tree = self._get_allowed_tree(frame)
        self.allowed_tree.grid(row=row, column=0, sticky=tk.NSEW)
        self._populate_allowed_tree()

        button = IconButton(frame, text.COPY, 'copy_docs', self._copy_allowed)
        button.grid(row=row, column=1, padx=PAD, pady=PAD, sticky=tk.N)

        row += 1
        separator = separator_frame(frame, '')
        separator.grid(row=row, column=0, columnspan=2,
                       sticky=tk.EW, padx=PAD)

        row += 1
        label = ttk.Label(frame, text='Missing from names')
        label.grid(row=row, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        row += 1
        self.names_tree = self._get_names_tree(frame)
        self.names_tree.grid(row=row, column=0, sticky=tk.NSEW)
        self._populate_names_tree()

        button = IconButton(frame, text.COPY, 'copy_docs', self._copy_names)
        button.grid(row=row, column=1, padx=PAD, pady=PAD, sticky=tk.N)
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            # frame.icon_button('build', True, self._process),
            frame.icon_button('exit', False, self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _get_allowed_tree(self, master: tk.Frame) -> ttk.Treeview:
        """Return  a tree widget."""
        tree = ttk.Treeview(
            master,
            selectmode='browse',
            height=15,
            show='headings',
            )
        # tree.bind('<<TreeviewSelect>>', self._tree_clicked)
        # tree.bind('<Button-3>', self._show_context_menu)

        col_list = tuple(col[0] for col in TREE_COLUMNS)

        tree['columns'] = col_list
        for col in TREE_COLUMNS:
            (col_key, col_text, col_width) = (col[0], col[1], col[2])
            tree.heading(col_key, text=col_text,
                         command=lambda c=col_key:
                         sort_treeview(tree, c, False))
            tree.column(col_key, width=col_width, anchor=tk.W)
        # tree.column(<'right-align-column-name'>, stretch=0, anchor=tk.E)
        return tree

    def _populate_allowed_tree(self) -> None:
        self.allowed_tree.delete(*self.allowed_tree.get_children())
        for item in self.comparison.missing_from_allowed.values():
            values = (
                item.ebu,
                f'{item.first_name} {item.last_name}',
                item.bbo)
            self.allowed_tree.insert('', 'end', values=values)

    def _copy_allowed(self, *args):
        dlg = messagebox.askyesno(
            '',
            'Overwrite Allowed file?'
        )
        if not dlg:
            return

        allowed = [member.bbo
                   for member in self.comparison.members.values()
                   if member.bbo and member.status == 'Member']
        path = self.parent.bbo_include_file.get()
        with open(path, 'w', encoding='utf8') as f_allowed:
            f_allowed.write('\n'.join(sorted(allowed)))
        self.comparison = Compare(self.parent)
        self._populate_allowed_tree()

    def _get_names_tree(self, master: tk.Frame) -> ttk.Treeview:
        """Return  a tree widget."""
        tree = ttk.Treeview(
            master,
            selectmode='browse',
            height=15,
            show='headings',
            )
        # tree.bind('<<TreeviewSelect>>', self._tree_clicked)
        # tree.bind('<Button-3>', self._show_context_menu)

        col_list = tuple(col[0] for col in TREE_COLUMNS)

        tree['columns'] = col_list
        for col in TREE_COLUMNS:
            (col_key, col_text, col_width) = (col[0], col[1], col[2])
            tree.heading(col_key, text=col_text,
                         command=lambda c=col_key:
                         sort_treeview(tree, c, False))
            tree.column(col_key, width=col_width, anchor=tk.W)
        # tree.column(<'right-align-column-name'>, stretch=0, anchor=tk.E)
        return tree

    def _populate_names_tree(self) -> None:
        self.names_tree.delete(*self.names_tree.get_children())
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
        with open(path, 'w', encoding='utf8') as f_allowed:
            f_allowed.write('\n'.join(sorted(names)))
        self.comparison = Compare(self.parent)
        self._populate_names_tree()

    def _process(self, *args) -> None:
        ...

    def _dismiss(self, *args) -> None:
        self.root.destroy()
