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

from extronlib import event
from extronlib.ui import Button, Label, Level

import devices
import utilities

from utilities import DebugPrint

# PLAYBACK BUTTONS, LABELS and LEVELS
btnPlayback_TallyPresetsLockout      = Button(devices.TouchPanel, 99)
btnPlayback_TallyTransportLockout    = Button(devices.TouchPanel, 49)

lblPlayback_CurrentClipLength = Label(devices.TouchPanel, 127)
lblPlayback_CurrentTimeCode   = Label(devices.TouchPanel, 128)
lblPlaybackTimeCodeRemaining  = Label(devices.TouchPanel, 203)
lblPlayback_CurrentPlaylist   = Label(devices.TouchPanel, 131)
lblPlayback_CurrentSourceItem = Label(devices.TouchPanel, 132)
lblPlayback_CurrentState      = Label(devices.TouchPanel, 150)
lvlPlayback_ClipPosition      = Level(devices.TouchPanel, 116)

btnPlayback_OnAir     = Button(devices.TouchPanel, 142)
btnPlayback_PLAY      = Button(devices.TouchPanel, 125)
btnPlayback_PAUSE     = Button(devices.TouchPanel, 126)
btnPlayback_STOP      = Button(devices.TouchPanel, 124)
btnPlayback_Playlist1 = Button(devices.TouchPanel, 135)
btnPlayback_Playlist2 = Button(devices.TouchPanel, 136)
btnPlayback_Playlist3 = Button(devices.TouchPanel, 147)
btnPlayback_Playlist4 = Button(devices.TouchPanel, 146)
btnPlayback_Playlist5 = Button(devices.TouchPanel, 148)
btnPlayback_Playlist6 = Button(devices.TouchPanel, 149)

lstPlaybackTransportButtons = [btnPlayback_PLAY, btnPlayback_PAUSE, btnPlayback_STOP]

lstPlayListButtons = [btnPlayback_Playlist1, btnPlayback_Playlist2, btnPlayback_Playlist3,
                      btnPlayback_Playlist4, btnPlayback_Playlist5,  btnPlayback_Playlist6]


@event(lstPlayListButtons, 'Pressed')
@event(lstPlaybackTransportButtons, 'Pressed')
def playback_button_pressed(button, state):

    if button is btnPlayback_PLAY:
        devices.playback.smd101.Set('Playback', 'Play')
        DebugPrint('interface/PlaybackButtonsPressed', 'Playback button pressed', 'Debug')

    elif button is btnPlayback_PAUSE:
        devices.playback.smd101.Set('Playback', 'Pause')
        DebugPrint('interface/PlaybackButtonsPressed', 'Pause button activated', 'Debug')

    elif button is btnPlayback_STOP:
        devices.playback.smd101.Set('Playback', 'Stop')
        DebugPrint('interface/PlaybackButtonsPressed', 'Stop button activated', 'Debug')

    elif button in lstPlayListButtons:

        playlist_button_map = {
            btnPlayback_Playlist1: 'devices/playback/playlist_1_filename',
            btnPlayback_Playlist2: 'devices/playback/playlist_2_filename',
            btnPlayback_Playlist3: 'devices/playback/playlist_3_filename',
            btnPlayback_Playlist4: 'devices/playback/playlist_4_filename',
            btnPlayback_Playlist5: 'devices/playback/playlist_5_filename',
            btnPlayback_Playlist6: 'devices/playback/playlist_6_filename'
        }

        playlist_name = utilities.config.get_value(playlist_button_map[button],
                                                   default_value=None)

        if playlist_name is not None:
            devices.playback.smd101.Set('LoadPlaylistCommand ', playlist_name)
            DebugPrint('interface/PlaybackButtonsPressed',
                       'Loading playlist: [{}]'.format(playlist_name), 'Info')

# end function (PlaybackButtonsPressed)
