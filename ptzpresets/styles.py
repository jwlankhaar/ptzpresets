# coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font



def get_default_font_family():
    root = tk.Tk()
    default_font = tkinter.font.nametofont('TkDefaultFont')
    font_family = default_font.actual()['family']
    root.destroy()
    return font_family


# Character width: https://stackoverflow.com/a/30954325
def get_character_width_pixels():
    root = tk.Tk()
    default_font = tkinter.font.nametofont('TkDefaultFont')
    width_pixels = default_font.measure('0')
    root.destroy()
    return width_pixels

DEFAULT_FONT = get_default_font_family()
CHAR_WIDTH_PX = get_character_width_pixels()

stl_btn_fixed_width_small_text_left = ttk.Style()
stl_btn_fixed_width_small_text_left.configure(
    'ButtonFixedWidthSmallTextLeft.TButton',
    anchor=tk.W,
    width=20,
    font=(DEFAULT_FONT, 8)
)
