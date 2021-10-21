#coding:utf-8

import argparse

from ptzpresets import controller
from ptzpresets import globals
from ptzpresets import root
from ptzpresets import utils


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--config', '-c',
        dest='config_file',
        help=('A configuration file, other than the default '
              'config.json in the current directory.'),
        default=globals.DEFAULT_CONFIG_FILE
    )
    args = argparser.parse_args()
    config = utils.read_config(args.config_file)
    ctrl = controller.Controller(config, master=root.root)
    ctrl.view.mainloop() 
