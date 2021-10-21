# coding: utf-8

"""
    Utility classes and functions.
"""

import appdirs
import tkinter as tk
import json

from pathlib import Path

from ptzpresets import globals


def read_config(config_file):
    """Read the JSON configuration file. Turn it into a dictionary
    with the camera name as key and the camera's configuration as value.
    """
    with open(config_file, 'r') as f:
        return {c['cameraname']: c for c in json.load(f)}

def get_user_config_dir():
    """Return the correct user configuration directory path. Create
    the directory if it does not exist.
    """
    dir = Path(appdirs.user_config_dir(globals.APP_TITLE, globals.APP_AUTHOR))
    if not dir.exists():
        dir.mkdir(parents=True)
    return dir
    
    


    
    
