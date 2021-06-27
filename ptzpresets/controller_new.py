#coding: utf-8

import ptzpresets.model as model
import ptzpresets.view as view

#create model
#create view
#init presets
#attach buttons to presets

class Controller:
    def __init__(self, config):
        self.model = model.Model(config)
        self.model.create_widget_event_handlers(self.preset_button_callback)
        
        # model maken: dan camera's en presets bekend
        # callbacks aanmaken voor presets (aan presets toevoegen)
        # view aanmaken (met model als arg)
        # register_status_observer
        
        
        # Waar zit mijn probleem? 
        #
        # Ik wil model en view echt gescheiden houden maar dat betekent
        # dat ik in de controler alsnog variabelen moet gaan aanmaken
        # zodat ik daar het model ga nabootsen. Of: ik moet het model
        # meegeven met de view, maar dan wordt de view afhankelijk van
        # het model. Daarmee schend ik volgens mij de principes.
        self.view = view.View(model=model)
        #register observers
        
    def preset_button_callback(self, preset, event):
        widget = event.widget
        state = event.state_decoded
                
        if state == '<Button-1>':
            preset.goto()
        elif state == '<Shift-Button-1>':
            preset.save()
        elif state == '<Control-Button-1>':
            new_name = widget.rename(new_name=None)
            preset.rename(new_name)
        elif state == '<Alt_L-Button-1>':
            preset.delete()
        
        
        # button = event.widget
        # state = event.state_decoded
        # preset_name = button.get_name()
        # camera = self.cameras[camera_key]
        # presets = self.presets[camera_key]
        # current_preset = self.current_presets[camera_key]
        # if state == '<Button-1>':
        #     camera.goto_preset(token)
        #     self._switch_highlight(camera_key, token)
        #     self.show_status(
        #         f'{camera_key}: Going to preset {preset_name} ({token})'
        #     )
        # elif state == '<Shift-Button-1>':
        #     camera.set_preset(preset_name, token)
        #     self._switch_highlight(camera_key, token)
        #     self.show_status(
        #         f'{camera_key}: Saving current position to preset {preset_name} ({token})'
        #     )
        # elif state == '<Control-Button-1>':
        #     old_name = button.get_name()
        #     new_name = button.rename()
        #     if new_name != old_name:
        #         camera.rename_preset(token, new_name)
        #         self._switch_highlight(camera_key, token)
        #         presets[token]['name'] = new_name
        #         self.show_status(
        #             f'{camera_key}: Renaming preset to {new_name} ({token})'
        #         )
        # elif state == '<Alt_L-Button-1>':
        #     camera.delete_preset(token)
        #     presets.pop(token)
        #     if current_preset == token:
        #         self.current_presets[camera_key] = None
        #     self.refresh_gui()
        #     self.show_status(
        #         f'{camera_key}: Preset {preset_name} ({token}) deleted'
        #     )
    
    def add_button_handler(self):
        pass
    
    def status_observer(self):
        pass
    
    def current_preset_observer(self):
        pass