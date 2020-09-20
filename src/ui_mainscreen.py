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

import re

import devices
import utilities
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
btnBottomBar4 = Button(devices.TouchPanel, 59)
btnBottomBar5 = Button(devices.TouchPanel, 60)
btnBottomBar6 = Button(devices.TouchPanel, 99)
btnBottomBar3 = Button(devices.TouchPanel, 110)

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
        execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_1_function', default_value=None), button)

    elif button is btnQuickButton2:
        execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_2_function', default_value=None), button)

    elif button is btnQuickButton3:
        execute_command(utilities.config.get_value(
            'interface/quickbuttons/button_3_function', default_value=None), button)

    elif button is btnQuickButton4:
        execute_command(utilities.config.get_value(
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
        devices.carbonite.Set('Auto', None)
        DebugPrint('interface/TransitionButtons', 'MIX Button pressed', 'Debug')

    elif button is btnCUT:
        devices.carbonite.Set('Cut', None)
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

    devices.carbonite.Set('MLEPresetSource', PresetSource[button])
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

    devices.carbonite.Set('KeySource', AUXSource[button], {'Keyer': 1})


# end function (AUXButtonsPressed)


@event([btnPreview_Key1, btnPreview_Key2], 'Pressed')
def KeyButtonsPressed(button, state):
    if button is btnPreview_Key1:
        devices.carbonite.Set('KeyOnPreview', 'Toggle', {'Keyer': 1})

    elif button is btnPreview_Key2:
        devices.carbonite.Set('KeyOnPreview', 'Toggle', {'Keyer': 2})

@event([btnCloseNoButtonsA, btnCloseNoButtonsB], 'Pressed')
def btnCloseButtonsPressed(button, state):
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')





##################################################################################
# FIXME - move this (the scripting and macro stuff) into its own file/class
def execute_command(macro_string, button = None):

    #    device:<object>:<command>:<value>
    #    ui:popup:<name>
    #    macro:<name>
    regex_ui = re.compile(r"^(ui:popup):(.*?)$")
    regex_device = re.compile(r"^(device):(.*?):(.*?):(.*?):(.*?)(?::(int|str):(.*?)){0,1}$")
    regex_preset = re.compile(r"^(preset):(.*)$")

    #ui:popup:POP - CAM1 - Control
    if regex_ui.match(macro_string):
        p = regex_ui.match(macro_string)
        if p.group(2):
            devices.TouchPanel.ShowPopup(p.group(2))
        else:
            DebugPrint('execute_button_macro/regex_ui', 'Attempted to handle a malformed command statement: [{}]'.format(macro_string),
                       'Error')

    #device:carbonite:Cut:None:None
    #device:carbonite:KeyOnPreview:On:Keyer:int:1
    elif regex_device.match(macro_string):
        p = regex_device.match(macro_string)
        if p.group(4):

            try:
                driver_object = devices.device_objects[p.group(2)]
                driver_command = p.group(3)

                if p.group(4).lower() == 'none':
                    driver_value = None

                else:
                    driver_value = p.group(4)


                if p.group(5) and p.group(5).lower() != 'none':
                    if p.group(6) and p.group(7):
                        if p.group(6) == 'int':
                            qualifier = {p.group(5): int(p.group(7))}

                        elif p.group(6) == 'str':
                            qualifier = {p.group(5): p.group(7)}

                else:
                        qualifier = None

                DebugPrint('interface.py/execute_command',
                           'Sending Device Driver Command: [{}] [{}] [{}]'.format(driver_command, driver_value, qualifier),
                           'Trace')

                # Run our driver_command
                driver_object.Set(driver_command, driver_value, qualifier)

            except:
                DebugPrint('execute_button_macro/regex_device',
                           'An error occurred sending a command to driver module. [{}]'.format(macro_string),
                           'Error')

        else:
            DebugPrint('execute_button_macro/regex_device', 'Attempted to handle a malformed command statement: [{}]'.format(macro_string),
                       'Error')

    elif regex_preset.match(macro_string):
        p = regex_preset.match(macro_string)
        DebugPrint('execute_button_macro/preset', 'We are loading macro #[{}] [{}]'.
                   format(p.group(2), macro_string))

        execute_preset(int(p.group(2)))

    else:
        if button is not None:
            DebugPrint('execute_button_macro', 'UNRECOGNIZED MACRO STRING! Button: [{}] Attempted to parse: [{}]'.
                       format(button.Name, macro_string), 'Error')

        else:
            DebugPrint('execute_button_macro', 'UNRECOGNIZED MACRO STRING! Attempted to parse: [{}]'.
                       format(macro_string), 'Error')

#end function (execute_button_macro)


def execute_preset(preset_number):
    if utilities.config.get_value('presets/preset_{}_enabled'.format(preset_number),
                                  default_value=False, cast_as='boolean') is True:

        preset_name = utilities.config.get_value('presets/preset_{}_name'.format(preset_number),
                                  default_value='Un-named', cast_as='string')

        DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                   'Preset starting execution..', 'Info')

        preset_index = 0
        while preset_index < 100:   # We don't want this loop to run away - 100 steps should be enough?
            preset_index += 1

            current_step_enabled = utilities.config.get_value(
                'presets/preset_{}_steps/{}_enabled'.format(preset_number, preset_index),
                default_value=False, cast_as='boolean')

            current_step_data = utilities.config.get_value(
                'presets/preset_{}_steps/{}_data'.format(preset_number, preset_index),
                default_value='None', cast_as='string')

            if ((current_step_enabled is False) and (current_step_data == 'None')):
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Step #{} is not present, so we are done. Execution completed!'.
                           format(preset_index), 'Info')

                break

            elif current_step_enabled is False:
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Skipping step #{} as it is disabled: [{}]'.
                           format(preset_index, current_step_data), 'Debug')
                continue

            # If we get here then we've got valid preset data, AND we're set as enabled. Let's execute!
            else:
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Execute step #{}'.format(preset_index), 'Debug')

                execute_command(current_step_data)

        #FIXME - we really should convert this to a system state
        lblNextPreset.SetText(preset_name)
#end function (execute_preset)



@event(btnBottomBar3, 'Pressed')
def btnBottomBar3Pressed(button, state):
    pass

@event(btnBottomBar4, 'Pressed')
def btnBottomBar4Pressed(button, state):
    devices.TouchPanel.ShowPage('No-Button View')

@event(btnBottomBar5, 'Pressed')
def btnBottomBar5Pressed(button, state):
    devices.TouchPanel.ShowPopup('POP - Options')

@event(btnBottomBar6, 'Pressed')
def btnBottomBar6Pressed(button, state):
    pass





#FIXME - this needs to become a system state (inside devices)
# DUPLICATED in interface.py
ActivePopup = None
def ShowPopup(PopupName):
    global ActivePopup
    devices.TouchPanel.ShowPopup(PopupName)
    ActivePopup = PopupName
    devices.system_states.Set('ActivePopup', PopupName)

#end function (ShowPopup)