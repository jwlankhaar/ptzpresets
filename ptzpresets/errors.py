#coding: utf-8

"""Exception classes for PTZ Presets.

"""


class Error(Exception):
    """Base class for PTZ Preset exceptions."""
    pass

class CouldNotCreateCameraError(Error):
    """Raised when a Camera could not be created
    for a given camera configuration.
    """
    pass