# coding: utf-8


import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

from pathlib import Path


# Instantiate style manager.
style = ttk.Style()

def system_font():
    """Return default font on the system. Use name system_font
    to avoid naming conflict with default font."""
    return tkfont.nametofont('TkDefaultFont')

def get_default_font_family():
    return system_font().actual()['family']

def get_character_width_pixels():
    """Get character width in pixels of default font."""
    return system_font().measure('0')
    # https://stackoverflow.com/a/30954325


DEFAULT_FONT = get_default_font_family()
CHAR_WIDTH_PX = get_character_width_pixels()

APP_DIR = Path.cwd()
STATIC_DIR = APP_DIR / 'static'

APP_ICON = STATIC_DIR / 'ptzpresets.ico'

BUTTON_ADD_PRESET_DEFAULT = tk.PhotoImage(file=(STATIC_DIR / 'button_add_preset_default.png'))
BUTTON_ADD_PRESET_HOVER = tk.PhotoImage(file=(STATIC_DIR / 'button_add_preset_hover.png'))


# ----- Styles ---------------------------------------------------------------

# Fonts

# Buttons
style.configure('PresetButton.TButton',
    anchor=tk.W,
    width=20,
    font=(DEFAULT_FONT, 9)
)

style.configure('Highlighted.PresetButton.TButton',
    font=(DEFAULT_FONT, 9, tkfont.BOLD),
    foreground='#6C2A44',
    width=17
)

# Labels
style.configure('Statusbar.TLabel',
    anchor=tk.W,
    font=(DEFAULT_FONT, 7)
)
