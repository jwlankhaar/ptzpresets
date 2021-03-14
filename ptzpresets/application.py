#coding: utf-8

"""
    Application class that defines the GUI (including its business logic).
"""

import tkinter as tk
import tkinter.ttk as ttk

import ptzpresets.presetbutton
import ptzpresets.camera
import ptzpresets.styles
import ptzpresets.statusbar


class Application(ttk.Frame):
    def __init__(self, parent=None, title='', config=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.master.title(title)
        self.config = config
        self.create_cameras()
        self.create_widgets()
        self.position_widgets()
        self.master.minsize(0, 450)

    def create_cameras(self):
        self.cameras = [
            ptzpresets.camera.Camera(config=self.config[c]) 
            for c in self.config
        ]

    def create_widgets(self):
        self.camera_labels = []
        self.camera_buttons = [] 
        for cam in self.cameras:
            self.camera_labels.append(
                ttk.Label(
                    master=self.master,
                    text=cam.name
                )
            )
            self.camera_buttons.append([
                ptzpresets.presetbutton.PresetButton(
                    master=self.master,
                    preset_token=cam.preset_tokens[pname],
                    preset_name=pname,
                    preset_num=i+1,
                    camera=cam,
                    response_handler=self.ptz_response_handler
                ) for i, pname in enumerate(cam.list_preset_names())
            ])
            self.status_bar = ptzpresets.statusbar.Statusbar(master=self.master)

    def position_widgets(self):
        for i, lb in enumerate(self.camera_labels):
            lb.grid(row=0, column=i)
        for i, cbuttons in enumerate(self.camera_buttons):
            for j, btn in enumerate(cbuttons):
                btn.grid(column=i, row=j+1, padx=5, pady=1)

    def ptz_response_handler(self, camera, action, response, arguments):
        preset_token = arguments['preset_token']
        preset_name = camera.preset_names[preset_token]
        if action == 'goto':
            self.status_bar.alert(
                f'{camera.name}: Going to preset {preset_name} ({preset_token})'
            )
        elif action == 'set':
            self.status_bar.alert(
                f'{camera.name}: Saving position as {preset_name} ({preset_token})'
            )
        elif action == 'rename':
            self.status_bar.alert(
                f'{camera.name}: Renamed preset ({preset_token}) to {arguments["new_name"]}'
            )
            


        pass



