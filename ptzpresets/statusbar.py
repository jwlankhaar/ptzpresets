import time
import tkinter as tk
import tkinter.ttk as ttk

import ptzpresets.styles as styles

class Statusbar(ttk.Label):
    """
        Class that adds a status bar to the current frame.

        Methods:
        - update(): Set the status bar text.
        - alert(): Show a status bar text temporarily.
        - clear(): Remove the status bar text.

        Property:
        - text: the status bar text.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master, 
            style='SmallTextLeft.TLabel', 
            *args, **kwargs
        )        
        self['background'] = 'white'
        self.message = ''
        self.display_text = tk.StringVar(master=self.master)
        self.config(textvariable=self.display_text)

    def update(self, message):
        self.message = message
        self.display_text.set(f'{message}')

    def alert(self, message, duration_seconds=2):
        """Show a message for a short period of time and reset the
        status bar text to its original text.
        """
        current_text = self.message
        self.update(message)
        self.after(duration_seconds*1000, lambda t=current_text: self.update(t))

    def clear(self):
        self.update(message='')

