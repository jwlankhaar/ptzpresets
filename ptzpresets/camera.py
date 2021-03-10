#coding: utf-8

"""
    Wrapper class for the ONVIFCamera class.
"""

import onvif

class Camera:
    def __init__(self, config):
        self.name = config['cameraname']
        self.camera = onvif.ONVIFCamera(
            host=config['ip'],
            port=config['port'],
            wsdl_dir=config['wsdl_dir'],
            user=config['user'],
            passwd=config['password']
        )
        self.media_service = self.camera.create_media_service()
        self.ptz_service = self.camera.create_ptz_service()
        self.profile_token = self.get_default_profile_token()
        self.preset_tokens = self.get_preset_tokens()
        self.num_of_presets = len(self.preset_tokens)

    def get_default_profile_token(self):
        profiles = self.media_service.GetProfiles()
        return profiles[0].token

    def get_presets(self):
        return self.ptz_service.GetPresets(self.profile_token)

    def get_preset_names(self):
        return [p['Name'] for p in self.get_presets()]

    def get_preset_tokens(self):
        return {p['Name']: p['token'] for p in self.get_presets()}

    def set_preset(self, preset_name=None, preset_token=None):
        self.ptz_service.SetPreset(self.profile_token, preset_name, preset_token)

    def goto_preset(self, preset_name):
        preset_token = self.preset_tokens[preset_name]
        self.ptz_service.GotoPreset(
            {'ProfileToken': self.profile_token, 'PresetToken': preset_token}
        )
