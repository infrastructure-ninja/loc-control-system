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
from extronlib.ui import Button, Label #, Slider

import devices
import utilities
import interface
from utilities import DebugPrint


btnAudio_Channel1 = Button(devices.TouchPanel, 48)
lblChannel1 = Label(devices.TouchPanel, 45)
lblChannel1State = Label(devices.TouchPanel, 219)

btnAudio_Channel2 = Button(devices.TouchPanel, 212)
lblChannel2 = Label(devices.TouchPanel, 50)
lblChannel2State = Label(devices.TouchPanel, 220)

btnAudio_Channel3 = Button(devices.TouchPanel, 218)
lblChannel3 = Label(devices.TouchPanel, 51)
lblChannel3State = Label(devices.TouchPanel, 221)


@event([btnAudio_Channel1, btnAudio_Channel2, btnAudio_Channel3], 'Pressed')
def audio_channel_buttons_pressed(button, state):

    ButtonMap = {btnAudio_Channel1: (1, 5),
                 btnAudio_Channel2: (2, 6),
                 btnAudio_Channel3: (3, 15)}

    channel = utilities.config.get_value('devices/soundboard/number{}_channel'.
                               format(ButtonMap[button][0]), default_value=ButtonMap[button][1],
                               cast_as='string')

    if devices.soundboard.soundboard.ReadStatus('InputMute', {'Channel': channel}) == 'On':
        devices.soundboard.soundboard.Set('InputMute', 'Off', {'Channel': channel})

    else:
        devices.soundboard.soundboard.Set('InputMute', 'On', {'Channel': channel})

# end function (audio_channel_buttons_pressed)
