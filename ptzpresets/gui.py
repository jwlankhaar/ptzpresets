# coding: utf-8

"""
    Gui classes that serve as an interface to Tk.
"""

import pathlib
import tkinter as tk
import tkinter.constants
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.ttk as ttk
import tkcalendar


import ptzpresets.constants
import ptzpresets.widgets


class Gui(ttk.Frame): 
    """
    GUI class derived from ttk.Frame.

    Arguments:
    - parent: The parent widget containing the GUI. If none, the GUI is
    considered the root.

    To add and position widgets to the GUI override the methods
    create_widgets() and position_widgets(). These methods should
    be called in the derived class. In position_widget() the .grid()
    or .pack() methods of the widgets should be called.

    Properties:
    
    - current_dir: Current directory for file/directory dialogs.

    Methods:

    - create_widgets(): To be implemented on instantiation.
    - position_widgets(): To be implemented on instantiation.  

    - askopenfilename(): Invoke a file open dialog.
    - askdirectory(): Invoke a select directory dialog.
    - create_booleanvar(): Create a traceable boolean variable.
    - create_button(): Create a button widget.
    - create_checkbutton(): Create a checkbutton (checkbox) widget.
    - create_datepicker(): Create a datepicker widget.
    - create_label(): Create a label widget.
    - create_treeview(): Create a treeview widget.
    - add_statusbar(): Add a status bar widget.
    - showerrorwindow(): Show an error window.
    - showinfo(): Show a message box.
    - update_cursor_busy(): Set mouse cursor busy.
    - update_cursor_reset(): Reset the mouse cursor.
    - update_statusbar(): Change status bar message.
    - update_statusbar_reset(): Clear status bar message.
    """

    def __init__(self, parent=None, *args, **kwargs):
        if not parent:
            parent = tk.Tk()
        super().__init__(master=parent, *args, **kwargs)
        self.const = ptzpresets.constants.GuiEnum()
        self.__current_dir = pathlib.Path.home()

    @property
    def current_dir(self): return self.__current_dir

    @current_dir.setter
    def current_dir(self, value):
        path = pathlib.Path(value)
        if path.exists():
            if path.is_file():
                self.__current_dir = path.parent    # Strip filename.
            else:
                self.__current_dir = path

    def create_widgets(self):
        """Define the GUI widgets. To be implemented on instantiation."""
        pass

    def position_widgets(self):
        """Position the GUI widgets on a grid. To be implemented on 
        instantation.
        """
        pass

    def askopenfilename(self, *args, **kwargs):
        """Show a dialog box for opening a file. Return the full path
        and filename as a pathlib.Path object. Use the GUI's current 
        directory if no initialdir is specified as argument. Update the
        GUI's current directory. Update the label text if a path_label 
        object is specified.
        """
        if 'initialdir' not in kwargs.keys():
            kwargs['initialdir'] = self.current_dir
        if 'path_label' in kwargs.keys():
            widget_label = kwargs.pop('path_label')
        else:
            widget_label = None
        path = pathlib.Path(
            tkinter.filedialog.askopenfilename(
                *args, 
                **kwargs
            )
        )
        self.current_dir = path.parent
        if widget_label:
            widget_label.update(str(path))
        return path

    def askdirectory(self, *args, **kwargs):
        """Invoke a dialog box for selection of a directory. Return the
        full path as a pathlib.Path object. Use the GUI's current 
        directory if no initialdir is specified. Update the GUI's
        current directory. Update the label text if a path_label
        object is specified.
        """
        if 'initialdir' not in kwargs.keys():
            kwargs['initialdir'] = self.current_dir
        if 'path_label' in kwargs.keys():
            widget_label = kwargs.pop('path_label')
        else:
            widget_label = None
        path = pathlib.Path(
            tkinter.filedialog.askdirectory(
                *args, 
                **kwargs
            )
        )
        self.current_dir = path
        if widget_label:
            widget_label.update(str(path))
        return path

    def create_datepicker(self, date, command):
        """Create a date picker widget and bind event handler command
        to it that is called after a date has been selected. The default
        date is date.
        """
        dtpckr = tkcalendar.DateEntry(
            self.master,
            locale='nl_NL',
            firstweekday='sunday',
            width=15
        )
        dtpckr.set_date(date)
        dtpckr.bind('<<DateEntrySelected>>', command)
        return dtpckr

    def create_label(self, text):
        """Create and return a text label widget."""
        return ptzpresets.widgets.Label(master=self.master, text=text)

    def create_booleanvar(self, value=False):
        """Create and return a traceable boolean var."""
        return tk.BooleanVar(
            master=self.master,
            value=value
        )

    def create_button(self, text, command, underline=None, enabled=True):
        """Create and return a button widget with an accelerator key 
        binding. Underline the character with index underline (indicates
        the accelerator key) and bind an accelerator key event to the 
        <ALT> + <underlined character> combination. Use the underlined
        character in lowercase.
        """
        btn = ptzpresets.widgets.Button(
            master=self.master,
            text=text,
            underline=underline,
            command=command
        )
        if not enabled:
            btn.disable()
        if underline:
            accelerator_key = f'<Alt_L>{text[underline].lower()}'
            self.master.bind(accelerator_key, lambda e:command())
        return btn

    def create_checkbutton(self, text, variable, underline, command=None):
        """Create a checkbutton (i.e. a checkbox) widget with an 
        accelerator key binding to the key combination 
        <ALT> + <underlined character>. Use the underlined character 
        in lowercase.
        """
        chckbtn = ttk.Checkbutton(
            self.master,
            text=text,
            variable=variable,
            underline=underline,
            command=command
        )
        accelerator_key = f'<Alt_L>{text[underline].lower()}'
        self.master.bind(accelerator_key, lambda e:chckbtn.invoke())
        return chckbtn

    def create_statusbar(self):
        """Create and return a status bar widget."""
        stbr = ptzpresets.widgets.Statusbar(master=self.master)
        return stbr
 
    def show_errorwindow(self, *args, **kwargs):
        """Show an error window for error or exception details."""
        ErrorWindow(*args, **kwargs)

    def show_info(self, title='', message='', *args, **kwargs):
        """Show a message box."""
        return tkinter.messagebox.showinfo(
            title=title, 
            message=message, 
            *args, 
            **kwargs
        )

    def create_treeview(self, columns, columnwidths, headings, command):
        """Create and return a treeview widget."""
        trvw = ptzpresets.widgets.Treeview()
        trvw.setup(columns, columnwidths, headings, command)
        return trvw


