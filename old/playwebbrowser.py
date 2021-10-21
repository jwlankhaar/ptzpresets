import webbrowser

import tkinter as tk
import tkinter.ttk as ttk

from pathlib import Path

HELP_FILE = Path('static') / 'help.html'


def show_help():
    webbrowser.open_new(HELP_FILE)


frame = ttk.Frame()
button = ttk.Button(master=frame, text='Help', command=show_help)
button.pack(padx=50, pady=50)
frame.pack()
frame.mainloop()