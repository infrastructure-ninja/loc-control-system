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
# Panasonic Camera #4
################################################

if utilities.config.get_value('devices/cam4/enabled', default_value=False, cast_as='boolean'):
    import driver_pana_camera_AW_HE_UE_Series_v1_6_1_1 as CameraDriver

#    cam2 = GetConnectionHandler(
#        CameraDriver.HTTPClass(
#            utilities.config.get_value('devices/cam2/ipaddress'),
#            utilities.config.get_value('devices/cam2/port', default_value=80, cast_as='integer'),
#            utilities.config.get_value('devices/cam2/username', default_value='admin', cast_as='string'),
#            utilities.config.get_value('devices/cam2/password', default_value='password', cast_as='string')),
#    ), 'Tally')
    cam4 = CameraDriver.HTTPClass(
            utilities.config.get_value('devices/cam4/ipaddress'),
            utilities.config.get_value('devices/cam4/port', default_value=80, cast_as='integer'),
            utilities.config.get_value('devices/cam4/username', default_value='admin', cast_as='string'),
            utilities.config.get_value('devices/cam4/password', default_value='password', cast_as='string'),
            Model='AW-HE40SWP')  #FIXME - this should come out of config file

else:
    cam4 = DummyDriver('Panasonic AW-HE40 Camera (CAM#3)')

devices.device_objects.update({'cam4': cam4})


def cam4_received_data_handler(command, value, qualifier):
    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/cam4_received_data_handler', 'Camera #4 has been successfully connected', 'Info')

        elif value == 'Disconnected':
            DebugPrint('devices.py/cam4_received_data_handler',
                       'Camera #4 has been disconnected from the system. Will attempt reconnection..', 'Error')

    else:
        DebugPrint('devices.py/cam4_received_data_handler',
                   'Camera #4 Unhandled data driver data received: [{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

# end function (cam4_received_data_handler)


cam4.SubscribeStatus('ConnectionStatus', None, cam4_received_data_handler)
