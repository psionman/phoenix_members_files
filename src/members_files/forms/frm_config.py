"""ConfigFrame for Phoenix Members Files."""

import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

from psiutils.buttons import ButtonFrame, Button, IconButton
from psiutils.constants import PAD, Pad
from psiutils.utilities import window_resize

from constants import APP_TITLE
from config import read_config, save_config
import text


class ConfigFrame():
    """
    A configuration dialog for editing application settings.

    This class creates a modal top-level window allowing the user to view
    and update configuration values such as file paths and other settings.

    Attributes:
        root (tk.Toplevel): The top-level window for the dialog.
        parent (ModuleCaller): The calling parent object.
        config (Config): The loaded configuration object.
        xxx (tk.StringVar): A Tk variable bound to a configuration value.
        data_directory (tk.StringVar): Tk variable for the data directory path.
        button_frame (ButtonFrame): Frame containing Save/Exit buttons.

    Methods:
        show(): Set up and display the form GUI.
        _main_frame(master): Build the main content frame.
        _button_frame(master): Build the frame containing action buttons.
        _value_changed(): Return True if any config field was modified.
        _enable_buttons(*args): Enable buttons based on config change.
        _get_data_directory(*args): Prompt user to select a directory.
        _save_config(*args): Save changes and exit the dialog.
        _dismiss(*args): Close the dialog window.
    """

    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.config = read_config()

        # tk variables
        self.xxx = tk.StringVar(value=self.config.xxx)
        self.data_directory = tk.StringVar(value=self.config.data_directory)

        self.data_directory.trace_add('write', self._enable_buttons)

        self.show()

    def show(self) -> None:
        """
        Initialize and display the configuration form GUI.

        This method configures the top-level window, sets up geometry,
        keybindings, resizability, and embeds the main and button frames.
        It also includes a sizegrip widget for manual resizing.

        Keybindings:
            - Ctrl+X: Close the dialog.
            - Ctrl+S: Save configuration and exit.
            - <Configure>: Trigger window size persistence on resize.

        Layout:
            - A main frame with form fields.
            - A button frame with Save and Exit buttons.
            - A sizegrip for resizing support.
        """
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.transient(self.parent.root)
        root.title(f'{APP_TITLE} - {text.CONFIG}')

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-s>', self._save_config)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=8, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        """
        Create and return the main frame containing form input widgets.

        This frame includes:
            - A label describing the input field.
            - An entry widget bound to the data_directory variable.
            - A button to open a directory selection dialog.

        The frame is configured to allow resizing and proper layout behaviour
        using row and column weights.

        Args:
            master (tk.Frame): The parent widget to contain the frame.

        Returns:
            ttk.Frame: The constructed main frame with input controls.
        """
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0
        label = ttk.Label(frame, text='xxx')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.data_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)

        # button = ttk.Button(
        #     frame, text=text.ELLIPSIS, command=self._get_data_directory)
        button = IconButton(frame, text.OPEN, 'open', self._get_data_directory)
        button.grid(row=row, column=2, padx=Pad.W)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        """
        Create and return the button frame for the form.

        This frame contains two buttons:
            - 'Save' to store the current configuration and exit.
            - 'Exit' to close the window without saving changes.

        The buttons are initially disabled and will be enabled based on user
        interaction. The frame is laid out horizontally.

        Args:
            master (tk.Frame): The parent widget that will contain the frame.

        Returns:
            tk.Frame: The constructed frame containing the control buttons.
        """
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('save', True, self._save_config),
            frame.icon_button('exit', False, self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _value_changed(self) -> bool:
        """
        Determine whether any configuration value has changed.

        Compares the current state of the form's variables with the saved
        configuration to identify changes made by the user.

        Returns:
            bool: True if at least one value has been altered; False otherwise.
        """
        return (
            self.xxx.get() != self.config.xxx or
            ...
        )

    def _enable_buttons(self, *args) -> None:
        """
        Enable or disable form buttons based on changes in configuration.

        Checks whether any tracked values have changed and enables the form's
        buttons accordingly to allow the user to save or exit.
        """
        enable = bool(self._value_changed())
        self.button_frame.enable(enable)

    def _get_data_directory(self, *args) -> None:
        """
        Prompt the user to select a new data directory and update the value.

        Opens a directory selection dialog, and if a valid directory is
        chosen, updates the corresponding Tkinter variable.
        """
        data_directory = filedialog.askdirectory(
            initialdir=Path(self.data_directory.get()),
            parent=self.root,
        )
        if data_directory:
            self.data_directory.set(data_directory)

    def _save_config(self, *args) -> None:
        """
        Save the current configuration and close the application window.

        Updates the configuration with values from the form, writes them to
        persistent storage, and then closes the config window.
        """
        # To generate assignments from tk-vars run script: assignment-invert
        self.config.update('xxx', self.xxx.get())
        save_config(self.config)
        self._dismiss()

    def _dismiss(self, *args) -> None:
        """
        Close the configuration window and terminate the application.

        Destroys the top-level window associated with the configuration form.
        """
        self.root.destroy()
