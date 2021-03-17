#coding: utf-8

from ptzpresets.camera import Camera
from ptzpresets.utils import read_config

config = read_config('config_dev.json')

presets_L = [
    'Voorganger',
    'Tafel',
    'Tafel zoom',
    'Muziekgroep',
    'Middenschip',
    'Transept',
    'Orgel',
    'Doopvont',
    'Koper',
    'Kansel overzicht',
    'Zanger split',
    'Preset%2014',
    'Test',
    'Zangers'
]

presets_R = [
    'Kansel',
    'Tafel',
    'Tafel%20zoom',
    'Muziekgroep',
    'Middenschip',
    'Transept',
    'Orgel',
    'Middenschip',
    'Kansel overzicht',
    'Doopvont',
    'Preset%2011',
    'Muziekgroep',
    'Zanger transept',
    'Kaars',
    'Onze Vader',
    'Zangers'
]

camera_L = Camera(config=config['Camera L'])
camera_R = Camera(config=config['Camera R'])

for p in presets_L:
    camera_L.set_preset(p)

for p in presets_R:
    camera_R.set_preset(p)
