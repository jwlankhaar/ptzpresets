# coding utf-8

"""
    Classes that define constants.
"""

import tkinter.constants


class GuiEnum():
    """Class that imports and bundles all Tk constants."""
    def __init__(self):
        for const, value in tkinter.constants.__dict__.items():
            if not const.startswith('_') and type(value) in [str, int, float]:
                setattr(self, const, value)


