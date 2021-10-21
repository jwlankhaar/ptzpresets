#coding: utf-8

"""
    Wrapper class for the ONVIFCamera class.
"""


import onvif

from collections import ChainMap

from ptzpresets import errors


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
        self.profile_token = None
        self.preset_tokens = dict()
        self.preset_names = dict()
        self.uncommitted_names = dict()
        self.uncommitted_tokens = dict()
        
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
        self.preset_tokens = self.get_presettokens_byname()
        self.preset_names = self.get_presetnames_bytoken()

    def get_default_profile_token(self):
        profiles = self.media_service.GetProfiles()
        return profiles[0].token

    def get_presets(self):
        return self.ptz_service.GetPresets(self.profile_token)

    def list_preset_names(self):
        return self.get_presetnames_bytoken().values()

    def get_presetnames_bytoken(self):
        committed_names = {p['token']: p['Name'] for p in self.get_presets()}
        return ChainMap(self.uncommitted_names, committed_names)

    def get_presettokens_byname(self):
        committed_tokens = {p['Name']: p['token'] for p in self.get_presets()}
        return ChainMap(self.uncommitted_tokens, committed_tokens)

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
        goto_response = self.ptz_service.GotoPreset({
            'ProfileToken': self.profile_token, 
            'PresetToken': preset_token
        })
        # Commit rename, if needed.
        if preset_token in self.uncommitted_names:
            new_name = self.uncommitted_names[preset_token]
            self.set_preset(new_name, preset_token)
            del self.uncommitted_names[preset_token]
            del self.uncommitted_tokens[new_name]
        return goto_response

    def get_position(self):
        response = self.ptz_service.GetStatus({
            'ProfileToken': self.profile_token
        })
        return response['Position']

    def rename_preset(self, preset_token, new_name, force_commit=False):
        """Rename a preset by. Because the PTZ service does not 
        provide a separate rename function, a rename action requires
        the camera to move to the preset position and save it under
        the new name. In order to be able to rename presets without 
        moving the camera, the rename is deferred until the next 
        time the preset is chosen (unless force_commit=True). In the 
        meantime, the rename action is stored as an uncommitted 
        rename.
        """
        if force_commit:
            self.goto_preset(preset_token=preset_token)
            self.set_preset(preset_name=new_name, preset_token=preset_token)
        else:
            self.uncommitted_names[preset_token] = new_name
            self.uncommitted_tokens[new_name] = preset_token
        self.preset_names = self.get_presetnames_bytoken()  # Update preset names list.
        self.preset_tokens = self.get_presettokens_byname()

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
        
    def commit_all_presetrenames(self):
        """Commit all preset renames that have not been committed yet.
        """
        for token in list(self.uncommitted_names.keys()):
        # List forces a copy so that the dictionary can be changed 
        # during iteration.
            new_name = self.uncommitted_names.pop(token)
            del self.uncommitted_tokens[new_name]
            self.rename_preset(token, new_name, force_commit=True)
