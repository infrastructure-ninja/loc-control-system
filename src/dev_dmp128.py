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
# Extron DMP128 Plus audio processor
################################################

if utilities.config.get_value('devices/dmp128/enabled', default_value=False, cast_as='boolean'):
    import driver_extr_dsp_DMP_128_Plus_Series_v1_9_0_0 as DMP128PlusDriver

    dmp128 = GetConnectionHandler(
        DMP128PlusDriver.EthernetClass(
            utilities.config.get_value('devices/dmp128/ipaddress'),
            utilities.config.get_value('devices/dmp128/port', cast_as='integer'),
            Model='DMP 128 Plus'), 'PartNumber')

else:
    dmp128 = DummyDriver('Extron DMP128 Plus audio processor')

devices.device_objects.update({'dmp128': dmp128})


def dmp128_received_data_handler(command, value, qualifier):
    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/dmp128_received_data_handler', 'DMP128 Plus has been successfully connected', 'Info')
            dmp128.Set('UnsolicitedMeterGroupNumber', '1')
            dmp128.Send('wR10GRPU\r\n')  # Global Meter Response Timer

        elif value == 'Disconnected':
            DebugPrint('devices.py/dmp128_received_data_handler',
                       'DMP128 Plus has been disconnected from the system. Will attempt reconnection..', 'Error')

    elif command == 'InputSignalLevelMonitor':
        pass

    elif command == 'UnsolicitedMeterData':
        # The DMP 128 Plus returns data from 0 (highest) to 1500 (lowest)
        # This little formula turns it into a more tradition -1500 to 0 value,
        # which is necessary to make the Level widget working properly
        meter_data = (int(value) - (int(value) * 2))

        if 'OID' in qualifier and qualifier['OID'] == 0:
            interface.mainscreen.lvlMainScreenLevel1.SetLevel(meter_data)

        elif 'OID' in qualifier and qualifier['OID'] == 1:
            interface.mainscreen.lvlMainScreenLevel2.SetLevel(meter_data)

        # This particular unsolicited update is *really* talkative,
        # and will fill up any log file you're working with - so we normally keep it disabled
        # DebugPrint('devices.py/dmp128_received_data_handler',
        #            'UnsolicitedMeterData data received: [{}] [{}] [{}] [METER DATA:{}]'.
        #            format(command, value, qualifier, meter_data), 'Trace')

    else:
        DebugPrint('devices.py/dmp128_received_data_handler',
                   'DMP128 Plus Unhandled data driver data received: [{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

# end function (dmp128_received_data_handler)


dmp128.SubscribeStatus('ConnectionStatus', None, dmp128_received_data_handler)
# dmp128.SubscribeStatus('InputSignalLevelMonitor', None, dmp128_received_data_handler)
dmp128.SubscribeStatus('UnsolicitedMeterData', {'OID': 0}, dmp128_received_data_handler)
dmp128.SubscribeStatus('UnsolicitedMeterData', {'OID': 1}, dmp128_received_data_handler)
