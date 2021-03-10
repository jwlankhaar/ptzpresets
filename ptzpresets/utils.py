# coding: utf-8

"""
    Utility classes and functions.
"""

import json

def read_config(config_file):
    """Read the JSON configuration file. Turn it into a dictionary
    with the camera name as key and the camera's configuration as value.
    """
    with open(config_file, 'r') as f:
        return {c['cameraname']: c for c in json.load(f)}
    


