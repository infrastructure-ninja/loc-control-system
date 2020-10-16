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
# Extron SMP351 Streaming Media Processor
################################################

if utilities.config.get_value('devices/smp351/enabled', default_value=False, cast_as='boolean'):
    import driver_extr_sm_SMP_300_Series_v1_16_3_0 as SMP351Driver
    smp351 = GetConnectionHandler(
        SMP351Driver.SerialClass(devices.ControlProcessor,
                                 utilities.config.get_value('devices/smp351/serial_port', default_value='COM1',
                                                            cast_as='string'),
                                 Baud=38400, Model='SMP 351'), 'Alarm')

else:
    smp351 = DummyDriver('Extron SMP351 Streaming Media Processor')

devices.device_objects.update({'smp351': smp351})


def smp351_received_data_handler(command, value, qualifier):
    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/smp351_received_data_handler', 'SMP351 has been successfully connected', 'Info')

        elif value == 'Disconnected':
            DebugPrint('devices.py/smp351_received_data_handler',
                       'SMP351 has been disconnected from the system. Will attempt reconnection..', 'Error')

    else:
        DebugPrint('devices.py/smp351_received_data_handler',
                   'SMP351 Unhandled data driver data received: [{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

        #interface.mainscreen.btnMainStreamingStatus.SetText('')
        #interface.mainscreen.btnMainStreamingStatus.SetState(0)

# end function (smp351_received_data_handler)


smp351.SubscribeStatus('ConnectionStatus', None, smp351_received_data_handler)
smp351.SubscribeStatus('Alarm', None, smp351_received_data_handler)
smp351.SubscribeStatus('Record', None, smp351_received_data_handler)
smp351.SubscribeStatus('RTMPStream', None, smp351_received_data_handler)

# When streaming starts and stops (but no record)
# [RTMPStream] [Enable] [{'Stream': 'Archive A'}]]
# [RTMPStream] [Disable] [{'Stream': 'Archive A'}]]


# When recording starts and stops
# [Record] [Start] [None]]
# [Record] [Stop] [None]