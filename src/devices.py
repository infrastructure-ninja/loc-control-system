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

from extronlib.device import ProcessorDevice, UIDevice

from helper_systemstate import DeviceClass

from utilities import DebugPrint
import utilities

ControlProcessor = ProcessorDevice('ExtronProcessor')
TouchPanel = UIDevice('ExtronPanel')

import interface


# This dictionary will store all of our device objects, so they can be accessed
# later via our "preset/macro" mechanism. Each device module we load below will be responsible
# to add itself to this dictionary.
device_objects = {}


import dev_cam1 as cam1
import dev_cam2 as cam2
import dev_cam3 as cam3
import dev_cam4 as cam4

import dev_switcher as switcher
import dev_matrix as matrix
import dev_playback as playback
import dev_soundboard as soundboard
import dev_recorder as recorder
import dev_midi as midi

# "system_states" is a custom driver module that provides a way to store various
# system states and trigger callbacks when they change.
system_states = DeviceClass()


def system_states_callback_handler(command, value, qualifier):
    if command == 'KeyOnPreview':
        DebugPrint('devices.py/system_states_callback_handler',
                   '[{}] [{}] [{}]'.format(command, value, qualifier), 'Trace')

        if qualifier['Keyer'] == 1:
            if value == 'On':
                interface.mainscreen.btnPreview_Key1.SetState(1)
                interface.mainscreen.btnPreview_Key1.SetBlinking('Fast', [0, 1])

            else:
                interface.mainscreen.btnPreview_Key1.SetState(0)

        elif qualifier['Keyer'] == 2:
            if value == 'On':
                interface.mainscreen.btnPreview_Key2.SetState(1)
                interface.mainscreen.btnPreview_Key2.SetBlinking('Fast', [0, 1])

            else:
                interface.mainscreen.btnPreview_Key2.SetState(0)

    # FIXME - this could be more compact and pythonic, when you get bored of everything else
    elif command == 'CameraSpeed' and qualifier['Camera Number'] == 1:
        button_map = {
            'Slow': interface.cam1.btnCAM1_Speed1,
            'Medium': interface.cam1.btnCAM1_Speed2,
            'Fast': interface.cam1.btnCAM1_Speed3
          }

        button_map[value].SetState(1)

        # Update states on all buttons than aren't the one we changed above
        for single_button in button_map.values():
            if single_button is not button_map[value]:
                single_button.SetState(0)


    elif command == 'CameraSpeed' and qualifier['Camera Number'] == 2:
        button_map = {
            'Slow': interface.cam2.btnCAM2_Speed1,
            'Medium': interface.cam2.btnCAM2_Speed2,
            'Fast': interface.cam2.btnCAM2_Speed3
          }

        button_map[value].SetState(1)

        # Update states on all buttons than aren't the one we changed above
        for single_button in button_map.values():
            if single_button is not button_map[value]:
                single_button.SetState(0)

    elif command == 'CameraSpeed' and qualifier['Camera Number'] == 3:
        button_map = {
            'Slow': interface.cam3.btnCam3_Speed1,
            'Medium': interface.cam3.btnCam3_Speed2,
            'Fast': interface.cam3.btnCam3_Speed3
          }

        button_map[value].SetState(1)

        # Update states on all buttons than aren't the one we changed above
        for single_button in button_map.values():
            if single_button is not button_map[value]:
                single_button.SetState(0)

    elif command == 'CameraSpeed' and qualifier['Camera Number'] == 4:
        button_map = {
            'Slow': interface.cam4.btnCam4_Speed1,
            'Medium': interface.cam4.btnCam4_Speed2,
            'Fast': interface.cam4.btnCam4_Speed3
          }

        button_map[value].SetState(1)

        # Update states on all buttons than aren't the one we changed above
        for single_button in button_map.values():
            if single_button is not button_map[value]:
                single_button.SetState(0)

# end function (system_states_callback_handler)


system_states.SubscribeStatus('ActivePopup', None, system_states_callback_handler)
system_states.SubscribeStatus('CameraSpeed', None, system_states_callback_handler)
system_states.SubscribeStatus('KeyOnPreview', None, system_states_callback_handler)


def initialize_all():
    DebugPrint('devices.py/initialize_all', 'Attempting to connect to Carbonite switcher..', 'Debug')
    switcher.carbonite.Connect()

    result = switcher.tally.StartListen()
    if result == 'Listening':
        DebugPrint('devices.py/initialize_all',
                   'TSL UMD Tally Driver is listening on {}/TCP..'.format(switcher.tally.IPPort), 'Info')

    else:
        DebugPrint('devices.py/initialize_all',
                   'TSL UMD Tally Driver is NOT LISTENING! Return status was: [{}]'.format(result), 'Error')

    DebugPrint('devices.py/initialize_all', 'Attempting to connect to DXP 88 HD matrix switcher..', 'Info')
    matrix.matrix.Connect()

    DebugPrint('devices.py/initialize_all', 'Attempting to connect to the SMD101 playback device..', 'Info')
    playback.smd101.Connect()

    DebugPrint('devices.py/initialize_all', 'Attempting to connect to the Yamaha TF5 audio console..', 'Info')
    soundboard.soundboard.Connect()

    #DebugPrint('devices.py/initialize_all', 'Attempting to connect to Camera #1 ..', 'Info')
    #cam1.cam1.Connect()

    #DebugPrint('devices.py/initialize_all', 'Attempting to connect to Camera #2 ..', 'Info')
    #cam2.cam2.Connect()

    # Set our system state for the starting camera movement speed
    system_states.Set('CameraSpeed',
                      utilities.config.get_value('devices/cam1/default_speed', default_value='Slow', cast_as='string'),
                      {'Camera Number': 1})

    system_states.Set('CameraSpeed',
                      utilities.config.get_value('devices/cam2/default_speed', default_value='Slow', cast_as='string'),
                      {'Camera Number': 2})

    system_states.Set('CameraSpeed',
                      utilities.config.get_value('devices/cam3/default_speed', default_value='Slow', cast_as='string'),
                      {'Camera Number': 3})

    system_states.Set('CameraSpeed',
                      utilities.config.get_value('devices/cam4/default_speed', default_value='Slow', cast_as='string'),
                      {'Camera Number': 4})
