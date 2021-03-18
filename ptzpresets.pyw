#coding:utf-8

import argparse

import ptzpresets.application as application
import ptzpresets.utils as utils


DEFAULT_CONFIG_FILE = 'config.json'


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--config', '-c',
        dest='config_file',
        help='A configuration file, other than the default config.json in the current directory.',
        default=DEFAULT_CONFIG_FILE
    )
    args = argparser.parse_args()
    config = utils.read_config(args.config_file)

    app = application.Application(config=config)
    app.mainloop()
