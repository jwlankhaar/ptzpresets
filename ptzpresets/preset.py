#coding: utf-8

"""PTZ Preset class
"""


class Preset:    
    #TODO: document
    def __init__(self, name=None, token=None, camera=None):
        self.name = name
        self.token = token
        self.camera = camera
        self.observers = []

    def save(self):
        """Save current position as the new preset position."""
        self.camera.set_preset(self.name, self.token)
        self._trigger_observers(event='save')

    def rename(self, new_name):
        """Rename the preset."""
        self.camera.rename_preset(self.token, new_name)
        self._trigger_observers(event='rename')
        
    def goto(self):
        """Go to the preset position."""
        self.camera.goto_preset(self.token)
        self._trigger_observers(event='goto')
        
    def register_observer(self, func):
        """Register an observer function that is notified 
        on changes in the preset.
        """
        self.observers.append(func)

    def _trigger_observers(self, event):
        """Call the observer functions."""
        for func in self.observers:
            func(self.camera.camera_key, self.token, event)

    def __del__(self):
        """Delete the preset."""
        self._trigger_observers(event='delete')
        super().__del__()

    def __repr__(self):
        return f"Preset(token={self.token}, name={self.name}, camera_key = {self.camera.name})"
