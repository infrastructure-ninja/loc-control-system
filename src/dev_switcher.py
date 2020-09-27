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

from utilities import DummyDriver
from utilities import DebugPrint
import utilities

from helper_connectionhandler import GetConnectionHandler

import interface
import devices

################################################
# Ross Video Carbonite Black Solo Frame 109
################################################

if utilities.config.get_value('devices/switcher/enabled', default_value=False, cast_as='boolean'):
    import driver_ross_carboniteblacksolo_v1_0_0 as CarboniteSolo109

    carbonite = GetConnectionHandler(
        CarboniteSolo109.EthernetClass(
            utilities.config.get_value('devices/switcher/ipaddress'),
            utilities.config.get_value('devices/switcher/port', default_value=5253, cast_as='integer'),
            Model='Carbonite Black Solo 109'), 'ProductName')

    if utilities.config.get_value('devices/switcher/tally_enabled', default_value=False, cast_as='boolean'):
        import driver_tslumd_31 as TallyDriver

        tally = TallyDriver.EthernetClass(
            utilities.config.get_value('devices/switcher/tally_port', default_value=5728, cast_as='integer')
        )

    else:
        tally = DummyDriver('TSL UMD Tally Device')


else:
    carbonite = DummyDriver('Carbonite Black Solo 109')
    tally = DummyDriver('TSL UMD Tally Device')

devices.device_objects.update({'carbonite': carbonite})
devices.device_objects.update({'tally': tally})


