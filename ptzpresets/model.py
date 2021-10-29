#coding: utf-8

"""Model class that defines the application logic.
"""

from ptzpresets import camera
from ptzpresets import errors
from ptzpresets import observables
from ptzpresets import preset


class Model:
    """Class that defines the data model and business logic.
    
    Properties
    ----------
    status
        An observable value that reflects the model state.
    cameras
        Dictionary of ptzpresets.Camera objects.
    camera_labels
        The camera names (also used as (dictionary) keys
        to identify the cameras).
    presets
        Dictionary with a list of ptzpresets.Preset objects
        for each preset position defined in the camera.
    
    Methods
    -------
    init_model()
        Initialize the model. To be able to observe the initialization, 
        a status observer should be registered befor init_model is 
        called.
    add_preset(camera_key, rename_func)
        Add a preset object for the given camera. rename_func is a 
        callback function that will be called in order to as far a new 
        preset name.
    get_preset(camera_key, token)
        Return the ptzpresets.Preset object for the given token and 
        camera_key.
    commit_uncommitted_renames()
        Make all rename actions that have not been committed yet firm.
    """
    def __init__(self, config):
        """
        Parameters
        ----------
        config : dict()
            A configuration dictionary with a key for each camera.
        """
        self.status = observables.ObservableValue(None)
        self.config = config
        self.cameras = None
        self.camera_labels = None
        self.presets = None
        
    def init_model(self):        
        """Initialize the model based on config. To be able 
        to observe the initialization a status observer
        should be registered first.
        """
        self.cameras = self._create_cameras(self.config) 
        self.camera_labels = self.cameras.keys()
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
                self._update_state(event='error', camera_key=ckey, 
                                   error_message='camera_creation_error')
        return cameras

    def _create_presets(self):        
        """Return a dictionary with a Preset object for each
        preset of each camera.
        """     
        presets = dict()
        for ckey, cam in self.cameras.items():
            presets[ckey] = {
                t: preset.Preset(name=n, token=t, camera=cam)
                for t, n in cam.preset_names.items()
            }
        return presets

    def _preset_observer(self, event, preset):
        """Observer function that observes preset events."""
        camera_key = preset.camera.name
        name = preset.name
        token = preset.token
        self._update_state(event, camera_key, token, name)        
                
    def _register_preset_observers(self):
        """Attach an observer to each preset. The observer 
        should accept an event as argument.
        """
        for cam in self.cameras.keys():
            for preset in self.presets[cam].values():
                preset.register_observer(self._preset_observer)

    def _update_state(self, event=None, camera_key=None, preset_token=None, 
                     preset_name=None, error_message=None):
        """Change the status."""
        self.status.value = {
            'event' : event,
            'camera' : camera_key,
            'preset_token' : preset_token,
            'preset_name' : preset_name,
            'error_message' : error_message
        }
        
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
        self._update_state(event='new', camera_key=camera_key, 
                           preset_token=token, preset_name=new_name)
        return token
        
    def get_preset(self, camera_key, token):
        """Return a preset for the given token."""
        return self.presets[camera_key][token]
    
    def commit_uncommitted_renames(self):
        """Commit all preset rename actions on all cameras that have
        not been committed.
        """
        for cam in self.cameras.values():
            cam.commit_all_presetrenames()
            
