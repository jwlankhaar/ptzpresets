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
    camera: camera
        the camera object the button is associated with
    ptz_response_handler: callable
        callable that handles the response of th PTZ callables

    Methods
    -------
    trigger_rename_preset:
        starts the rename preset flow
    """ 
    def __init__(self, master=None, preset_token=None, preset_name=None, 
        preset_num=None, camera=None, response_handler=None, 
        *args, **kwargs):
        
        super().__init__(master=master, *args, **kwargs)
        self.preset_token = preset_token
        self.preset_name = preset_name
        self.preset_num = preset_num

        self.camera = camera
        self.ptz_goto_preset = camera.goto_preset
        self.ptz_set_preset = camera.set_preset
        self.ptz_rename_preset = camera.rename_preset
        self.ptz_delete_preset = camera.delete_preset
        self.response_handler = response_handler

        self.config(style='FixedWidthSmallTextLeft.TButton')
        self._update_button_text()

        self.bind('<Button-1>', self._goto_preset)
        self.bind('<Shift-Button-1>', self._set_preset)
        self.bind('<Control-Button-1>', self.trigger_rename_preset)
        self.bind('<Alt-Button-1>', self._delete_preset)

    def trigger_rename_preset(self, event=None):
        """Place a text entry in the button. Set focus to the entry. The entry 
        text will be used as the new preset name. 
        """
        entry_text = tk.StringVar(master=self.master, value=self.preset_name)
        entry = tk.Entry(
            relief=tk.FLAT,
            master=self,
            exportselection=False,
            textvariable=entry_text
        )
        entry.bind('<FocusIn>', lambda e: e.widget.select_range(start=0, end=tk.END))
        entry.bind('<Return>', lambda e: self._rename_preset(entry=e.widget))
        entry.bind('<Escape>', lambda e: e.widget.forget())
        entry.pack(expand=tk.YES, fill=tk.X, side=tk.TOP, anchor=tk.CENTER)
        entry.focus()

    def _rename_preset(self, entry):
        """Rename the preset by calling the PTZ service, update the button text 
        and destroy the text entry.
        """
        self.preset_name = entry.get()
        response = self.ptz_rename_preset(self.preset_token, self.preset_name)
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
        response = self.ptz_set_preset(self.preset_name, self.preset_token)
        self.response_handler(
            camera=self.camera,
            action='set',
            response=response,
            arguments={
                'preset_token': self.preset_token
            }
        )

    def _goto_preset(self, event):
        response = self.ptz_goto_preset(self.preset_token)
        self.response_handler(
            camera=self.camera,
            action='goto',
            response=response,
            arguments={
                'preset_token': self.preset_token
            }
        )

    def _delete_preset(self, event):
        response = self.ptz_delete_preset(self.preset_token)
        self.response_handler(
            camera=self.camera,
            action='delete',
            response=response,
            arguments={
                'preset_token': self.preset_token
            }
        )
