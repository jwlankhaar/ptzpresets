#coding: utf-8


import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

import pathlib

from ptzpresets.styles import *


def msgbox(text):
    tkinter.messagebox.showinfo(title='Info', message=text)

def on_control_click(event, button):
    # Get preset_token
    preset_token = '19840811'
    new_name = tk.StringVar()
    new_name.set(button['text'])
    button_width = button.winfo_width() // CHAR_WIDTH_PX - 1
    entr = tk.Entry(
        relief=tk.FLAT,
        master=button.master,
        exportselection=False,
        width=button_width,
        textvariable=new_name
    )
    entr.select_range(start=0, end=tk.END)
    entr.bind('<FocusIn>', lambda x: entr.select_range(start=0, end=tk.END))
    entr.bind('<Return>', lambda e: rename_preset(e, new_name, preset_token, entr, btn))
    entr.bind('<Escape>', lambda x: entr.destroy())
    entr.grid(
        row=button.grid_info()['row'], 
        column=button.grid_info()['column'], 
        padx=button.grid_info()['padx']
    )
    entr.focus()


def rename_preset(event, textvar, preset_token, entry, button):
    btn['text'] = textvar.get()
    print(f'{preset_token}: {textvar.get()}')
    #TODO: call rename pre
    # 
    # et here
    entry.destroy()


# Bij CTRL+CLICK:
# get button text
# Clear button text
# Show entry on top of button
# Add button text to entry
# Select entry text
# On ENTER:
# Hide entry
# Set button text
# Save preset name to preset with token

# root = tk.Tk()
root = ttk.Frame(master=None)
btn = ttk.Button(
    master=root.master,
    text='Dit is een test'
)
btn.bind('<Button-1>', lambda x: msgbox('Echt een test!'))
btn.bind('<Shift-Button-1>', lambda x: msgbox('Deze boodschap geeft het een SHIFT!!!!'))
btn.bind('<Control-Button-1>', lambda x: on_control_click(x, btn))
btn.grid(row=0, column=0, padx=15, pady=15)
root.mainloop()


