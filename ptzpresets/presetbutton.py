#coding: utf-8

"""
    PresetButton class for PTZ presets. 
"""

import tkinter as tk
import tkinter.ttk as ttk

import ptzpresets.styles as styles


class PresetButton(ttk.Button):
    """PresetButton class provides a tkinter.Button with 
    additional functionality, such as going to, setting and renaming
    a PTZ preset. Note that the button style (i.e. font size) is defined
    within the class.

    Attributes
    ----------
    preset_token: str
        the token that uniquely identifies the preset (ONVIF)
    preset_name: str
        the name of the preset
    button_num: int
        the ordinal number of the preset
    ptz_response_handler: callable
        callable that handles the response of th PTZ callables

    """ 
    def __init__(self, master=None, preset_token=None, preset_name=None, 
        preset_num=None, camera=None, response_handler=None, 
        *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.master=master
        self.preset_token = preset_token
        self.preset_name = preset_name
        self.preset_num = preset_num
        self.config(style='ButtonFixedWidthSmallTextLeft.TButton')
        self._update_button_text()

        self.camera = camera
        self.ptz_goto_preset = camera.goto_preset
        self.ptz_set_preset = camera.set_preset
        self.ptz_rename_preset = camera.rename_preset
        self.response_handler = response_handler

        # Bindings
        self.bind('<Button-1>', self._goto_preset)
        self.bind('<Shift-Button-1>', self._set_preset)
        self.bind('<Control-Button-1>', self._ask_new_presetname)

    def _ask_new_presetname(self, event):
        """Place an Entry widget on top of the button text. Make sure its width
        does not exceed that of the button. Set focus to the entry. The entry 
        text will be used as the new preset name. 
        """
        entry_width = self.winfo_width() // styles.CHAR_WIDTH_PX - 1
        entry_text = tk.StringVar(master=self.master, value=self.preset_name)
        entry = tk.Entry(
            relief=tk.FLAT,
            master=self.master,
            exportselection=False,
            width=entry_width,
            textvariable=entry_text
        )
        entry.select_range(start=0, end=tk.END)
        entry.bind('<FocusIn>', lambda e: entry.select_range(start=0, end=tk.END))
        entry.bind('<Return>', lambda e: self._rename_preset(entry=entry))
        entry.bind('<Escape>', lambda e: entry.destroy())

        # Position entry on top of button text.
        g = self.grid_info()
        entry.grid(row=g['row'], column=g['column'], padx=g['padx'])
        entry.focus()

    def _rename_preset(self, entry):
        """Rename the preset by calling the PTZ service, update the button text 
        and destroy the text entry.
        """
        self.preset_name = entry.get()
        response = self.ptz_rename_preset(
            preset_token=self.preset_token, 
            new_name=self.preset_name
        )
        self.response_handler(
            camera=self.camera,
            action='rename', 
            response=response, 
            arguments={
                'preset_token': self.preset_token, 
                'new_name': self.preset_name}
        )
        self._update_button_text()
        entry.destroy()

    def _update_button_text(self):
        """Set the button text formatted as <preset_num> <preset_name>.
        Truncate the preset name if it exceeds 20 characters.
        """ 
        button_text = f'{self.preset_num:02} {self.preset_name:.20}'
        self.config(text=button_text)

    def _set_preset(self, event):
        response = self.ptz_set_preset(
            preset_name=self.preset_name,
            preset_token=self.preset_token 
        )
        self.response_handler(
            camera=self.camera,
            action='set',
            response=response,
            arguments={
                'preset_token': self.preset_token
            }
        )

    def _goto_preset(self, event):
        response = self.ptz_goto_preset(preset_token=self.preset_token)
        self.response_handler(
            camera=self.camera,
            action='goto',
            response=response,
            arguments={
                'preset_token': self.preset_token
            }
        )



    


    

    
