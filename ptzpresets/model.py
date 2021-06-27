#coding: utf-8

"""Model class that defines the application logic.
"""

import functools

import ptzpresets.camera as camera
import ptzpresets.errors as errors
import ptzpresets.observables as observables
import ptzpresets.preset as preset


class Model:
    #TODO: document
    def __init__(self, config):
        self.status = observables.ObservableValue('')
        self.cameras = self._create_cameras(config)
        self.camera_labels = self.cameras.keys()
        self.widget_event_handlers = dict()
        self.current_presets = observables.ObservableDict( 
            self._init_current_presets()
        )
        self.presets = self._create_presets()
        self._register_preset_observers()
        
    def _create_cameras(self, config):
        """Return a dictionary with a Camera object for each
        camera.
        """
        cameras = dict()
        for ckey, cfg in config.items():
            try: 
                cameras[ckey] = camera.Camera(cfg)
            except errors.CouldNotCreateCameraError:
                self._state(f'Could not connect to camera {ckey}, continuing without it.')
        return cameras

    def _create_presets(self):        
        """Return a dictionary with a Preset object for each
        preset of each camera.
        """     
        presets = dict()
        for ckey, cam in self.cameras.items():
            presets[ckey] = {
                t: preset.Preset(name=n, token=t, camera=cam)
                for t, n in cam.get_preset_names().items()
            }
        return presets

    def _init_current_presets(self):
        return {ckey: None for ckey in self.cameras.keys()}
    
    def _preset_observer(self, camera_key, token, event):
        """Observer function to be attached to a preset. Set the 
        model state message according to the observed event.
        """
        preset = self.presets[camera_key][token]
        name = preset.name
        token = preset.token
        if event == 'goto':
            self._state(f'{camera_key}: Going to {name} ({token})')
        elif event == 'save':
            self._state(f'{camera_key}: Current position saved as {name} ({token})')
        elif event == 'renamed':
            self._state(f'{camera_key}: Preset renamed to {name} ({token})')
        elif event == 'delete':
            self._state(f'{camera_key}: Preset {name} deleted ({token})')

    def _register_preset_observers(self):
        """Attach an observer function to each preset."""
        for presets in self.presets.values():
            for preset in presets:
                preset.register_observer(self._preset_observer)
            
    def _state(self, message):
        """Set the status message."""
        self.status.value = message
        
    def create_widget_event_handlers(self, func):
        """Create a widget event handler for each preset that is based
        on func, a function that should accept a preset as first
        argument.
        """
        for ckey, presets in self.presets.items():
            self.widget_event_handlers[ckey] = []
            for preset in presets:
                self.widget_event_handlers[ckey].append(
                    functools.partial(
                        func,
                        preset
                    )
                )

    def add_preset(self, camera_key, rename_func=None):
        """Save the current camera position as a new preset.
        If rename_func is specified, this callable is called
        to get a new name for the preset. Return the preset 
        token.
        """
        token = self.cameras[camera_key].set_preset()
        if rename_func:
            new_name = rename_func()
        else:
            new_name = self.cameras[camera_key].preset_names[token]
        self.presets[camera_key][token] = preset.Preset(
            name=new_name,
            token=token,
            camera=self.cameras[camera_key]
        )
        self.current_presets[camera_key] = token
        return token
        
    # def attach_widget(self, camera_key, token, widget):
    #     """Store the widget (an arbitrary object) that corresponds 
    #     to the preset in the preset. Note that the widget is only
    #     stored, the preset does not provide any behaviour on the
    #     widget.
    #     """
    #     self.presets[camera_key][token].widget = widget
        
    def register_status_observer(self, func):
        """Register a callable that observes changes to the status."""
        self.status.register_observer(func)
        
    # def register_preset_observer(self, camera_key, token, func):
    #     """Register a callable that observes changes to a preset."""
    #     self.presets[camera_key][token].register_observer(func)
    
    def register_currentpreset_observer(self, camera_key, func):
        """Register a callable that observes changes to the current
        preset pointer.
        """
        self.current_presets[camera_key].register_observer(func)

    def set_preset(self, camera_key, token):
        """Save the current position to the preset and adjust
        the current preset pointer.
        """
        self.presets[camera_key][token].save()
        self.current_presets[camera_key] = token

    def goto_preset(self, camera_key, token):
        """Move the camera to the preset position. Adjust the
        current preset pointer.
        """
        self.presets[camera_key][token].goto()
        self.current_presets[camera_key] = token

    def rename_preset(self, camera_key, token, new_name):
        """Rename a preset object. Because renaming will make 
        move the camera to the preset position, the current 
        present pointer must be adjusted as well.
        """
        self.cameras[camera_key].rename_preset(token, new_name)
        self.current_presets[camera_key] = token

    def delete_preset(self, camera_key, token):
        """Delete a preset object. Make sure the
        current preset pointer is adjusted accordingly.
        """
        del self.presets[camera_key][token]
        if self.current_presets[camera_key] == token:
            self.current_presets[camera_key] = None
            
    def detach_widget(self, camera_key, token):
        """Detach the widget object from a preset."""
        self.presets[camera_key][token].widget = None



    
