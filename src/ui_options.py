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
from extronlib.ui import Button, Label

import devices
import utilities
import interface
from utilities import DebugPrint


# Options - Ignore MIDI
btnSettingIgnoreMIDI = Button(devices.TouchPanel, 214)
lblSettingIgnoreMIDI = Label(devices.TouchPanel, 215)


@event(btnSettingIgnoreMIDI, 'Pressed')
def btn_setting_ignore_midi_pressed(button, state):
    current_state = devices.system_states.ReadStatus('IgnoreMIDI')
    if current_state == 'On':
        devices.system_states.Set('IgnoreMIDI', 'Off')

    else:
        devices.system_states.Set('IgnoreMIDI', 'On')
