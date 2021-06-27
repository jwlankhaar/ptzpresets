# coding: utf-8

"""
    PresetPanel class that holds the widgets
    belonging to a camera.
"""

import tkinter as tk
import tkinter.ttk as ttk

import ptzpresets.multibutton as multibutton
import ptzpresets.styles as styles

#TODO: Document PresetPanel class.
class PresetPanel(ttk.Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.cameralabel = None
        self.presetbuttons = []
        self.addbutton = None
        
    def create_generalwidgets(self):
        self.cameralabel = self._create_cameralabel()
        self.addbutton = self._create_addbutton()

    def create_presetbuttons(self, num_presets):
        for i in range(num_presets):
            self.presetbuttons.append(
                multibutton.MultiButton(
                    master=self,
                    text='Preset',
                    number=i+1,
                    default_style='PresetButton.TButton',
                    highlight_style='Highlighted.PresetButton.TButton',
                    callback=None
                )
            )
            
    def position_widgets(self):
        self.cameralabel.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=1)
        for btn in self.presetbuttons:
            btn.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=1)
        self.addbutton.pack(side=tk.TOP, expand=True)
    
    def set_camera_name(self, camera_name):
        self.cameralabel['text'] = camera_name
    
    def set_presetbutton_names(self, names, indices=None):
        if not indices:
            indices = range(len(self.presetbuttons))
        for i, name in zip(indices, names):
            self.presetbuttons[i].rename(name)
                
    def register_presetbutton_callbacks(self, callbacks, indices=None):
        if not indices:
            indices = range(len(self.presetbuttons))
        for i, callback in zip(indices, callbacks):
            self.presetbuttons[i].register_callback(callback)
    
    def register_addbutton_callback(self, callback):
        self.addbutton.bind('<Button-1>', callback)
    
    def delete_presetbutton(self, index):
        btn = self.presetbuttons.pop(index)
        btn.destroy()
    
    def refresh(self):
        for widget in self.winfo_children():
            widget.forget()
        self.position_widgets()

    def _create_cameralabel(self):
        label = ttk.Label(
            master=self,
            text='',
            style='TLabel'
        )
        return label

    def _create_addbutton(self):
        img_default = styles.ADDPRESET_BUTTON_DEFAULT
        img_hover = styles.ADDPRESET_BUTTON_HOVER
        btn = ttk.Label(master=self, image=img_default)
        btn.bind('<Enter>', lambda e, i=img_hover: e.widget.config(image=i))
        btn.bind('<Leave>', lambda e, i=img_default: e.widget.config(image=i))
        return btn    
