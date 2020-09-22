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

from extronlib.system import Timer

from utilities import DummyDriver
from utilities import DebugPrint
import utilities

from helper_connectionhandler import GetConnectionHandler

import interface
import devices

################################################
# Extron SMD 101 Playback Device
################################################

if utilities.config.get_value('devices/playback/enabled', cast_as='boolean'):
    import driver_extr_sm_SMD101_SMD202_v1_11_4_0 as SMD101Driver

    smd101 = GetConnectionHandler(
        SMD101Driver.SSHClass(
            utilities.config.get_value('devices/playback/ipaddress'),
            utilities.config.get_value('devices/playback/port', cast_as='integer'),
            Credentials=(
                utilities.config.get_value('devices/playback/username'),
                utilities.config.get_value('devices/playback/password'),
            )), 'Temperature')
else:
    smd101 = DummyDriver('Extron SMD101 Playback Unit')

devices.device_objects.update({'smd101': smd101})


def smd101_receive_data_handler(command, value, qualifier):
    DebugPrint('devices.py/smd101_receive_data_handler',
               'Received SMD101 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    if command == 'ConnectionStatus':
        if value == 'Connected':
            DebugPrint('devices.py/smd101_receive_data_handler', 'SMD101 has been successfully connected', 'Info')

            for update in lstSMD101statusSubscriptions:
                if update != 'ConnectionStatus': # ConnectionStatus does not support Updates
                    smd101.Update(update)

            smd101_poll_timer.Resume()

        elif value == 'Disconnected':
            DebugPrint('devices.py/smd101_receive_data_handler',
                       'SMD101 has been disconnected from the system. Will attempt reconnection..', 'Error')
            smd101_poll_timer.Pause()

    elif command == 'CurrentClipLength':
        interface.playback.lblPlayback_CurrentClipLength.SetText(value)

        timecode_in_seconds = utilities.ConvertTimecodeToSeconds(value)
        if timecode_in_seconds <= 0:
            interface.playback.lvlPlayback_ClipPosition.SetVisible(False)
            interface.playback.lvlPlayback_ClipPosition.SetRange(0, 1)
            interface.playback.lblPlaybackTimeCodeRemaining.SetVisible(False)

        else:
            interface.playback.lvlPlayback_ClipPosition.SetVisible(True)
            interface.playback.lvlPlayback_ClipPosition.SetRange(0, timecode_in_seconds)
            interface.playback.lblPlaybackTimeCodeRemaining.SetVisible(True)

    elif command == 'CurrentTimecode':
        interface.playback.lblPlayback_CurrentTimeCode.SetText(value)

        timecode_in_seconds = utilities.ConvertTimecodeToSeconds(value)
        interface.playback.lvlPlayback_ClipPosition.SetLevel(timecode_in_seconds)
        current_clip_length = utilities.ConvertTimecodeToSeconds(smd101.ReadStatus('CurrentClipLength'))

        remaining_seconds = current_clip_length - timecode_in_seconds
        interface.playback.lblPlaybackTimeCodeRemaining.SetText(
            '(-{})'.format(utilities.ConvertSecondsToTimeCode(remaining_seconds)))

    elif command == 'CurrentPlaylistTrack':
        interface.playback.lblPlayback_CurrentPlaylist.SetText(value)

    elif command == 'CurrentSourceItem':
        #FIXME - add some parsing/conversion here so we don't need such a large amount of room
        interface.playback.lblPlayback_CurrentSourceItem.SetText(value)

    elif command == 'Playback':
        value_text = {'Play': 'Playing', 'Pause': 'Paused', 'Stop': 'Stopped'}[value]
        interface.playback.lblPlayback_CurrentState.SetText(value_text)

    else:
        DebugPrint('devices.py/smd101_receive_data_handler',
                   'Playback Unhandled data driver data received: [{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')


# end function (smd101_receive_data_handler)

lstSMD101statusSubscriptions = ['ConnectionStatus', 'Playback', 'CurrentTimecode', 'CurrentSourceItem',
                                'CurrentPlaylistTrack', 'CurrentTimecode', 'CurrentClipLength']

for status in lstSMD101statusSubscriptions:
    smd101.SubscribeStatus(status, None, smd101_receive_data_handler)


def smd101_poll_function(timer, count):
    smd101.Update('CurrentClipLength')
    smd101.Update('CurrentPlaylistTrack')
    smd101.Update('CurrentSourceItem')
    smd101.Update('CurrentTimecode')


# end function(SMD101_poll_function)


smd101_poll_timer = Timer(1, smd101_poll_function)
smd101_poll_timer.Stop()
