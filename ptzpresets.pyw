#coding:utf-8

import ptzpresets.application
import ptzpresets.utils


CONFIG_FILE = 'config_dev.json'


if __name__ == '__main__':
    config = ptzpresets.utils.read_config(CONFIG_FILE)
    app = ptzpresets.application.Application(title='PTZ presets', config=config)
    app.mainloop()
