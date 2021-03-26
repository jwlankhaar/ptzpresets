# coding: utf-8

from ptzpresets.camera import Camera
from ptzpresets.utils import read_config

config = read_config('config_dev.json')

camera_L = Camera(config=config['Camera L'])

preset_token = 'PRESET_24763028'

camera_L.rename_preset(preset_token=preset_token, new_name='Test')
# camera_L.set_preset('Test close-up')