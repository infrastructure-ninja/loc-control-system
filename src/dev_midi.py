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

import devices
import presets

################################################
# DecaBox MIDI<->RS-232
################################################
if utilities.config.get_value('devices/midi/enabled', default_value=False, cast_as='boolean'):
  import driver_decaboxmidi_1_0 as MIDIDriver

  midi = MIDIDriver.SerialClass(devices.ControlProcessor,
                                utilities.config.get_value('devices/midi/serial_port',
                                                           cast_as='string'),
                                Baud=38400, Data=8, Parity='None', Stop=1, Mode='RS232')

else:
  midi = DummyDriver('DecaBox MIDI<->RS-232 Gateway')


devices.device_objects.update({'midi': midi})


def midi_received_data_handler(command, value, qualifier):
  print('MIDI CALLBACK ->[{}] [{}] [{}]'.format(command, value, qualifier))

  if value != 'Off':
    midi_note = qualifier['Note']
    midi_channel = qualifier['Channel']

    config_value_to_lookup = 'devices/midi/preset_mapping/{}'.format(midi_note)

    preset_information = utilities.config.get_value(config_value_to_lookup,
                               default_value='None', cast_as='string')

    preset_number, tmp_stage = preset_information.split(':')

    preset_stage = {'p': 'prepare', 'a': 'activate'}[tmp_stage.lower()]

    print('MIDI NOTE     ->', midi_note)
    print('CONFIG VALUE  ->', config_value_to_lookup)
    print('PRESET NUMBER ->', preset_number)
    print('PRESET STAGE  ->', preset_stage)

    if preset_number != 'None' and preset_stage in ['prepare', 'activate']:
      print('TRIGGERING PRESET #{}/{}'.format(preset_number, preset_stage))
      presets.execute_preset(preset_number, stage=preset_stage)


    #DebugPrint('devices.py/smp351_received_data_handler',
    #       'SMP351 Unhandled data driver data received: [{}] [{}] [{}]'.
    #       format(command, value, qualifier), 'Trace')

# end function (midi_received_data_handler)

#FIXME - add the MIDI channel (filter) subscription code here
midi.SubscribeStatus('IncomingNote', None, midi_received_data_handler)
