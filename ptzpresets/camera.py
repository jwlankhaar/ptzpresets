#coding: utf-8

"""
    Wrapper class for the ONVIFCamera class.
"""

import onvif

import ptzpresets.errors as errors


class Camera:
    """Camera class that wraps and eases the ONVIFCamera class.

    Attributes
    ----------
    media_service: <ONVIFCamera media service>
        Service neccessary to set and get a media profile token.
    ptz_service: <ONVIFCamera PTZ service>
        The PTZ service to which most functionality of the class
        is tied.
    config: dictionary
        Host, port, user credentials and other configuration info
        needed to connect to the camera.
    profile_token: string
        The media profile token needed to use most of the camera's 
        functionality.
    preset_tokens: dictionary
        Tokens of the presets by preset name.
    preset_names: dictionary
        Names of the presets by token.

    Methods
    -------
    get_default_profile_token(): string
        Get the first media profile token defined in the
        media service of the camera.
    get_presets(): list
        Get all presets defined in the default media profile.
        This includes the PTZ position details.
    list_preset_names(): list
        Return a list of the preset names.
    get_preset_names(): dictionary
        Return a dictionary of preset names by token.
    get_preset_tokens(): dictionary
        Return a dictionary of preset tokens by name.
    refresh(): None
        Re-initialize tokens and presets.
    set_preset(name=None, token=None): string
        Save the current camera position as a PTZ preset. Overwrite
        the current position if token is not None. Return the preset 
        token.
    goto_preset(token): <GotoPresetResponse>
        Move the camera to the preset position.
    get_position(token): dictionary
        Get the camera position of a preset.
    rename_preset(token, name):
        Rename a preset by going to it and setting a new with
        a new name. Because the PTZ service does not provide a separate 
        rename function the camera is first moved to the preset so 
        that the new name will not be attached to the wrong position.
    delete_preset(token):
        Delete a preset.
    find_preset_by_position(position, ignore_space=True)
        Return the preset token that matches the current PTZ position. 
        Return None if no preset matches the current settings.
    """
    def __init__(self, config):
        self._create_camera(config)
        self.media_service = self.camera.create_media_service()
        self.ptz_service = self.camera.create_ptz_service()
        self.init_tokens_and_presets()

    def _create_camera(self, config):
        self.name = config['cameraname']
        try:
            self.camera = onvif.ONVIFCamera(
                host=config['ip'],
                port=config['port'],
                wsdl_dir=config['wsdl_dir'],
                user=config['user'],
                passwd=config['password']
            )
        except:
            raise errors.CouldNotCreateCameraError

    def init_tokens_and_presets(self):
        self.profile_token = self.get_default_profile_token()
        self.preset_tokens = self.get_preset_tokens()
        self.preset_names = self.get_preset_names()

    def get_default_profile_token(self):
        profiles = self.media_service.GetProfiles()
        return profiles[0].token

    def get_presets(self):
        return self.ptz_service.GetPresets(self.profile_token)

    def list_preset_names(self):
        return [p['Name'] for p in self.get_presets()]

    def get_preset_names(self):
        return {p['token']: p['Name'] for p in self.get_presets()}

    def get_preset_tokens(self):
        return {p['Name']: p['token'] for p in self.get_presets()}

    def refresh(self):
        self.init_tokens_and_presets()

    def set_preset(self, preset_name=None, preset_token=None):
        response = self.ptz_service.SetPreset({
            'ProfileToken': self.profile_token, 
            'PresetToken': preset_token,
            'PresetName': preset_name
        })
        self.refresh()
        return response

    def goto_preset(self, preset_token):
        return self.ptz_service.GotoPreset({
            'ProfileToken': self.profile_token, 
            'PresetToken': preset_token
        })

    def get_position(self):
        response = self.ptz_service.GetStatus({
            'ProfileToken': self.profile_token
        })
        return response['Position']

    def rename_preset(self, preset_token, new_name):
        """Rename a preset by going to it and setting a new with
        a new name. Because the PTZ service does not provide a separate 
        rename function the camera is first moved to the preset so 
        that the new name will not be attached to the wrong position.
        """
        self.goto_preset(preset_token=preset_token)  #TODO: find a workaround that does not require goto
        self.set_preset(preset_name=new_name, preset_token=preset_token)
        self.preset_names = self.get_preset_names()  # Update preset names list.

    def delete_preset(self, preset_token):
        return self.ptz_service.RemovePreset({
            'ProfileToken': self.profile_token,
            'PresetToken': preset_token
        })

    def find_preset_by_position(self, position, ignore_space=True):
        """Return the preset token that matches the current PTZ position. 
        Return None if no preset matches the current settings.
        """
        pos = dict(position)   # Force a copy by value
        if ignore_space:
            del pos['PanTilt']['space']
            del pos['Zoom']['space']
        for p in self.get_presets():
            pre_pos = dict(p['PTZPosition'])
            if ignore_space:
                del pre_pos['PanTilt']['space']
                del pre_pos['Zoom']['space']
            if pre_pos == pos:
                return p['token']
        return None
        #TODO: implement
