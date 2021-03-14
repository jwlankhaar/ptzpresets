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
        super().__init__(*args, **kwargs)        
        self.master=master
        self['background'] = 'white'
        self.place(
            relx=0, 
            rely=1.0, 
            x=0, 
            y=0, 
            relwidth=1.0, 
            anchor=tk.SW
        )
        self.message = ''
        self.status_text = tk.StringVar(master=self.master)
        self.config(textvariable=self.status_text)

    def update(self, message):
        self.message = message
        self.status_text.set(f'  {message}')
        self.update_idletasks()

    def alert(self, message, duration_seconds=1):
        """Show a message for a short period of time and reset the
        status bar text to its original text.
        """
        current_text = self.message
        self.update(message)
        import time
        time.sleep(duration_seconds)
        self.update(current_text)

    def clear(self):
        self.update(message='')

