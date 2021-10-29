#coding: utf-8

import json

from functools import partial
from pathlib import Path

from ptzpresets import globals
from ptzpresets import model
from ptzpresets import splashscreen
from ptzpresets import view


class Controller:
    """Controller class that ties the application model to the view.
    """
    
    def __init__(self, config, master=None):
        self.master = master
        self.view = None
        self.buttons_presets = dict()

        self.splashscreen = splashscreen.Splashscreen(master)
        self.splashscreen.show_info('Starting PTZ presets...')
        self.splashscreen.show_info('Loading model...')
        self.model = model.Model(config)
        self.model.status.register_observer(self.status_observer)
        self.model.init_model()
        self.splashscreen.show_info('Initializing main screen...')
        self.splashscreen.destroy()

        self.build_main_view()
        self.master.deiconify()

    def status_observer(self):
        state = self.model.status.value
        event = state['event']
        camera = state['camera']
        token = state['preset_token']
        name = state['preset_name']
        if event == 'error':
            if state['error_message'] == 'camera_creation_error':
                message = (f'{camera}: Could not connect to camera. '
                           f'Continuing without it...')
            else:
                message = f'{camera}: Unknown error...'
        elif event == 'new':
            message = f'{camera}: Adding new preset {name} ({token})'
        elif event == 'save':
            message = f'{camera}: Saving current position to {name} ({token})'
        elif event == 'rename':
            message = f'{camera}: Renamed to {name} ({token})'
        elif event == 'goto':
            message = f'{camera}: Going to {name} ({token})'
        elif event == 'delete':
            message = f'{camera}: Deleting {name} ({token})...'
        elif event == 'commit_renames':
            message = f'{camera}: Committing all unsaved renames...'
        if self.view is not None:
            self.view.statusbar.inform(message)
        else:
            self.splashscreen.show_info(message)
        
    def build_main_view(self):
        """Build the application's main view. Create a preset 
        buttons panel for each camera and register the button 
        callback handlers.
        """
        v = view.View(self.master)
        for camera_key, presets in self.model.presets.items():
            panel = v.create_presetpanel(camera_name=camera_key, 
                                         num_presets=len(presets))
            buttons_presets = self.attach_buttons_to_presets(camera_key, panel)
            for button, preset in buttons_presets:
                button.rename(preset.name)
                button.register_callback(
                    partial(self.presetbutton_callback, camera_key=camera_key, 
                            preset=preset, panel=panel)
                )
            panel.register_addbutton_observer(
                partial(self.addbutton_observer, camera_key=camera_key, 
                        panel=panel)
            )
            self.buttons_presets[camera_key] = buttons_presets
        v.refresh(silent=True)
        v.register_quit_callback(self.quit_callback)
        self.view = v
        
    def load_panel_layout(self):
        """Load the panel layout from a JSON file if it exists, 
        or else return a default layout that is determined by
        the preset order in the camera.
        """
        layout = dict()
        if globals.PANEL_LAYOUT_FILE.exists():
            with open(globals.PANEL_LAYOUT_FILE, 'rt', encoding='utf8') as f:
                layout = json.load(f)
        else:   # Default layout
            for ckey, presets in self.model.presets.items():
                layout[ckey] = list(presets.keys())
        return layout
    
    def save_panel_layout(self):
        """Save panel layout to a JSON file, which is structured 
        as follows:
            {"camkey": ["token", ...], ...}
        """
        layout = dict()
        for ckey, panel in self.view.presetpanels.items():
            layout[ckey] = [self.get_preset_by_button(ckey, b).token 
                            for b in panel.presetbuttons]
        with open(globals.PANEL_LAYOUT_FILE, 'wt', encoding='utf8') as f:
            json.dump(layout, f, indent=4)
    
    def attach_buttons_to_presets(self, camera_key, panel):
        """Return a list of tuples of button-preset pairs ordered
        according to the layout file.
        """
        layout = self.load_panel_layout()
        presets = self.model.presets[camera_key]
        if camera_key in layout:
            # camera_key does not have to be present in layout file
            # (e.g. in case a new camera was added).
            presets_ordered = [presets[t] for t in layout[camera_key]]
        else:
            presets_ordered = presets.values()
        return [*zip(panel.presetbuttons, presets_ordered)]
    
    def get_preset_by_button(self, camera_key, button):
        """Return the preset attached to a button.
        """
        # https://stackoverflow.com/a/18114565
        d = dict(self.buttons_presets[camera_key])      
        return d[button] 

    def presetbutton_callback(self, event, preset, panel, camera_key):
        """Callback function that is attached to each preset button.
        """
        button = event.widget
        state = event.state_decoded
        
        # CapsLock state should be ignored.
        state = state.replace('CapsLock-', '')
        
        if event.type.name == 'ButtonRelease':
            # ButtonRelease can be triggered by a click as well as by
            # a drag and drop acction (button reordering). 
            # In the latter case it should be ignored.
            if not panel.is_widgets_reordered:
                if state == '<ButtonRelease-Button-1>':
                    preset.goto()
                    panel.set_current_button(button)
                elif state == '<Shift-ButtonRelease-Button-1>':
                    preset.save()
                    panel.set_current_button(button)
                elif state == '<Control-ButtonRelease-Button-1>':
                    new_name = button.rename(new_name=None)
                    preset.rename(new_name)
                elif state == '<Alt-ButtonRelease-Button-1>':
                    panel.delete_presetbutton(button)
                    self.buttons_presets[camera_key].remove((button, preset))
                    preset.delete()
            else:
                self.save_panel_layout()
                panel.is_widgets_reordered = False
            
    def addbutton_observer(self, button, camera_key, panel):
        """Observer function for the add button. Create a new preset 
        and a button and connect them to each other.
        """
        token = self.model.add_preset(camera_key, button.rename)
        preset = self.model.get_preset(camera_key, token)
        button.register_callback(
            partial(self.presetbutton_callback, camera_key=camera_key, 
                    preset=preset, panel=panel)
        )
        self.buttons_presets[camera_key].append((button, preset))
        panel.refresh()
        panel.set_current_button(button)
        
    def quit_callback(self):
        """Callback function that is called before the application 
        is shut down. 
        """
        self.model.commit_uncommitted_renames()
        self.save_panel_layout()
                
