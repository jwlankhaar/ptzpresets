

import ptzpresets.utils as utils
import ptzpresets.camera as camera


cfg = utils.read_config('config_dev.json')
cam = camera.Camera(cfg['Camera L'])
presets = cam.get_presets()
voorganger_token = cam.preset_tokens['Voorganger']
transept_token = cam.preset_tokens['Transept']
cam.goto_preset(transept_token)
status = cam.ptz_service.GetStatus(cam.profile_token)
pass
