# coding: utf-8

"""
    PresetPanel class that holds the widgets
    belonging to a camera.
"""

import tkinter as tk
import tkinter.ttk as ttk

from ptzpresets import multibutton
from ptzpresets import styles
from ptzpresets import dragandrop


class PresetPanel(ttk.Frame, dragandrop.DragAndDropMixin):
    """Class containing preset buttons and additional widgets for a 
    single camera.
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.cameralabel = None
        self.presetbuttons = []
        self.addbutton = None
        self.addbutton_observer = None
        self.highlighted_button = None

        self.create_generalwidgets()
        self.position_widgets()
        
        self.dnd_register_master_refresh_callback(self.refresh)
                
    def create_generalwidgets(self):
        """Create the general widgets for the camera."""
        self.cameralabel = self._create_cameralabel()
        self.addbutton = self._create_addbutton()

    def create_presetbuttons(self, num_presets):
        """Create the preset button widgets, register a callback for 
        each and initialize the drag and drop functionality.
        """
        num_offset = len(self.presetbuttons)
        buttons = []
        for i in range(num_presets):
            button = multibutton.MultiButton(
                master=self, text='Preset', 
                number=None, #num_offset+i+1, 
                default_style='PresetButton.TButton',
                highlight_style='Highlighted.PresetButton.TButton',
                callback=None
            )
            self.dnd_register_callbacks(button)
            buttons.append(button)
        self.presetbuttons.extend(buttons)
        self.dnd_init(master=self, widgets=self.presetbuttons)
        self.refresh()
        return buttons
    
    def _create_cameralabel(self):
        return ttk.Label(master=self, text='', style='TLabel')

    def _create_addbutton(self):
        """Create a button for adding a preset to the panel and 
        configure its behavior.
        """
        img_default = styles.ADDPRESET_BUTTON_DEFAULT
        img_hover = styles.ADDPRESET_BUTTON_HOVER
        btn = ttk.Label(master=self, image=img_default)
        btn.bind('<Enter>', lambda e, i=img_hover: e.widget.config(image=i))
        btn.bind('<Leave>', lambda e, i=img_default: e.widget.config(image=i))
        btn.bind('<Button-1>', lambda e, f=self._addbutton_callback: f())
        return btn    
    
    def _addbutton_callback(self):
        """Callback for the add preset button. Create a button and
        run the observer function that is registered (if any) to 
        process the add button event in the model.
        """
        button = self.create_presetbuttons(1)[0]
        if self.addbutton_observer is not None:
            self.addbutton_observer(button)

    def register_addbutton_observer(self, function):
        """Register an observer function that is called when a new 
        preset button is added to the panel.
        """
        self.addbutton_observer = function
    
    def set_cameraname(self, camera_name):
        self.cameralabel['text'] = camera_name
        
    def position_widgets(self):
        self.cameralabel.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=1)
        for btn in self.presetbuttons:
            btn.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=1)
        self.addbutton.pack(side=tk.TOP, expand=True)
        if len(self.presetbuttons) > 0:
            self.dnd_init(master=self, widgets=self.presetbuttons)
    
    def delete_presetbutton(self, button):
        """Remove a preset button from the panel.
        """
        self.presetbuttons.remove(button)
        if self.highlighted_button is button:
            self.unset_current_button()
        button.destroy()
    
    def refresh(self):
        """Rebuild the preset panel and reposition its widgets.
        """
        for widget in self.winfo_children():
            widget.forget()
        self.position_widgets()
        
    def set_current_button(self, button):
        """Set button as the current button and highlight it.
        """
        if self.highlighted_button is None:
            self.highlighted_button = button
        elif self.highlighted_button.is_highlighted:
            self.highlighted_button.playdown()
        button.highlight()
        self.highlighted_button = button

    def unset_current_button(self):
        """Unset the highlighted button.
        """
        if self.highlighted_button is not None:
            if self.highlighted_button.is_highlighted:
                self.highlighted_button.playdown()
            self.highlighted_button = None