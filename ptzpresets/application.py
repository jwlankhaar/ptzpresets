#coding: utf-8

"""
    Application class that defines the GUI (including its business logic).
"""


import ptzpresets.gui
import ptzpresets.camera


class Application(ptzpresets.gui.Gui):
    def __init__(self, parent=None, title='', config=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.master.title(title)
        self.config = config
        self.create_cameras()
        self.create_widgets()
        self.position_widgets()

    def create_cameras(self):
        self.cameras = [
            ptzpresets.camera.Camera(config=self.config[c]) 
            for c in self.config
        ]

    def create_widgets(self):
        self.camera_labels = []
        self.camera_buttons = [] 
        for cam in self.cameras:
            self.camera_labels.append(self.create_label(cam.name))
            self.camera_buttons.append([
                self.create_camera_button(
                    camera=cam, 
                    preset_num=i+1, 
                    preset_name=pname
                ) for i, pname in enumerate(cam.get_preset_names())
            ])

    def create_camera_button(self, camera, preset_num, preset_name):
        return self.create_button(
            text=f'{preset_num:02} {preset_name}',
            command=lambda: camera.goto_preset(preset_name)
        )

    def position_widgets(self):
        for i, lb in enumerate(self.camera_labels):
            lb.grid(row=0, column=i)
        for i, cbuttons in enumerate(self.camera_buttons):
            for j, btn in enumerate(cbuttons):
                btn.grid(column=i, row=j+1)


