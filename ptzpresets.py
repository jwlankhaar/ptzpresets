#coding:utf-8

import ptzpresets.application
import ptzpresets.utils
import ptzpresets.styles


CONFIG_FILE = 'config.json'


if __name__ == '__main__':
    config = ptzpresets.utils.read_config(CONFIG_FILE)
    app = ptzpresets.application.Application(config=config)
    app.master.iconbitmap(ptzpresets.styles.APP_ICON)
    app.mainloop()
