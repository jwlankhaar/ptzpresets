from onvif import ONVIFCamera

mycam = ONVIFCamera('192.168.2.23', 10000, '' , '', 'venv/Lib/site-packages/wsdl')

# print(mycam.devicemgmt.GetHostname())
# print(mycam.devicemgmt.GetCapabilities())
ptz_service = mycam.create_ptz_service()
media_service = mycam.create_media_service()
profiles = media_service.GetProfiles()
profile_token = profiles[0].token
ptz_service.SetPreset(profile_token, 'presetname1')
ptz_service.SetPreset(profile_token, 'presetname2')
ptz_service.SetPreset(profile_token, 'presetname3')
for p in ptz_service.GetPresets(profile_token):
    print(p)
