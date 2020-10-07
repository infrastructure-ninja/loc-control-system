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
from extronlib.system import Wait

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

            @Wait(1)
            def update_status():
                update_all_soundboard_status()

        elif value == 'Disconnected':
            DebugPrint('devices.py/soundboard_receive_data_handler',
                       'Yamaha TF5 soundboard has been disconnected from the system. Will attempt reconnection..',
                       'Error')

    elif command == 'AuxLevel':
        DebugPrint('devices.py/soundboard_receive_data_handler',
                   'Received Yamaha TF5 Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Trace')

        if qualifier['Input Channel'] == '5' and qualifier['Aux Channel'] == '13':
            pass

        elif qualifier['Input Channel'] == '6' and qualifier['Aux Channel'] == '13':
            pass

        elif qualifier['Input Channel'] == '15' and qualifier['Aux Channel'] == '13':
            pass

    elif command == 'InputMute':
        DebugPrint('devices.py/soundboard_receive_data_handler',
                   'Received Yamaha TF5 Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Trace')

        if qualifier['Channel'] == utilities.config.get_value(
                'devices/soundboard/number1_channel', default_value='5', cast_as='string'):

            if value == 'On':
                interface.audio.btnAudio_Channel1.SetState(1)
                interface.audio.lblChannel1State.SetText('ON')

            else:
                interface.audio.btnAudio_Channel1.SetState(0)
                interface.audio.lblChannel1State.SetText('MUTED')

        elif qualifier['Channel'] == utilities.config.get_value(
                'devices/soundboard/number2_channel', default_value='6', cast_as='string'):

            if value == 'On':
                interface.audio.btnAudio_Channel2.SetState(1)
                interface.audio.lblChannel2State.SetText('ON')
            else:
                interface.audio.btnAudio_Channel2.SetState(0)
                interface.audio.lblChannel2State.SetText('MUTED')

        elif qualifier['Channel'] == utilities.config.get_value(
                'devices/soundboard/number3_channel', default_value='15', cast_as='string'):

            if value == 'On':
                interface.audio.btnAudio_Channel3.SetState(1)
                interface.audio.lblChannel3State.SetText('ON')

            else:
                interface.audio.btnAudio_Channel3.SetState(0)
                interface.audio.lblChannel3State.SetText('MUTED')


    else:
        DebugPrint('devices.py/soundboard_receive_data_handler',
                   'Soundboard Unhandled data driver data received: [{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

        #interface.mainscreen.btnMainSoundMicsActive.SetText('')
        #interface.mainscreen.btnMainSoundMicsActive.SetState(0)

        #interface.mainscreen.btnMainSoundPlaybackActive.SetText('')
        #interface.mainscreen.btnMainSoundPlaybackActive.SetState(0)

# end function (soundboard_receive_data_handler)


lstSoundboardStatusSubscriptions = ['ConnectionStatus','Firmware', 'OutputMute',
                                    'OutputLevel','InputMute', 'InputLevel',
                                    'AuxMute', 'AuxLevel', 'StereoInLevel',
                                    'StereoInMute']

for status in lstSoundboardStatusSubscriptions:
    soundboard.SubscribeStatus(status, None, soundboard_receive_data_handler)


def update_all_soundboard_status():
    print('UPDATING ALL SOUND BOARD STATUS ..')

    # Primary beltpack
    input1 = utilities.config.get_value('devices/soundboard/number1_channel',
                                        default_value='5', cast_as='integer')

    soundboard.Update('InputMute', {'Channel': input1})
    soundboard.Update('AuxLevel', {'Input Channel': input1, 'Aux Channel': 13})


    # Secondary beltpack
    input2 = utilities.config.get_value('devices/soundboard/number2_channel',
                                        default_value='6', cast_as='integer')

    soundboard.Update('InputMute', {'Channel': input2})
    soundboard.Update('AuxLevel', {'Input Channel': input2, 'Aux Channel': 13})

    # Playback System
    input3 = utilities.config.get_value('devices/soundboard/number3_channel',
                                        default_value='15', cast_as='integer')

    soundboard.Update('InputMute', {'Channel': input3})
    soundboard.Update('AuxLevel', {'Input Channel': input3, 'Aux Channel': 13})

    try:
        soundboard.Update('InputMute', {'Channel': input3 + 1})
        soundboard.Update('AuxLevel', {'Input Channel': input3 + 1, 'Aux Channel': 13})
    except:
        pass