class Window(Gui):
    """
    Class the defines a top-level (non-root) window.
    """

    def __init__(self, parent=None, *args, **kwargs):
        parent = tk.Toplevel(parent)
        super().__init__(parent=parent, *args, **kwargs)
        

class ErrorWindow(Window):
    """
        Class that defines a toplevel error window with a plain text
        text frame and a close button.
    """
    def __init__(self, parent=None, error_message='', window_title='Error'):
        super().__init__(parent=parent)
        self.master.title(window_title)
        self.master.minsize(400, 200)
        self.create_widgets()
        self.position_widgets()

        self.scrlldtxt.insert(tk.INSERT, chars=error_message)
    
    def create_widgets(self):
        scrlldtxt = tkinter.scrolledtext.ScrolledText(
            self.master, 
            wrap=tk.WORD,
            width=80,       # Characters. 
            height=10       # Lines.
        )
        scrlldtxt.configure(font=('Consolas', 10, ''))
        self.scrlldtxt = scrlldtxt
        self.btn_close = tkinter.ttk.Button(
            self.master, 
            text='Sluiten',
            command=self.master.destroy
        )
        
    def position_widgets(self):
        self.scrlldtxt.grid(row=0, column=0, columnspan=4, padx=25, pady=15, sticky=tk.EW)
        self.btn_close.grid(row=1, column=3,               padx=25, pady=15, sticky=tk.E)
