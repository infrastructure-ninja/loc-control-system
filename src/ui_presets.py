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
import interface
import presets
import utilities

from utilities import DebugPrint

lstPresetButtons = []

lstPresetButtonIDs = [153, 154, 155, 156, 157, 158, 159, 160, 213, 214, 215, 216]
for button_id in lstPresetButtonIDs:
    lstPresetButtons.append(Button(devices.TouchPanel, button_id))


@event(lstPresetButtons, 'Pressed')
def preset_button_pressed(button, state):
    try:
        DebugPrint('ui_presets.py/preset_button_pressed', 'Trigger Preset #{}'.format(lstPresetButtons.index(button) + 1), 'Trace')
        presets.execute_preset(lstPresetButtons.index(button) + 1)

    except ValueError:
        pass

# end function (preset_button_pressed)
