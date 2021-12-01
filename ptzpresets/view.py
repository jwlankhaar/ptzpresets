#coding: utf-8

"""
    View class that defines the GUI.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import webbrowser

from pathlib import Path

from ptzpresets import globals
from ptzpresets import statusbar
from ptzpresets import styles
from ptzpresets import presetpanel


class View(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master.title(globals.APP_TITLE)
        self.master.iconbitmap(styles.APP_ICON)
        self.presetpanels = dict()
        self.refreshbutton = None
        self.statusbar = None
        self.helpbutton = None
        self.body = None
        self.footer = None
        self.build_view()   # Will be empty.

    def build_view(self):
        self.create_body()
        self.create_footer()
        self.create_footer_widgets()
        self.position_frames()
        self.position_body_widgets()
        self.position_footer_widgets()
        self.pack()
        self.master.update_idletasks()

    def create_body(self):
        self.body = ttk.Frame(master=self)
        
    def create_presetpanel(self, camera_name, num_presets):
        panel = presetpanel.PresetPanel(master=self.body)
        panel.set_cameraname(camera_name)
        panel.create_presetbuttons(num_presets)
        self.presetpanels[camera_name] = panel
        self.refresh(silent=True)
        return panel        

    def create_footer(self):
        self.footer = ttk.Frame(master=self)
        
    def create_footer_widgets(self):
        refr_btn = ttk.Label(master=self.footer, text=chr(0x2B6E), # ⭮
                             background='white', style='Statusbar.TLabel', 
                             width=3)
        refr_btn.bind('<Button-1>', self.refresh)
        help_btn = ttk.Label(master=self.footer, text='?', background='white', 
                             style='Statusbar.TLabel', width=2)
        help_btn.bind('<Button-1>', self.show_help)
        self.refreshbutton = refr_btn
        self.statusbar = statusbar.Statusbar(master=self.footer)
        self.helpbutton = help_btn

    def position_frames(self):
        self.body.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)
        self.footer.pack(expand=tk.NO, fill=tk.X, side=tk.BOTTOM, pady=(10,0))
        
    def position_body_widgets(self):
        for panel in self.presetpanels.values():
            panel.pack(side=tk.LEFT, anchor=tk.NW)

    def position_footer_widgets(self):
        self.refreshbutton.grid(row=0, column=0)
        self.statusbar.master.columnconfigure(1, weight=1)  # Stretch statusbar only 
        self.statusbar.grid(row=0, column=1, sticky=tk.E+tk.W)
        self.helpbutton.grid(row=0, column=2)
        
    def register_quit_callback(self, callback):
        """Register a callback function that is called before
        the view is destroyed.
        """
        root = self.winfo_toplevel()
        if root.master:
            root = root.master
            # https://mail.python.org/pipermail/python-list/2000-April/045376.html
        def wrapper():
            try:
                callback()
            except Exception as error:
                tkinter.messagebox.showerror(title='Error', message=str(error))
            root.destroy()
        root.protocol('WM_DELETE_WINDOW', wrapper)

    def refresh(self, event=None, silent=False):
        if not silent:
            self.show_status('Reloading presets...')
        for panel in self.presetpanels.values():
            panel.refresh()
        self.position_body_widgets()
        if not silent:
            self.show_status('')

    def show_status(self, message):
        self.statusbar.inform(message)

    def show_help(self, event):
        webbrowser.open_new(globals.HELP_FILE)
        
    