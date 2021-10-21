import sys

from cx_Freeze import setup, Executable


VERSION = 2.0#input(f"{'*'*100}\nVersion: ")

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [], 
    'excludes': [], 
    'include_files': [
        ('static', 'static'),
        ('venv/Lib/site-packages/wsdl', 'onvif/wsdl'),
        ('config_template.json', 'config.json'),
        ('README.html', 'README.html'),
        ('Release Notes.html', 'Release Notes.html')
    ]
}

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable(
        'ptzpresets.pyw', 
        base=base,
        shortcut_name='PTZ Presets',
        icon='static/ptzpresets.ico'
        )
]

setup(name='ptzpresets',
      version = VERSION,
      description = 'A simple presets switchboard for PTZ cameras',
      options = {'build_exe': build_options},
      executables = executables)
