#coding: utf-8

import requests

USER = 'Gebruiker'
PASSW = 'Beamen2019%23'
CAMERA_CONFIG = {
    'CAML': {'IP': '192.168.2.4'},
    'CAMR': {'IP': '192.168.2.5'}
}
PRESET_URL_TEMPLATE = r'http://{user}:{password}@{camera_ip}/cgi-bin/ptz.cgi?action=start&channel=0&code=GotoPreset&arg1=0&arg2={preset_num}&arg3=0&arg4=0'

def render_url(url_template, camera_ip, preset_num):
    return PRESET_URL_TEMPLATE.format(**{
        'user': USER, 
        'camera_ip': camera_ip,
        'password': PASSW, 
        'preset_num': preset_num
    })


def set_preset(camera, preset_num):
    ip = CAMERA_CONFIG[camera]['IP']
    url = render_url(PRESET_URL_TEMPLATE, ip, preset_num)
    requests.post(url)
    print(f'requesting url: {url}')

