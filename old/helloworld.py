#coding: utf-8

import json
import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import onvif


CONFIG_FILE = pathlib.Path('config_dev.json')


class Application(ttk.Frame):

    def __init__(self, parent=None, title='', config=None, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        self.master.title(title)
        self.config = config
        self.create_cameras()
        self.create_widgets()
        self.position_widgets()

    def create_cameras(self):
        self.cameras = [Camera(config=self.config[c]) for c in self.config]

    def create_widgets(self):
        self.camera_labels = []
        self.camera_buttons = [] 
        for cam in self.cameras:
            self.camera_labels.append(ttk.Label(text=cam.name))
            self.camera_buttons.append([
                self.create_camera_button(
                    camera=cam, 
                    preset_num=i+1, 
                    preset_name=pname
                ) for i, pname in enumerate(cam.get_preset_names())
            ])

    def create_camera_button(self, camera, preset_num, preset_name):
        return ttk.Button(
            text=f'{preset_num:02} {preset_name}',
            command=lambda: camera.goto_preset(preset_name)
        )

    def position_widgets(self):
        for i, lb in enumerate(self.camera_labels):
            lb.grid(row=0, column=i)
        for i, cbuttons in enumerate(self.camera_buttons):
            for j, btn in enumerate(cbuttons):
                btn.grid(column=i, row=j+1)





def read_config(config_file):
    """Read the JSON configuration file. Turn it into a dictionary
    with the camera name as key and the camera's configuration as value.
    """
    with open(config_file, 'r') as f:
        return {c['cameraname']: c for c in json.load(f)}
    

if __name__ == '__main__':
    config = read_config(CONFIG_FILE)
    root = tk.Tk()
    window = Application(parent=root, title='PTZ presets', config=config)
    root.mainloop()
