"""
    View class that defines splash screen.
"""

import time
import tkinter as tk
import tkinter.ttk as ttk

from ptzpresets import globals
from ptzpresets import statusbar
from ptzpresets import styles


class Splashscreen(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.overrideredirect(True)
        self.body = None
        self.footer = None
        self.statusbar = None
        self.build_view()
        self.master.eval(f'tk::PlaceWindow {str(self)} center')
        # https://stackoverflow.com/a/10018670/12646289
        
    def build_view(self):
        self.body = self.create_body()
        self.footer = self.create_footer()
        self.position_frames()
        
    def create_body(self):
        body = ttk.Frame(master=self)
        img = ttk.Label(master=body, image=styles.SPLASH_SCREEN, 
                        text=globals.CREDITS_LINE, compound=tk.TOP,
                        style='Splashscreen.CreditsLine.TLabel')
        img.pack()
        return body
        
    def create_footer(self):
        footer =  ttk.Frame(master=self)
        stbar = statusbar.Statusbar(master=footer)
        stbar.config(style='Splashscreen.Statusbar.TLabel', 
                     background=styles.SPLASHSCREEN_STATUSBAR_BACKGROUND)
        stbar.pack(expand=tk.YES, fill=tk.X, side=tk.LEFT)
        self.statusbar = stbar
        return footer
    
    def position_frames(self):
        self.body.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)
        self.footer.pack(expand=tk.NO, fill=tk.X, side=tk.BOTTOM)
        
    def show_info(self, message):
        self.statusbar.inform(message)
        time.sleep(0.5)
        self.update_idletasks()

        
        
        