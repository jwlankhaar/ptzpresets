
from ptzpresets import controller
from ptzpresets import root
from ptzpresets import utils


config_file = 'config_dev.json'
config = utils.read_config(config_file)
ctrl = controller.Controller(config, master=root.root)
ctrl.view.mainloop() 