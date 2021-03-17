#coding: utf-8

"""
    Application class that defines the GUI (including its business logic).
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsgbox

import ptzpresets.presetbutton as presetbutton
import ptzpresets.camera as camera
import ptzpresets.styles as styles
import ptzpresets.statusbar as statusbar

from pathlib import Path


APP_TITLE = 'PTZ Presets'
HELP_FILE = Path('static') / 'help.txt'


class Application(ttk.Frame):
    def __init__(self, master=None, config=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.master.title(APP_TITLE)
        self.config = config
        self.create_cameras()

        self.create_frames()
        self.create_camera_widgets()
        self.create_general_widgets()
        self.position_frames()
        self.position_camera_widgets()
        self.position_general_widgets()

    def create_cameras(self):
        self.cameras = [
            camera.Camera(config=self.config[c]) 
            for c in self.config
        ]

    def create_frames(self):
        self.body = ttk.Frame(master=self.master)
        self.footer = ttk.Frame(master=self.master)

    def create_camera_widgets(self):
        self.labels_camera = []
        self.buttons_presets = []
        self.buttons_add_preset = [] 
        for cam in self.cameras:
            self.labels_camera.append(
                ttk.Label(master=self.body, text=cam.name, style='TLabel')
            )
            self.buttons_presets.append([
                presetbutton.PresetButton(
                    master=self.body,
                    preset_token=cam.preset_tokens[pname],
                    preset_name=pname,
                    preset_num=i+1,
                    camera=cam,
                    response_handler=self.ptz_response_handler
                ) for i, pname in enumerate(cam.list_preset_names())
            ])
            self.buttons_add_preset.append(self.create_add_preset_button(cam))

    def create_add_preset_button(self, camera):
        btn = ttk.Label(master=self.body, image=styles.BUTTON_ADD_PRESET_DEFAULT)
        btn.bind('<Button-1>', lambda e, c=camera: self.add_new_preset(c))
        btn.bind('<Enter>', lambda e: e.widget.config(image=styles.BUTTON_ADD_PRESET_HOVER))
        btn.bind('<Leave>', lambda e: e.widget.config(image=styles.BUTTON_ADD_PRESET_DEFAULT))
        return btn

    def create_general_widgets(self):
        self.button_refresh = ttk.Label(
            master=self.footer, 
            text=u'\U0001F5D8',
            background='white',
            style='SmallTextLeft.TLabel',
            width=3
        )
        self.button_refresh.bind('<Button-1>', self.refresh_presets)
        self.statusbar = statusbar.Statusbar(master=self.footer)
        self.button_help = ttk.Label(
            master=self.footer,
            text='?',
            background='white',
            style='SmallTextLeft.TLabel',
            width=2
        )
        self.button_help.bind('<Button-1>', self.show_help)

    def position_frames(self):
        self.body.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)
        self.footer.pack(expand=tk.NO, fill=tk.X, side=tk.BOTTOM, pady=(10,0))

    def position_camera_widgets(self):
        for i, camlabel in enumerate(self.labels_camera):
            camlabel.grid(row=0, column=i)
            for j, btn in enumerate(self.buttons_presets[i]):
                btn.grid(column=i, row=j+1, padx=5, pady=1)
            self.buttons_add_preset[i].grid(column=i, row=j+2)

    def position_general_widgets(self):
        self.button_refresh.grid(row=0, column=0)
        self.statusbar.grid(row=0, column=1, sticky=tk.E+tk.W)
        self.button_help.grid(row=0, column=2)
        self.statusbar.master.columnconfigure(1, weight=1)  # Stretch statusbar only 

    def add_new_preset(self, camera):
        preset_token = camera.set_preset()
        self.refresh_presets(silent=True)
        preset_button = self._get_preset_button(preset_token)
        preset_button.trigger_rename_preset()

    def _get_preset_button(self, preset_token):
        for cbuttons in self.buttons_presets:
            for btn in cbuttons:
                if btn.preset_token == preset_token:
                    return btn
        
    def refresh_presets(self, event=None, silent=False):
        if not silent:
            self.statusbar.update('Reloading presets...')
        for w in self.body.winfo_children():
            w.destroy()
        for cam in self.cameras:
            cam.refresh()
        self.create_camera_widgets()
        self.position_camera_widgets()
        if not silent:
            self.statusbar.update('')

    def show_help(self, event):
        window = tk.Toplevel()
        window.title('PTZ Presets Help')
        help_txt = open(HELP_FILE, 'rt', encoding='utf8').read().replace('\\t', '\t')
        txt_widget = tk.Text(
            master=window, 
            font=styles.system_font(), 
            relief=tk.FLAT,
            background=window['background']
        )
        txt_widget.insert(index=tk.END, chars=help_txt)
        btn_ok = ttk.Button(master=window, text='OK', command=window.destroy)
        txt_widget.pack(padx=20)
        btn_ok.pack(pady=20)
        
    def ptz_response_handler(self, camera, action, response, arguments):
        preset_token = arguments['preset_token']
        preset_name = camera.preset_names[preset_token]
        if action == 'goto':
            self.statusbar.alert(
                f'{camera.name}: Going to preset {preset_name} ({preset_token})'
            )
        elif action == 'set':
            self.statusbar.alert(
                f'{camera.name}: Saved current position as {preset_name} ({preset_token})'
            )
        elif action == 'rename':
            self.statusbar.alert(
                f'{camera.name}: Renamed preset ({preset_token}) to {arguments["new_name"]}'
            )
        elif action == 'delete':
            self.refresh_presets()
            self.statusbar.alert(
                f'{camera.name}: Preset {preset_name} ({preset_token}) deleted'
            )

