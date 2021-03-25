import time
import tkinter as tk
import tkinter.ttk as ttk

import ptzpresets.styles as styles

class Statusbar(ttk.Label):
    """Subclass of ttk.Label for a statusbar.

    Add a status bar to the parent widget.

    Attributes
    ----------
    message: string
        The actual status string of the statusbar.
    display_text: string
        What is displayed on the statusbar (may be equal
        to message or a truncated or differently formatted
        version of message).
    
    Methods
    -------
    update_(message): 
        Set the status bar text.
    alert(message, duration_seconds=2): 
        Show a status bar text temporarily. Restore the previous
        message afterwards.
    clear(): 
        Remove the status bar text.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master, 
            style='Statusbar.TLabel', 
            *args, **kwargs
        )        
        self['background'] = 'white'
        self.message = ''
        self.display_text = tk.StringVar(master=self.master)
        self.config(textvariable=self.display_text)

    def update_(self, message):
        self.message = message
        self.display_text.set(f'{message}')

    def alert(self, message, duration_seconds=2):
        """Show a message for a short period of time and reset the
        status bar text to its original text.
        """
        current_text = self.message
        self.update_(message)
        self.after(duration_seconds*1000, lambda t=current_text: self.update_(t))

    def clear(self):
        self.update_(message='')

