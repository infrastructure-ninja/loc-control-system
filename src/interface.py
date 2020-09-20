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


# Main Menu Buttons
btnMainMenuR1C1 = Button(devices.TouchPanel, 1000)
btnMainMenuR2C1 = Button(devices.TouchPanel, 1001)
btnMainMenuR3C1 = Button(devices.TouchPanel, 1002)
btnMainMenuR4C1 = Button(devices.TouchPanel, 1003)

btnMainMenuR1C2 = Button(devices.TouchPanel, 1004)
btnMainMenuR2C2 = Button(devices.TouchPanel, 1005)
btnMainMenuR3C2 = Button(devices.TouchPanel, 1006)
btnMainMenuR4C2 = Button(devices.TouchPanel, 1007)

btnMainMenuR1C3 = Button(devices.TouchPanel, 1008)
btnMainMenuR2C3 = Button(devices.TouchPanel, 1009)
btnMainMenuR3C3 = Button(devices.TouchPanel, 1010)
btnMainMenuR4C3 = Button(devices.TouchPanel, 1011)

btnMainMenuR1C4 = Button(devices.TouchPanel, 1012)
btnMainMenuR2C4 = Button(devices.TouchPanel, 1013)
btnMainMenuR3C4 = Button(devices.TouchPanel, 1014)
btnMainMenuR4C4 = Button(devices.TouchPanel, 1015)

btnMainMenuR1C5 = Button(devices.TouchPanel, 1016)
btnMainMenuR2C5 = Button(devices.TouchPanel, 1017)
btnMainMenuR3C5 = Button(devices.TouchPanel, 1018)
btnMainMenuR4C5 = Button(devices.TouchPanel, 1019)
lstMainPopupButtons = [
                    btnMainMenuR1C1, btnMainMenuR2C1, btnMainMenuR3C1, btnMainMenuR4C1,
                    btnMainMenuR1C2, btnMainMenuR2C2, btnMainMenuR3C2, btnMainMenuR4C2,
                    btnMainMenuR1C3, btnMainMenuR2C3, btnMainMenuR3C3, btnMainMenuR4C3,
                    btnMainMenuR1C4, btnMainMenuR2C4, btnMainMenuR3C4, btnMainMenuR4C4,
                    btnMainMenuR1C5, btnMainMenuR2C5, btnMainMenuR3C5, btnMainMenuR4C5
                    ]

def initialize_all():
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Main Menu')
    devices.system_states.Set('ActivePopup', 'POP - Main Menu')

    # FIXME - we really should convert this to a system state
    mainscreen.lblNextPreset.SetText('n/a')

    # We want these things hidden until they are programmatically shown
    playback.lvlPlayback_ClipPosition.SetVisible(False)
    playback.lblPlaybackTimeCodeRemaining.SetVisible(False)

    cam1.btnCAM1_OnAir.SetVisible(False)
    cam1.btnCAM1_OnAir.SetEnable(False)

    cam2.btnCAM2_OnAir.SetVisible(False)
    cam2.btnCAM2_OnAir.SetEnable(False)

    playback.btnPlayback_OnAir.SetVisible(False)
    playback.btnPlayback_OnAir.SetEnable(False)

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

    # Hide the CAM3 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam3_is_enabled:
        # HIDE
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x87\x04\x00\x00\x00\x00') #MV Box3 Label (0xc87)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x00\x00') #MV Box3 Source (0xc84)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1a\x04\x00\x00\x00\x00') #MV Box3 Border (0x191a)

    else:
        # SHOW
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x87\x04\x00\x00\x00\x01') #MV Box3 Label (0xc87)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x03\xea') #MV Box3 Source (0xc84)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1a\x04\x00\x00\x00\x01') #MV Box3 Border (0x191a)

    cam4_is_enabled = utilities.config.get_value('devices/cam4/enabled', default_value=False, cast_as='boolean')
    for i in [mainscreen.btnCAM4_PTZ, mainscreen.btnCAM4_Preview, mainscreen.btnCAM4_AUX]:
        i.SetVisible(cam4_is_enabled)

    # Hide the CAM4 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam4_is_enabled:
        # HIDE
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8e\x04\x00\x00\x00\x00') #MV Box4 Label (0xc8e)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8b\x04\x00\x00\x00\x00') #MV Box4 Source (0xc8b)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1b\x04\x00\x00\x00\x00') #MV Box4 Border (0x191b)

    else:
        # SHOW
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8e\x04\x00\x00\x00\x01') #MV Box4 Label (0xc8e)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8b\x04\x00\x00\x03\xeb') #MV Box4 Source (0xc8b)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1b\x04\x00\x00\x00\x01') #MV Box4 Border (0x191b)

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




@event(lstMainPopupButtons, 'Pressed')
def MainMenuPopupButtonsPressed(button,state):
    DebugPrint('interface/MainMenuPopupButtonsPressed', 'Button was pressed: [{}]'.format(button.Name), 'Debug')

#                    btnMainMenuR1C1, btnMainMenuR2C1, btnMainMenuR3C1, btnMainMenuR4C1,
#                    btnMainMenuR1C2, btnMainMenuR2C2, btnMainMenuR3C2, btnMainMenuR4C2,
#                    btnMainMenuR1C3, btnMainMenuR2C3, btnMainMenuR3C3, btnMainMenuR4C3,
#                    btnMainMenuR1C4, btnMainMenuR2C4, btnMainMenuR3C4, btnMainMenuR4C4,
#                    btnMainMenuR1C5, btnMainMenuR2C5, btnMainMenuR3C5, btnMainMenuR4C5

    if button is btnMainMenuR4C5:
        DebugPrint('interface/MainMenuPopupButtonsPressed', 'Running a re-initialize', 'Info')
        utilities.config.reload()
        initialize_all()












