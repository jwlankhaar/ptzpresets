#coding: utf-8

"""
PTZ Preset class, a thin wrapper around camera functionality.
"""


class Preset:    
    """
    Wrapper class for preset-related camera functionality, 
    mainly meant to make camera functionality observable.
    
    Arguments
    
    Properties
    ----------
    name
        The name of the preset.
    token
        The token of the preset that uniquely identifies the preset
        in the camera.
    camera
        The camera object the preset belongs to.
    observers
        A list of observer functions that is triggered on each camera
        action.
        
    Methods
    -------
    save()
        Save current position as the new preset position.
    rename(new_name)
        Rename the preset.
    goto()
        Move the camera to the preset position.
    delete()
        Delete the preset.
    register_observer(func)
        Register an observer function that is notified on 
        changes.
    """
    
    def __init__(self, name=None, token=None, camera=None):
        """
        Parameters
        ----------
            name : str
                The name of the preset.
            token : str
                The preset token that uniquely identifies the preset
                in the camera.
            camera : ptzpresets.Camera
                The camera object to which the preset belongs.
        """
        self.name = name
        self.token = token
        self.camera = camera
        self.observers = []

    def save(self):
        """Save current position as the new preset position.
        """
        self.camera.set_preset(self.name, self.token)
        self._trigger_observers(event='save')

    def rename(self, new_name):
        """Rename the preset to new_name."""
        self.camera.rename_preset(self.token, new_name)
        self.name = new_name
        self._trigger_observers(event='rename')
        
    def goto(self):
        """Move the camera to the preset position."""
        self.camera.goto_preset(self.token)
        self._trigger_observers(event='goto')
        
    def delete(self):
        """Delete the preset position."""
        self.camera.delete_preset(self.token)
        self._trigger_observers(event='delete')
        
    def register_observer(self, func):
        """Register an observer function that is notified 
        on changes in the preset. The function should accept 
        the parameters event and preset.
        """
        self.observers.append(func)

    def _trigger_observers(self, event):
        """Call the observer functions. Pass the event and 
        the current preset instance to the observer functions.
        """
        for func in self.observers:
            func(event, self)

    def __repr__(self):
        return (f'Preset(token={self.token}, name={self.name}, '
                f'camera_key = {self.camera.name})')
