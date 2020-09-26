# "LoC Audio/Visual Control System for Extron ControlScript"
# Copyright (C) 2020 Joel D. Caturia <jcaturia@katratech.com>
#
# "LoC Control" is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "LoC Control" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this code.  If not, see <https://www.gnu.org/licenses/>.

from extronlib import event
from extronlib.ui import Button

import devices
import utilities
from utilities import DebugPrint

import ui_mainscreen as mainscreen
import ui_playback as playback
import ui_cam1 as cam1
import ui_cam2 as cam2
import ui_cam3 as cam3
import ui_cam4 as cam4

import ui_presets as presets
import ui_mainmenu as mainmenu
import ui_options as options


def initialize_all():

    # FIXME - we really should convert this to a system state
    mainscreen.lblNextPreset.SetText('n/a')

    # We want these things hidden until they are programmatically shown
    cam1.btnCAM1_OnAir.SetVisible(False)
    cam1.btnCAM1_OnAir.SetEnable(False)
    cam1.btnCAM1_TallyLockout.SetVisible(False)
    cam1.lblCam1_PresetUpdatedNotice.SetVisible(False)

    cam2.btnCAM2_OnAir.SetVisible(False)
    cam2.btnCAM2_OnAir.SetEnable(False)
    cam2.btnCam2_TallyLockout.SetVisible(False)
    cam2.lblCam2_PresetUpdatedNotice.SetVisible(False)

    cam3.btnCam3_OnAir.SetVisible(False)
    cam3.btnCam3_OnAir.SetEnable(False)
    cam3.btnCam3_TallyLockout.SetVisible(False)
    cam3.lblCam3_PresetUpdatedNotice.SetVisible(False)

    cam4.btnCam4_OnAir.SetVisible(False)
    cam4.btnCam4_OnAir.SetEnable(False)
    cam4.btnCam4_TallyLockout.SetVisible(False)
    cam4.lblCam4_PresetUpdatedNotice.SetVisible(False)

    playback.btnPlayback_OnAir.SetVisible(False)
    playback.btnPlayback_OnAir.SetEnable(False)
    playback.btnPlayback_TallyPresetsLockout.SetVisible(False)
    playback.lvlPlayback_ClipPosition.SetVisible(False)
    playback.lblPlaybackTimeCodeRemaining.SetVisible(False)

    playback.lblPlayback_CurrentState.SetText('Playing [-00:00:02]')

    # Initialize a bunch of buttons using text pulled from our configuration file
    # This dictionary stores the button object we want to "SetText' on, and the configuration
    # path where we will be able to retrieve the name. The loop at the bottom makes it happen.
    init_button_name_dict = {
        playback.btnPlayback_Playlist1: 'devices/playback/playlist_1_name',
        playback.btnPlayback_Playlist2: 'devices/playback/playlist_2_name',
        playback.btnPlayback_Playlist3: 'devices/playback/playlist_3_name',
        playback.btnPlayback_Playlist4: 'devices/playback/playlist_4_name',
        playback.btnPlayback_Playlist5: 'devices/playback/playlist_5_name',
        playback.btnPlayback_Playlist6: 'devices/playback/playlist_6_name',

        cam1.btnCAM1_Preset1: 'devices/cam1/preset_1_name',
        cam1.btnCAM1_Preset2: 'devices/cam1/preset_2_name',
        cam1.btnCAM1_Preset3: 'devices/cam1/preset_3_name',
        cam1.btnCAM1_Preset4: 'devices/cam1/preset_4_name',
        cam1.btnCAM1_Preset5: 'devices/cam1/preset_5_name',
        cam1.btnCAM1_Preset6: 'devices/cam1/preset_6_name',
        cam1.btnCAM1_Preset7: 'devices/cam1/preset_7_name',
        cam1.btnCAM1_Preset8: 'devices/cam1/preset_8_name',

        cam2.btnCAM2_Preset1: 'devices/cam2/preset_1_name',
        cam2.btnCAM2_Preset2: 'devices/cam2/preset_2_name',
        cam2.btnCAM2_Preset3: 'devices/cam2/preset_3_name',
        cam2.btnCAM2_Preset4: 'devices/cam2/preset_4_name',
        cam2.btnCAM2_Preset5: 'devices/cam2/preset_5_name',
        cam2.btnCAM2_Preset6: 'devices/cam2/preset_6_name',
        cam2.btnCAM2_Preset7: 'devices/cam2/preset_7_name',
        cam2.btnCAM2_Preset8: 'devices/cam2/preset_8_name',

        cam3.btnCam3_Preset1: 'devices/cam3/preset_1_name',
        cam3.btnCam3_Preset2: 'devices/cam3/preset_2_name',
        cam3.btnCam3_Preset3: 'devices/cam3/preset_3_name',
        cam3.btnCam3_Preset4: 'devices/cam3/preset_4_name',
        cam3.btnCam3_Preset5: 'devices/cam3/preset_5_name',
        cam3.btnCam3_Preset6: 'devices/cam3/preset_6_name',
        cam3.btnCam3_Preset7: 'devices/cam3/preset_7_name',
        cam3.btnCam3_Preset8: 'devices/cam3/preset_8_name',

        cam4.btnCam4_Preset1: 'devices/cam4/preset_1_name',
        cam4.btnCam4_Preset2: 'devices/cam4/preset_2_name',
        cam4.btnCam4_Preset3: 'devices/cam4/preset_3_name',
        cam4.btnCam4_Preset4: 'devices/cam4/preset_4_name',
        cam4.btnCam4_Preset5: 'devices/cam4/preset_5_name',
        cam4.btnCam4_Preset6: 'devices/cam4/preset_6_name',
        cam4.btnCam4_Preset7: 'devices/cam4/preset_7_name',
        cam4.btnCam4_Preset8: 'devices/cam4/preset_8_name',

        mainscreen.btnQuickButton1: 'interface/quickbuttons/button_1_name',
        mainscreen.btnQuickButton2: 'interface/quickbuttons/button_2_name',
        mainscreen.btnQuickButton3: 'interface/quickbuttons/button_3_name',
        mainscreen.btnQuickButton4: 'interface/quickbuttons/button_4_name',
    }

    for button, config_key in init_button_name_dict.items():
        button.SetText(utilities.config.get_value(config_key, default_value='(unused)'))

    # Show/Hide our "quick sidebar buttons" based on whether they are enabled in the configuration or not
    init_button_visible_dict = {
        mainscreen.btnQuickButton1: 'interface/quickbuttons/button_1_enabled',
        mainscreen.btnQuickButton2: 'interface/quickbuttons/button_2_enabled',
        mainscreen.btnQuickButton3: 'interface/quickbuttons/button_3_enabled',
        mainscreen.btnQuickButton4: 'interface/quickbuttons/button_4_enabled'
    }

    for button, config_key in init_button_visible_dict.items():
        button.SetVisible(utilities.config.get_value(config_key, default_value=False, cast_as='boolean'))


    # Set our "quick sidebar buttons" color based on how they are defined in the configuration
    button_color_map = {'blue': 0, 'green': 2, 'red': 3, 'white': 4, 'yellow': 5, 'gray': 6, 'grey': 6}
    init_button_color_dict = {
        mainscreen.btnQuickButton1: 'interface/quickbuttons/button_1_color',
        mainscreen.btnQuickButton2: 'interface/quickbuttons/button_2_color',
        mainscreen.btnQuickButton3: 'interface/quickbuttons/button_3_color',
        mainscreen.btnQuickButton4: 'interface/quickbuttons/button_4_color'
    }

    for button, config_key in init_button_color_dict.items():
        button_color = utilities.config.get_value(config_key, default_value='blue', cast_as='string')

        if button_color not in button_color_map:
            DebugPrint('interface.py/initialize_all',
                       'Invalid color specified in config file: [{}]. Defaulting to blue!'.format(config_key),
                       'Warn')

            button_color = 'blue'

        button.SetState(button_color_map[button_color])


    # Show/Hide our Camera UI buttons based on whether the camera is disabled in the configuration
    cam1_is_enabled = utilities.config.get_value('devices/cam1/enabled', default_value=False, cast_as='boolean')
    for i in [mainscreen.btnCAM1_PTZ, mainscreen.btnCAM1_Preview, mainscreen.btnCAM1_AUX]:
        i.SetVisible(cam1_is_enabled)

    cam2_is_enabled = utilities.config.get_value('devices/cam2/enabled', default_value=False,cast_as='boolean')
    for i in [mainscreen.btnCAM2_PTZ, mainscreen.btnCAM2_Preview, mainscreen.btnCAM2_AUX]:
        i.SetVisible(cam2_is_enabled)

    cam3_is_enabled = utilities.config.get_value('devices/cam3/enabled', default_value=False, cast_as='boolean')
    for i in [mainscreen.btnCAM3_PTZ, mainscreen.btnCAM3_Preview, mainscreen.btnCAM3_AUX]:
        i.SetVisible(cam3_is_enabled)

    cam3_is_enabled = utilities.config.get_value('devices/cam3/enabled', default_value=False, cast_as='boolean')
    for i in [mainscreen.btnCAM3_PTZ, mainscreen.btnCAM3_Preview, mainscreen.btnCAM3_AUX]:
        i.SetVisible(cam3_is_enabled)

    cam4_is_enabled = utilities.config.get_value('devices/cam4/enabled', default_value=False, cast_as='boolean')
    for i in [mainscreen.btnCAM4_PTZ, mainscreen.btnCAM4_Preview, mainscreen.btnCAM4_AUX]:
        i.SetVisible(cam4_is_enabled)

    # Hide the CAM1 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam1_is_enabled:
        # HIDE
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x79\x04\x00\x00\x00\x00') #MV Box1 Label (0xc79)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x76\x04\x00\x00\x00\x00') #MV Box1 Source (0xc76)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x18\x04\x00\x00\x00\x00') #MV Box1 Border (0x1918)

    else:
        # SHOW
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x79\x04\x00\x00\x00\x01') #MV Box1 Label (0xc79)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x76\x04\x00\x00\x03\xe8') #MV Box1 Source (0xc76)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x18\x04\x00\x00\x00\x01') #MV Box1 Border (0x1918)

    # Hide the CAM2 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam2_is_enabled:
        # HIDE
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x80\x04\x00\x00\x00\x00') #MV Box2 Label (0xc80)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x00\x00') #MV Box2 Source (0xc84)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x19\x04\x00\x00\x00\x00') #MV Box2 Border (0x1919)

    else:
        # SHOW
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x80\x04\x00\x00\x00\x01') #MV Box2 Label (0xc80)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x03\xe9') #MV Box2 Source (0xc84)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x19\x04\x00\x00\x00\x01') #MV Box2 Border (0x1919)

    # Hide the CAM3 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam3_is_enabled:
        # HIDE
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x87\x04\x00\x00\x00\x00') #MV Box3 Label (0xc87)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x00\x00') #MV Box3 Source (0xc84)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1a\x04\x00\x00\x00\x00') #MV Box3 Border (0x191a)

    else:
        # SHOW
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x87\x04\x00\x00\x00\x01') #MV Box3 Label (0xc87)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x03\xea') #MV Box3 Source (0xc84)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1a\x04\x00\x00\x00\x01') #MV Box3 Border (0x191a)

    # Hide the CAM4 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam4_is_enabled:
        # HIDE
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8e\x04\x00\x00\x00\x00') #MV Box4 Label (0xc8e)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8b\x04\x00\x00\x00\x00') #MV Box4 Source (0xc8b)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1b\x04\x00\x00\x00\x00') #MV Box4 Border (0x191b)

    else:
        # SHOW
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8e\x04\x00\x00\x00\x01') #MV Box4 Label (0xc8e)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8b\x04\x00\x00\x03\xeb') #MV Box4 Source (0xc8b)
        devices.switcher.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1b\x04\x00\x00\x00\x01') #MV Box4 Border (0x191b)

    # PRESET INITIALIZATION
    for preset_id in range(1, 13):
        if utilities.config.get_value('presets/preset_{}_enabled'.
                                              format(preset_id), default_value=False, cast_as='boolean') is True:

            presets.lstPresetButtons[preset_id - 1].SetText(utilities.config.get_value('presets/preset_{}_name'.
                                              format(preset_id), default_value='Unnamed', cast_as='string'))

            presets.lstPresetButtons[preset_id - 1].SetEnable(True)
            presets.lstPresetButtons[preset_id - 1].SetVisible(True)

        else:
            presets.lstPresetButtons[preset_id - 1].SetVisible(False)

    # The last thing we do is to show our actual Main Page and the home popup.
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Main Menu')
    devices.system_states.Set('ActivePopup', 'POP - Main Menu')

#end function (Initialize)


#FIXME - this needs to become a system state (inside devices)
# DUPLICATED in ui_mainscreen.py
ActivePopup = None
def ShowPopup(PopupName):
    global ActivePopup
    devices.TouchPanel.ShowPopup(PopupName)
    ActivePopup = PopupName
    devices.system_states.Set('ActivePopup', PopupName)

#end function (ShowPopup)















