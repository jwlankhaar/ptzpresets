#coding: utf-8

"""MultiButton class that subclasses the ttk.Button class.
"""


import tkinter as tk
import tkinter.ttk as ttk


class MultiButton(ttk.Button):
    """Multifunctional subclass of ttk.Button.

    It adds a rename functionality with a text entry and facilitates easy 
    capturing of button clicks combined with Shift, Alt and Control keys. 
    It also facilitates easy highlighting of button.

    Attributes
    ----------
    master: <tk parent>
        A parent object for the widget.
    text: string
        Button text.
    number: integer
        A button number. The button text is prepended with the number 
        (zero-padded).
    default_style: string
        The name of the ttk style that is used by default for the button 
        (should descend from the TButton style).
    highlight_style: string
        The name of the ttk style that is used to highlight the button 
        (should descend from the TButton style).
    callback: callable
        The callable that is used to handle the click events (should 
        accept an event argument). The event object passed to the callback 
        has an additional attribute state_decoded that contains the captured 
        event in the same notation as used for the binding (e.g. '<Button-1>' 
        for a regular click).    

    Methods
    -------
    rename(new_name=None):
        If new_name is None, ask for a new name in a text entry within the 
        button. Otherwise, rename the button.
    get_name:
        Return the button name.
    highlight:
        Apply the highlight style to the button.
    playdown:
        Apply the default style to the button (i.e. turn highlighting off)
    """
    def __init__(self, master=None, text=None, number=None, default_style=None, 
                 highlight_style=None, callback=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
             
        self.default_style = default_style or 'TButton'
        self.highlight_style = highlight_style or 'TButton'
        self.current_style = default_style or 'TButton'
        
        self.number = number
        self._set_text(text)
        self.config(style=default_style)

        self._is_renaming = tk.BooleanVar(value=False)

        def event_state_decorator(func):
            """Wrap the callback to add the decoded event state to the 
            event.
            """
            def wrapper(event):
                event.state_decoded = self._add_decoded_event_state(event.state)
                return func(event)
            return wrapper
        events = [
            '<Button-1>', 
            '<Shift-Button-1>', 
            '<Control-Button-1>', 
            '<Alt-Button-1>'
        ]
        for type in events:
            self.bind(type, event_state_decorator(callback))

    def _set_text(self, name):
        if self.number is not None:
            text = f'{self.number:02} {name}'
        else:
            text = name
        self.config(text=text)

    def get_name(self):
        return self['text'].split(' ', maxsplit=1)[1]

    def rename(self, new_name=None):
        if not new_name:
            self._ask_new_name()
            self.wait_variable(self._is_renaming)
            new_name = self.get_name()
        else:
            self._set_text(new_name)
        return new_name

    def highlight(self):
        self.config(style=self.highlight_style)
        self.current_style = self.highlight_style

    def playdown(self):
        self.config(style=self.default_style)
        self.current_style = self.default_style

    def _ask_new_name(self):
        self._is_renaming.set(True)
        entry_text = tk.StringVar(master=self.master, value=self.get_name())
        entry = tk.Entry(
            master=self,
            relief=tk.FLAT,
            exportselection=False,
            textvariable=entry_text
        )
        entry.bind('<FocusIn>', lambda e: e.widget.select_range(start=0, end=tk.END))
        entry.bind('<Return>', lambda e: self._close_rename(e.widget))
        entry.bind('<Escape>', lambda e: self._cancel_rename(e.widget))
        entry.pack(expand=tk.YES, fill=tk.X, side=tk.TOP, anchor=tk.CENTER)
        entry.focus()

    def _close_rename(self, entry):
        new_name = entry.get()
        entry.destroy()
        self._refresh()
        self._set_text(new_name)
        self._is_renaming.set(False)

    def _cancel_rename(self, entry):
        entry.destroy()
        self._refresh()
        self._is_renaming.set(False)

    def _refresh(self):
        self.config(text=self['text'])
        # Resetting the text seems to be sufficient for an update.

    @staticmethod
    def _add_decoded_event_state(state):
        states = {
            0x8: '<Button-1>',
            0xc: '<Control-Button-1>',
            0xd: '<Control-Shift-Button-1>',
            0x9: '<Shift-Button-1>',
            0x20008: '<Alt_L-Button-1>',
            0x20009: '<Alt_L-Shift-Button-1>',
            0x2000c: '<Alt-Control-1>',
            0x2000d: '<Alt_R-Shift-Button-1>'
        }
        # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/event-handlers.html 
        # (refer to the state value)
        return states.get(state, '<Other>')




