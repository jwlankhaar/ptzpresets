import tkinter as tk
import tkinter.messagebox 

from ptzpresets import presetpanel
from ptzpresets import root


def button_callback(event):
    tkinter.messagebox.showinfo(message=event.widget.state())
    event.widget.state(['selected', '!pressed', '!active'])
    print(event.widget.state())
    if event.state_decoded == '<Control-Button-1>':
        cam1_panel.refresh()
        tkinter.messagebox.showinfo(message='Test na refresh')
        event.widget.state('normal')


cam1_panel = presetpanel.PresetPanel(master=root.root)
cam1_panel.set_cameraname('Camera 1')
cam1_panel.create_presetbuttons(5)
cam1_panel.register_presetbutton_callbacks(
    [button_callback, button_callback], button_indices=[0, 1])
cam1_panel.pack(side=tk.LEFT, anchor=tk.NW)

cam2_panel = presetpanel.PresetPanel(master=root.root)
cam2_panel.pack(side=tk.LEFT, anchor=tk.NW)

root.root.mainloop()