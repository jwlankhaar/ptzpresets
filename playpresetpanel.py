import tkinter as tk
import tkinter.messagebox 
import tkinter.ttk as ttk
from typing import Text

import ptzpresets.presetpanel as presetpanel


root = ttk.Frame()
camera_panel = presetpanel.PresetPanel(master=root)
camera_panel.create_generalwidgets()
camera_panel.set_camera_name('Camera 1')
camera_panel.create_presetbuttons(5)
camera_panel.position_widgets()
def button_callback(event):
    tkinter.messagebox.showinfo(message=event.widget.state())
    event.widget.state(['selected', '!pressed', '!active'])
    # camera_panel.refresh()
    print(event.widget.state())
    if event.state_decoded == '<Control-Button-1>':
        camera_panel.refresh()
        tkinter.messagebox.showinfo(message='Test na refresh')
        event.widget.state('normal')
camera_panel.register_presetbutton_callbacks([button_callback, button_callback], indices=[0, 1])


camera_panel.pack(side=tk.LEFT, anchor=tk.NW)

cam_2 = presetpanel.PresetPanel(master=root)
cam_2.create_generalwidgets()
cam_2.create_presetbuttons(3)
cam_2.position_widgets()
cam_2.pack(side=tk.LEFT, anchor=tk.NW)


root.pack(anchor=tk.NW)
root.mainloop()