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

from helper_connectionhandler import GetConnectionHandler

from utilities import DummyDriver
from utilities import DebugPrint
import utilities

import interface
import devices

################################################
# Yamaha TF5 Soundboard
################################################

if utilities.config.get_value('devices/soundboard/enabled', cast_as='boolean'):
    import driver_yama_dsp_TF1_TF5_TFRack_v1_0_0_0 as SoundboardDriver

    soundboard = GetConnectionHandler(
        SoundboardDriver.EthernetClass(
            utilities.config.get_value('devices/soundboard/ipaddress'),
            utilities.config.get_value('devices/soundboard/port', cast_as='integer'),
            Model='TF5'), 'Firmware')
else:
    soundboard = DummyDriver('Yamaha TF5 Sound Console')

devices.device_objects.update({'soundboard': soundboard})


def soundboard_receive_data_handler(command, value, qualifier):
    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/soundboard_receive_data_handler',
                       'Yamaha TF5 soundboard has been successfully connected', 'Info')

        elif value == 'Disconnected':
            DebugPrint('devices.py/soundboard_receive_data_handler',
                       'Yamaha TF5 soundboard has been disconnected from the system. Will attempt reconnection..',
                       'Error')

    else:
        DebugPrint('devices.py/soundboard_receive_data_handler',
                   'Soundboard Unhandled data driver data received: [{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

# end function (soundboard_receive_data_handler)

soundboard.SubscribeStatus('ConnectionStatus', None, soundboard_receive_data_handler)
soundboard.SubscribeStatus('InputMute', None, soundboard_receive_data_handler)
soundboard.SubscribeStatus('OutputLevel', None, soundboard_receive_data_handler)
soundboard.SubscribeStatus('InputLevel', None, soundboard_receive_data_handler)
