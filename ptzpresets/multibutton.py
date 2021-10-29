#coding: utf-8

"""MultiButton class that subclasses the ttk.Button class.
"""


import tkinter as tk
import tkinter.ttk as ttk


class MultiButton(ttk.Button):
    """Multifunctional subclass of ttk.Button.

    Adds a rename functionality with a text entry and facilitates easy 
    capturing of button clicks combined with Shift, Alt and Control keys. 
    Also facilitates easy highlighting of button.

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
    is_highlighted: boolean
        Flag that indicates whether the button is highlighted.

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
        self.__is_highlighted = False
        
        if callback:
            self.register_callback(callback)
            
    def register_callback(self, callback):
        event_patterns = [
            '<ButtonRelease-1>', 
            '<Shift-ButtonRelease-1>', 
            '<Control-ButtonRelease-1>', 
            '<Alt-ButtonRelease-1>'
        ]
        for pattern in event_patterns:
            self.bind(pattern, MultiButton._add_decoded_event_state(callback), 
                      add='+')

    def get_name(self):
        if self.number is not None:
            return self['text'].split(' ', maxsplit=1)[1]
        else:
            return self['text']

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
        self.__is_highlighted = True

    def playdown(self):
        self.config(style=self.default_style)
        self.current_style = self.default_style
        self.__is_highlighted = False
        
    @property
    def is_highlighted(self): return self.__is_highlighted
    
    def _ask_new_name(self):
        self._is_renaming.set(True)
        entry_text = tk.StringVar(master=self, value=self.get_name())
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
        
    def _set_text(self, name):
        if self.number is not None:
            text = f'{self.number:02} {name}'
        else:
            text = name
        self.config(text=text)

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
    def _decode_event_sequence(event):
        """Decode the event state and keys to a human-readible event
        sequence of the form <[modifier]...event type [detail]>.
        """
        # Checking the modifiers bit by bit is adapted from the 
        # tkinter.Event.__repr__ method (in Lib/tkinter/__init__.py).
        modifiers = ('Shift', 'CapsLock', 'Control',
                     'Mod1', 'NumLock', 'Mod3', 'Mod4', 'Mod5',
                     'Button-1', 'Button-2', 'Button-3', 'Button-4', 'Button-5')
                    # Refined according to the modifier masks table in
                    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/event-handlers.html
        used_modifiers = []
        used_detail = []
        # Alt is a special case (https://stackoverflow.com/a/61998948).
        if event.state & 0x20000:
            used_modifiers.append('Alt')
        for i, name in enumerate(modifiers):
            if event.state & (1 << i) and not name.startswith('Mod'):
                # Ignore Mod# because the meaning is unclear.
                if i < 8: # Buttons should not be regarded as modifier.
                    used_modifiers.append(name)
                else:   
                    used_detail.append(name)
        if event.type.name in ['KeyPress', 'KeyRelease']:
            used_detail.append(chr(event.keysym_num))
        
        sequence_items = [*used_modifiers, event.type.name, *used_detail]
        if len(sequence_items) == 0:
            sequence_items.append('Other')
        return f'<{"-".join(sequence_items)}>'

    @staticmethod
    def _add_decoded_event_state(func):
        """Decorate the event with the decoded event state.
        """
        def wrapper(event):
            event.state_decoded = MultiButton._decode_event_sequence(event)
            return func(event)
        return wrapper
        



