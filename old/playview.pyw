
import functools

from ptzpresets import view_new as view


def callback(event):
    print('Button was pressed')
    

view = view.View()
view.create_presetpanel('Camera L', 5)
view.create_presetpanel('Camera R', 6)
view.presetpanels[0].set_presetbutton_names(['Knop1', 'Kansel', 'Orgel'], [0, 1, 2])
view.presetpanels[0].presetbuttons[0].register_callback(callback)
view.refresh()
view.show_status('Wordt vervolgd...')
view.mainloop()