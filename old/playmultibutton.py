
import tkinter as tk

import ptzpresets.multibutton as multibutton

def ctrl_button1_callback(event):
    if event.state_decoded == '<Control-Button-1>':
        event.widget.rename()
    elif event.state_decoded == '<Shift-Button-1>':
        event.widget.highlight()
    elif event.state_decoded == '<Alt_L-Button-1>':
        event.widget.playdown()


app = tk.Tk()
import ptzpresets.styles
mbtn = multibutton.MultiButton(
    master=app, 
    text='Button', 
    callback=ctrl_button1_callback,
    regular_style='MultiButton.TButton',
    highlight_style='Highlighted.MultiButton.TButton'
)
mbtn.pack(padx=50, pady=50)
app.mainloop()
