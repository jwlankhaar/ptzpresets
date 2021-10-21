#coding: utf-8

"""
    View class that defines the GUI.
"""

import tkinter as tk
import tkinter.ttk as ttk

from pathlib import Path

import ptzpresets.statusbar as statusbar
import ptzpresets.styles as styles

from ptzpresets import multibutton


APP_TITLE = 'PTZ Presets'
HELP_FILE = Path('static') / 'help.txt'


class View(ttk.Frame):
    def __init__(self, master=None, model=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.master.title(APP_TITLE)
        self.master.iconbitmap(styles.APP_ICON)
        self.create_frames()
        self.create_camera_widgets(model.presets)
        self.create_general_widgets()
        self.position_frames()
        self.position_camera_widgets()
        self.position_general_widgets()

    def create_frames(self):
        self.body = ttk.Frame(master=self.master)
        self.footer = ttk.Frame(master=self.master)

    def create_camera_widgets(self, presets):
        self.camera_labels = []
        self.preset_buttons = []
        self.add_preset_buttons = []
        for cname in presets.keys():
            self.camera_labels.append(
                ttk.Label(master=self.body, text=cname, style='TLabel')
            ) 
            for i, preset in enumerate(presets[cname].values()):
                button = multibutton.MultiButton(
                    master=self.body,
                    text=preset.name,
                    number=i+1,
                    default_style='PresetButton.TButton',
                    highlight_style='Highlighted.PresetButton.TButton',
                    callback=preset.callback
                )
                self.preset_buttons.append(button)
            add_button = self.create_add_preset_button(cname)
            self.add_preset_buttons.append(add_button)
        #TODO: move to controller
        # for cname in self.controller.cameras.keys():
        #     self.labels_camera.append(
        #         ttk.Label(master=self.body, text=cname, style='TLabel')
        #     )
        #     self.buttons_presets.append([
        #         multibutton.MultiButton(
        #             master=self.body, 
        #             text=p['name'], 
        #             number=i+1,
        #             default_style='PresetButton.TButton',
        #             highlight_style='Highlighted.PresetButton.TButton',
        #             callback=lambda e, c=cname, t=t: 
        #                 self.controller.process_preset_click(e, c, t)
        #         ) for i, (t, p) in enumerate(self.controller.presets[cname].items())
        #     ])
        #     self.controller.add_buttons_to_presets(cname, self.buttons_presets[-1])
        #     self.buttons_add_preset.append(self.create_add_preset_button(cname))
            
    def create_add_preset_button(self, camera_key):
        btn = ttk.Label(master=self.body, image=styles.ADDPRESET_BUTTON_DEFAULT)
        btn.bind('<Button-1>', lambda e, c=camera_key: self.controller.add_preset(e, c))
        btn.bind('<Enter>', lambda e, i=styles.ADDPRESET_BUTTON_HOVER: e.widget.config(image=i))
        btn.bind('<Leave>', lambda e, i=styles.ADDPRESET_BUTTON_DEFAULT: e.widget.config(image=i))
        return btn

    def create_general_widgets(self):
        self.button_refresh = ttk.Label(
            master=self.footer, 
            text=u'\U0001F5D8',
            background='white',
            style='Statusbar.TLabel',
            width=3
        )
        self.button_refresh.bind('<Button-1>', self.refresh)
        self.statusbar = statusbar.Statusbar(master=self.footer)
        self.button_help = ttk.Label(
            master=self.footer,
            text='?',
            background='white',
            style='Statusbar.TLabel',
            width=2
        )
        self.button_help.bind('<Button-1>', self.show_help)

    def position_frames(self):
        self.body.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)
        self.footer.pack(expand=tk.NO, fill=tk.X, side=tk.BOTTOM, pady=(10,0))

    def position_camera_widgets(self):
        for i, camlabel in enumerate(self.camera_labels):
            camlabel.grid(row=0, column=i)
            for j, btn in enumerate(self.preset_buttons[i]):
                btn.grid(column=i, row=j+1, padx=5, pady=1)
            self.add_preset_buttons[i].grid(column=i, row=j+2)

    def position_general_widgets(self):
        self.button_refresh.grid(row=0, column=0)
        self.statusbar.grid(row=0, column=1, sticky=tk.E+tk.W)
        self.button_help.grid(row=0, column=2)
        self.statusbar.master.columnconfigure(1, weight=1)  # Stretch statusbar only 

    def refresh(self, event=None, silent=False):
        if not silent:
            self.statusbar.inform('Reloading presets...')
        for w in self.body.winfo_children():
            w.destroy()
        for cam in self.controller.cameras.values():
            cam.refresh()
        self.create_camera_widgets()
        self.position_camera_widgets()
        for ckey in self.controller.cameras.keys():
            current_preset = self.controller.current_presets[ckey]
            if current_preset:
                self.controller.presets[ckey][current_preset]['button'].highlight()
        if not silent:
            self.statusbar.inform('')

    def show_status(self, message):
        self.statusbar.inform(message)

    def show_help(self, event):
        window = tk.Toplevel()
        window.title('PTZ Presets Help')
        window.iconbitmap(styles.APP_ICON)
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
        
    