#coding: utf-8

"""Controller class that defines and controls the PTZ Presets logic.
"""


import ptzpresets.camera as camera
import ptzpresets.errors as errors


class Controller:
    """Controller class that defines and controls the PTZ Presets logic.

    Attributes
    ----------
    config: dictionary
        Camera configurations.
    cameras: dictionary
        Holds a dictionary for each camera with the actual
        camera object (Camera class) and the presets.
    refresh_gui_func: callable
        A callable that refreshes the GUI.
    show_status_func: callable
        A callable that displays the status messages in the GUI.
    status: string
        Representation of the current status of the application.
    
    Methods
    -------
    get_preset_names(camera_key)
        Return a list of names of the presets of a camera.
    add_buttons_to_presets(camera_key, buttons)
        Tie the GUI preset buttons to the presets of a camera.
    process_preset_click(event, camera_key, token)
        Callback for the GUI preset buttons of a camera.
    add_preset(event, camera_key)
        Callback for the Add preset button of a camera.
    """
    def __init__(self, config=None, refresh_gui_func=None, show_status_func=None):
        self.cameras = self._create_cameras(config)
        self.presets = self._get_presets()
        self.current_presets = self._init_current_presets()
        self.refresh_gui = refresh_gui_func
        self.show_status = show_status_func

    def _create_cameras(self, config):
        cameras = dict()
        for ckey, cfg in config.items():
            try: 
                cameras[ckey] = camera.Camera(cfg)
            except errors.CouldNotCreateCameraError:
                self.show_status(
                    f'Error creating camera {ckey}, continuing without it'
                )
        return cameras

    def _get_presets(self):
        presets = dict()
        for ckey, cam in self.cameras.items():
            presets[ckey] = {
                token: {'name': name, 'button': None} 
                for token, name in cam.get_preset_names().items()
            }
        return presets

    def _init_current_presets(self):
        return {ckey: None for ckey in self.cameras.keys()}

    def add_buttons_to_presets(self, camera_key, buttons):
        presets = self.presets[camera_key]
        for token, button in zip(presets, buttons):
            presets[token]['button'] = button

    def process_preset_click(self, event, camera_key, token):
        button = event.widget
        state = event.state_decoded
        preset_name = button.get_name()
        camera = self.cameras[camera_key]
        presets = self.presets[camera_key]
        current_preset = self.current_presets[camera_key]
        if state == '<Button-1>':
            camera.goto_preset(token)
            self._switch_highlight(camera_key, token)
            self.show_status(
                f'{camera_key}: Going to preset {preset_name} ({token})'
            )
        elif state == '<Shift-Button-1>':
            camera.set_preset(preset_name, token)
            self._switch_highlight(camera_key, token)
            self.show_status(
                f'{camera_key}: Saving current position to preset {preset_name} ({token})'
            )
        elif state == '<Control-Button-1>':
            old_name = button.get_name()
            new_name = button.rename()
            if new_name != old_name:
                camera.rename_preset(token, new_name)
                self._switch_highlight(camera_key, token)
                presets[token]['name'] = new_name
                self.show_status(
                    f'{camera_key}: Renaming preset to {new_name} ({token})'
                )
        elif state == '<Alt_L-Button-1>':
            camera.delete_preset(token)
            presets.pop(token)
            if current_preset == token:
                self.current_presets[camera_key] = None
            self.refresh_gui()
            self.show_status(
                f'{camera_key}: Preset {preset_name} ({token}) deleted'
            )
        
    def add_preset(self, event, camera_key):
        camera = self.cameras[camera_key]
        token = camera.set_preset()
        preset_name = camera.preset_names[token]
        self.presets[camera_key][token] = {'name': preset_name}
        self.current_presets[camera_key] = token
        self._refresh()
        new_name = self.presets[camera_key][token]['button'].rename()
        self.presets[camera_key][token]['button'].highlight()
        self.presets[camera_key][token]['name'] = new_name
        self.show_status(
            f'{camera_key}: Preset {new_name} ({token}) added'
        )

    def _refresh(self):
        for ckey in self.cameras.keys():
            self.cameras[ckey].refresh()
        self.presets = self._get_presets()
        self.refresh_gui()

    def _switch_highlight(self, camera_key, token_to_highlight):
        current_preset = self.current_presets[camera_key]
        if self.current_presets[camera_key]:
            self.presets[camera_key][current_preset]['button'].playdown()
        self.presets[camera_key][token_to_highlight]['button'].highlight()
        self.current_presets[camera_key] = token_to_highlight

