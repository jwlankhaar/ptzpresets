"""
Global variables for the project.
"""

from pathlib import Path

from ptzpresets import utils


DEFAULT_CONFIG_FILE = 'config.json'

APP_TITLE = 'PTZ Presets'
APP_VERSION = '2.0'
APP_AUTHOR = 'Lankhaar'
APP_DIR = Path.cwd()
STATIC_DIR = APP_DIR / 'static'

CREDITS_LINE = f'{APP_TITLE} {APP_VERSION} by Jan-Willem Lankhaar, October 2021'
HELP_FILE = Path('static') / 'help.html'
USER_CONFIG_DIR = utils.get_user_config_dir()
PANEL_LAYOUT_FILE = USER_CONFIG_DIR / 'panel_layout.json'
