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
########### Extron DXP HD 8x8 MATRIX ###########
################################################

if utilities.config.get_value('devices/matrix/enabled', cast_as='boolean'):
  import driver_extr_matrix_DXPHD4k_Series_v1_3_3_0 as MatrixDriver

  matrix = GetConnectionHandler(
    MatrixDriver.EthernetClass(
      utilities.config.get_value('devices/matrix/ipaddress'),
      utilities.config.get_value('devices/matrix/port', cast_as='integer'),
      Model='DXP 88 HD 4K'), 'Temperature')

else:
  matrix = DummyDriver('Extron DXP 88 HD 4K Matrix')

devices.device_objects.update({'matrix': matrix})


def matrix_received_data_handler(command, value, qualifier):
    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/matrix_received_data_handler', 'Matrix switch has been successfully connected', 'Info')

        elif value == 'Disconnected':
            DebugPrint('devices.py/matrix_received_data_handler',
                       'Matrix has been disconnected from the system. Will attempt reconnection..', 'Error')

    else:
        DebugPrint('devices.py/matrix_received_data_handler',
                   'Matrix Unhandled data driver data received: [{}] [{}] [{}]'.format(command, value, qualifier), 'Trace')

# end function (matrix_received_data_handler)

matrix.SubscribeStatus('ConnectionStatus', None, matrix_received_data_handler)
matrix.SubscribeStatus('InputSignalStatus', None, matrix_received_data_handler)
matrix.SubscribeStatus('InputTieStatus', None, matrix_received_data_handler)
matrix.SubscribeStatus('OutputTieStatus', None, matrix_received_data_handler)
