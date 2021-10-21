# coding: utf-8


import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

from ptzpresets import globals
from ptzpresets import root


# Instantiate style manager.
style = ttk.Style(master=root.root)

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

APP_ICON = globals.STATIC_DIR / 'ptzpresets.ico'

SPLASH_SCREEN = tk.PhotoImage(file=(globals.STATIC_DIR / 'splash_screen.png'))

ADDPRESET_BUTTON_DEFAULT = tk.PhotoImage(
    file=(globals.STATIC_DIR / 'addpreset_button_default.png'))
ADDPRESET_BUTTON_HOVER = tk.PhotoImage(
    file=(globals.STATIC_DIR / 'addpreset_button_hover.png'))

# Cursor path should be prepended by @ (https://stackoverflow.com/a/66205274)
# and it seems to have to be a representation with forward slashes.
DRAGANDDROP_CURSOR = '@static/drag_and_drop_cursor.cur' 
DRAGANDDROP_SNAP_DISTANCE = 4

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

style.configure('Splashscreen.Statusbar.TLabel',
    anchor=tk.W,
    font=(DEFAULT_FONT, 7)
)

style.configure('Splashscreen.CreditsLine.TLabel',
    anchor = tk.W,
    font=(DEFAULT_FONT, 7),
    foreground='#4D4D4D')

SPLASHSCREEN_STATUSBAR_BACKGROUND = '#DEE1E6'