def carbonite_received_data_handler(command, value, qualifier):
    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/carbonite_received_data_handler', 'Carbonite has been successfully connected',
                       'Info')

            for update in lstCarboniteStatusSubscriptions:
                if update == 'ConnectionStatus':  # ConnectionStatus does not support Updates
                    continue

                DebugPrint('devices.py/carbonite_received_data_handler',
                           'Updating status for command: [{}]'.format(update), 'Trace')

                carbonite.Update(update)

        elif value == 'Disconnected':
            DebugPrint('devices.py/carbonite_received_data_handler',
                       'Carbonite has been disconnected from the system. Will attempt reconnection..', 'Error')

    elif command == 'MLEPresetSource':
        DebugPrint('devices.py/carbonite_received_data_handler',
                   'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

        mle_preset_source_map = {
            'Cam 1': interface.mainscreen.btnCAM1_Preview, 'Cam 2': interface.mainscreen.btnCAM2_Preview,
            'Cam 3': interface.mainscreen.btnCAM3_Preview, 'Cam 4': interface.mainscreen.btnCAM4_Preview,
            'HDMI 1': interface.mainscreen.btnIN5_Preview, 'HDMI 2': interface.mainscreen.btnIN6_Preview
        }

        # Set all buttons to normal state, except the one we just set to its "selected" state
        # Be careful, as we can get a whole bunch of other values from this callback, so make sure it's one we expect
        if value in mle_preset_source_map:
            mle_preset_source_map[value].SetState(2)

        for input_name, button in mle_preset_source_map.items():
            if button is not mle_preset_source_map[value]:
                button.SetState(0)

    elif (command == 'KeySource') and qualifier['Keyer'] == 1:
        DebugPrint('devices.py/carbonite_received_data_handler',
                   'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

        keyer1_source_map = {
            'Cam 1': interface.mainscreen.btnCAM1_AUX, 'Cam 2': interface.mainscreen.btnCAM2_AUX,
            'Cam 3': interface.mainscreen.btnCAM3_AUX, 'Cam 4': interface.mainscreen.btnCAM4_AUX,
            'HDMI 1': interface.mainscreen.btnIN5_AUX
        }

        # Set all "AUX" buttons to normal state, except the one we just set to its "selected" state
        for input_name, button in keyer1_source_map.items():
            if button is not keyer1_source_map[value]:
                button.SetState(0)

    elif command == 'NextTransitionLayers':
        DebugPrint('devices.py/carbonite_received_data_handler',
                   'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

        carbonite.Update('KeyOnPreview')

    elif command == 'KeyerStatus':
        DebugPrint('devices.py/carbonite_received_data_handler',
                   'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

        carbonite.Update('KeyOnPreview')

    # Set our "Key 1" and "Key 2" buttons to show what keys are active for the next transition
    # We use blinking (SetBlinking) to make sure they're noticeable on the screen.
    elif command == 'KeyOnPreview':
        DebugPrint('devices.py/carbonite_received_data_handler',
                   'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

        keyer_button = {1: interface.mainscreen.btnPreview_Key1,
                        2: interface.mainscreen.btnPreview_Key2}[qualifier['Keyer']]

        if value == 'On':
            keyer_button.SetState(1)
            keyer_button.SetBlinking('Fast', [0, 1])

        else:
            keyer_button.SetState(0)

    else:
        DebugPrint('devices.py/carbonite_received_data_handler', 'Unhandled Carbonite Driver Data: [{0}] [{1}] [{2}]'.
                   format(command, value, qualifier), 'Trace')


# end function (carbonite_received_data_handler)


def tally_received_data_handler(command, value, qualifier):
    DebugPrint('devices.py/tally_received_data_handler', 'Tally Data Received: -> [{}] [{}] [{}]'.format(
        command, value, qualifier), 'Trace')

    if qualifier['Input'] == 'Cam 1':

        if (value == 'Off') or (value == 'Green'):
            devices.cam1.cam1.Set('Tally', 'Off')

            interface.cam1.btnCAM1_OnAir.SetState(0)
            interface.cam1.btnCAM1_OnAir.SetVisible(False)
            interface.cam1.btnCAM1_TallyLockout.SetVisible(False)

        elif (value == 'Red') or (value == 'Red & Green'):
            devices.cam1.cam1.Set('Tally', 'On')

            interface.cam1.btnCAM1_OnAir.SetBlinking('Fast', [0, 1])
            interface.cam1.btnCAM1_OnAir.SetVisible(True)
            interface.cam1.btnCAM1_TallyLockout.SetVisible(True)

    elif qualifier['Input'] == 'Cam 2':

        if (value == 'Off') or (value == 'Green'):
            devices.cam2.cam2.Set('Tally', 'Off')

            interface.cam2.btnCAM2_OnAir.SetState(0)
            interface.cam2.btnCAM2_OnAir.SetVisible(False)
            interface.cam2.btnCam2_TallyLockout.SetVisible(False)

        elif (value == 'Red') or (value == 'Red & Green'):
            devices.cam2.cam2.Set('Tally', 'On')

            interface.cam2.btnCAM2_OnAir.SetBlinking('Fast', [0, 1])
            interface.cam2.btnCAM2_OnAir.SetVisible(True)
            interface.cam2.btnCam2_TallyLockout.SetVisible(True)

    elif qualifier['Input'] == 'Cam 3':

        if (value == 'Off') or (value == 'Green'):
            devices.cam3.cam3.Set('Tally', 'Off')

            interface.cam3.btnCam3_OnAir.SetState(0)
            interface.cam3.btnCam3_OnAir.SetVisible(False)
            interface.cam3.btnCam3_TallyLockout.SetVisible(False)

        elif (value == 'Red') or (value == 'Red & Green'):
            devices.cam3.cam3.Set('Tally', 'On')

            interface.cam3.btnCam3_OnAir.SetBlinking('Fast', [0, 1])
            interface.cam3.btnCam3_OnAir.SetVisible(True)
            interface.cam3.btnCam3_TallyLockout.SetVisible(True)

    elif qualifier['Input'] == 'Cam 4':

        if (value == 'Off') or (value == 'Green'):
            devices.cam4.cam4.Set('Tally', 'Off')

            interface.cam4.btnCam4_OnAir.SetState(0)
            interface.cam4.btnCam4_OnAir.SetVisible(False)
            interface.cam4.btnCam4_TallyLockout.SetVisible(False)

        elif (value == 'Red') or (value == 'Red & Green'):
            devices.cam4.cam4.Set('Tally', 'On')

            interface.cam4.btnCam4_OnAir.SetBlinking('Fast', [0, 1])
            interface.cam4.btnCam4_OnAir.SetVisible(True)
            interface.cam4.btnCam4_TallyLockout.SetVisible(True)

    if qualifier['Input'] == 'HDMI 2':
        if (value == 'Off') or (value == 'Green'):
            interface.playback.btnPlayback_OnAir.SetState(0)
            interface.playback.btnPlayback_OnAir.SetVisible(False)
            interface.playback.btnPlayback_TallyTransportLockout.SetVisible(False)

        elif (value == 'Red') or (value == 'Red & Green'):
            interface.playback.btnPlayback_OnAir.SetBlinking('Fast', [0, 1])
            interface.playback.btnPlayback_OnAir.SetVisible(True)
            interface.playback.btnPlayback_TallyTransportLockout.SetVisible(True)

# end function (tally_received_data_handler)


lstCarboniteStatusSubscriptions = ['ConnectionStatus', 'MLEBackgroundSource', 'MLEPresetSource',
                                   'KeySource', 'AuxSource', 'ProductName', 'NextTransitionLayers',
                                   'KeyerStatus', 'KeyOnPreview']
for status in lstCarboniteStatusSubscriptions:
    carbonite.SubscribeStatus(status, None, carbonite_received_data_handler)

tally.SubscribeStatus('Tally', None, tally_received_data_handler)
