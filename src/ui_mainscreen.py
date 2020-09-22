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
from extronlib.ui import Button, Label

import devices
import utilities
import presets
from utilities import DebugPrint


# The background button
btnBackground = Button(devices.TouchPanel, 9)

# The "Next Preset" label
lblNextPreset = Label(devices.TouchPanel, 109)

# MENU and QuickButtons
btnMainMenu = Button(devices.TouchPanel, 16)
btnQuickButton1 = Button(devices.TouchPanel, 111)
btnQuickButton2 = Button(devices.TouchPanel, 205)
btnQuickButton3 = Button(devices.TouchPanel, 206)
btnQuickButton4 = Button(devices.TouchPanel, 207)
lstMainMenuButtons = [btnMainMenu, btnQuickButton1, btnQuickButton2, btnQuickButton3, btnQuickButton4]

btnCAM1_PTZ = Button(devices.TouchPanel, 1)
btnCAM2_PTZ = Button(devices.TouchPanel, 2)
btnCAM3_PTZ = Button(devices.TouchPanel, 43)
btnCAM4_PTZ = Button(devices.TouchPanel, 46)
lstPTZButtons = [btnCAM1_PTZ, btnCAM2_PTZ, btnCAM3_PTZ, btnCAM4_PTZ]


btnCAM1_Preview = Button(devices.TouchPanel, 33)
btnCAM2_Preview = Button(devices.TouchPanel, 3)
btnCAM3_Preview = Button(devices.TouchPanel, 41)
btnCAM4_Preview = Button(devices.TouchPanel, 42)
btnIN5_Preview  = Button(devices.TouchPanel, 100)
btnIN6_Preview  = Button(devices.TouchPanel, 107)
lstPreviewButtons = [btnCAM1_Preview, btnCAM2_Preview, btnCAM3_Preview,
                     btnCAM4_Preview, btnIN5_Preview, btnIN6_Preview]


btnCAM1_AUX = Button(devices.TouchPanel, 98)
btnCAM2_AUX = Button(devices.TouchPanel, 101)
btnCAM3_AUX = Button(devices.TouchPanel, 102)
btnCAM4_AUX = Button(devices.TouchPanel, 103)
btnIN5_AUX  = Button(devices.TouchPanel, 104)
lstAuxButtons = [btnCAM1_AUX, btnCAM2_AUX, btnCAM3_AUX, btnCAM4_AUX, btnIN5_AUX]

btnCUT = Button(devices.TouchPanel, 5)
btnMIX = Button(devices.TouchPanel, 52)

btnPlaybackControls = Button(devices.TouchPanel, 47)

btnPreview_Key1 = Button(devices.TouchPanel, 108)
btnPreview_Key2 = Button(devices.TouchPanel, 182)

btnCloseNoButtonsA = Button(devices.TouchPanel, 11)
btnCloseNoButtonsB = Button(devices.TouchPanel, 115)

@event(btnBackground, 'Pressed')
def BackgroundButtonPressed(button, state):
    button.SetEnable(False)
#end function (BackgroundButtonPressed)


@event(lstMainMenuButtons, 'Pressed')
def main_screen_buttons_pressed(button, state):
    DebugPrint('interface.py/main_screen_buttons_pressed', 'Main Screen Button Pressed: [{}]'.format(button.Name), 'Debug')

    if button is btnMainMenu:
        devices.TouchPanel.ShowPopup('POP - Main Menu')
        devices.system_states.Set('ActivePopup', 'POP - Main Menu')

    elif button is btnQuickButton1:
        presets.execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_1_function', default_value=None), button)

    elif button is btnQuickButton2:
        presets.execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_2_function', default_value=None), button)

    elif button is btnQuickButton3:
        presets.execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_3_function', default_value=None), button)

    elif button is btnQuickButton4:
        presets.execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_4_function', default_value=None), button)

#end function (main_screen_buttons_pressed)

@event(btnPlaybackControls, 'Pressed')
@event(lstPTZButtons, 'Pressed')
def PTZButtonsPressed(button, state):
    PopupMap = {
        btnCAM1_PTZ        : 'POP - CAM1-Control',
        btnCAM2_PTZ        : 'POP - CAM2-Control',
        btnCAM3_PTZ        : 'POP - CAM3-Control',
        btnCAM4_PTZ        : 'POP - CAM4-Control',
        btnPlaybackControls: 'POP - Playback Control'
    }
    DebugPrint('interface/PTZButtonsPressed', 'Button [{}] pressed. Loading popup: [{}]'.
               format(button.Name, PopupMap[button]), 'Debug')

    ShowPopup(PopupMap[button])


# end function (PTZButtonsPressed)


@event([btnMIX, btnCUT], 'Pressed')
def TransitionButtons(button, state):
    if button is btnMIX:
        devices.switcher.carbonite.Set('Auto', None)
        DebugPrint('interface/TransitionButtons', 'MIX Button pressed', 'Debug')

    elif button is btnCUT:
        devices.switcher.carbonite.Set('Cut', None)
        DebugPrint('interface/TransitionButtons', 'CUT Button pressed', 'Debug')

# end function (TransitionButtons)


@event(lstPreviewButtons, 'Pressed')
def PreviewButtonsPressed(button, state):
    PresetSource = {
        btnCAM1_Preview: 'Cam 1',
        btnCAM2_Preview: 'Cam 2',
        btnCAM3_Preview: 'Cam 3',
        btnCAM4_Preview: 'Cam 4',
        btnIN5_Preview : 'HDMI 1',
        btnIN6_Preview : 'HDMI 2'
    }

    devices.switcher.carbonite.Set('MLEPresetSource', PresetSource[button])
    DebugPrint('interface/PreviewButtonsPressed', 'Preset button pressed for input: [{}]'.
               format(PresetSource[button]), 'Debug')

# end function (PreviewButtonsPressed)


@event(lstAuxButtons, 'Pressed')
def AUXButtonsPressed(button, state):
    AUXSource = {
        btnCAM1_AUX: 'Cam 1',
        btnCAM2_AUX: 'Cam 2',
        btnCAM3_AUX: 'Cam 3',
        btnCAM4_AUX: 'Cam 4',
        btnIN5_AUX : 'HDMI 1',
    }

    devices.switcher.carbonite.Set('KeySource', AUXSource[button], {'Keyer': 1})

# end function (AUXButtonsPressed)


@event([btnPreview_Key1, btnPreview_Key2], 'Pressed')
def KeyButtonsPressed(button, state):
    if button is btnPreview_Key1:
        devices.switcher.carbonite.Set('KeyOnPreview', 'Toggle', {'Keyer': 1})

    elif button is btnPreview_Key2:
        devices.switcher.carbonite.Set('KeyOnPreview', 'Toggle', {'Keyer': 2})


@event([btnCloseNoButtonsA, btnCloseNoButtonsB], 'Pressed')
def btnCloseButtonsPressed(button, state):
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')


##################################################################################




#FIXME - this needs to become a system state (inside devices)
# DUPLICATED in interface.py
ActivePopup = None
def ShowPopup(PopupName):
    global ActivePopup
    devices.TouchPanel.ShowPopup(PopupName)
    ActivePopup = PopupName
    devices.system_states.Set('ActivePopup', PopupName)

#end function (ShowPopup)