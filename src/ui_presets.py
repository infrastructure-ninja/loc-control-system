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
from extronlib.ui import Button

import devices
import interface
import presets
import utilities

from utilities import DebugPrint

btnServicePresetsPage1 = Button(devices.TouchPanel, 217)
btnServicePresetsPage2 = Button(devices.TouchPanel, 225)

lstPresetButtonIDs = [153, 154, 155, 156, 157, 158, 159, 160, 213,
                      227, 228, 229, 230, 231, 232, 233, 234, 235]

lstPresetButtons = []
for button_id in lstPresetButtonIDs:
    lstPresetButtons.append(Button(devices.TouchPanel, button_id))


@event(lstPresetButtons, 'Pressed')
def preset_button_pressed(button, state):
    try:
        DebugPrint('ui_presets.py/preset_button_pressed', 'Trigger Preset #{}'.format(
            lstPresetButtons.index(button) + 1), 'Trace')
        presets.execute_preset(lstPresetButtons.index(button) + 1)

    except ValueError:
        pass

# end function (preset_button_pressed)

@event([btnServicePresetsPage1, btnServicePresetsPage2], 'Pressed')
def page_button_pressed(button, state):
    if button is btnServicePresetsPage1:
        show_page1()

    elif button is btnServicePresetsPage2:
        show_page2()
# end function (page_button_pressed)

def show_page1():
    btnServicePresetsPage1.SetState(1)
    btnServicePresetsPage2.SetState(0)

    for single_button in lstPresetButtons[9:]:
        single_button.SetVisible(False)

    for single_button in lstPresetButtons[0:9]:
        # If the button is enabled then we want it visible, otherwise it'll be set to invisible
        single_button.SetVisible(single_button.Enabled)
# end function (show_page1)

def show_page2():
    btnServicePresetsPage1.SetState(0)
    btnServicePresetsPage2.SetState(1)

    for single_button in lstPresetButtons[9:]:
        # If the button is enabled then we want it visible, otherwise it'll be set to invisible
        single_button.SetVisible(single_button.Enabled)

    for single_button in lstPresetButtons[0:9]:
        single_button.SetVisible(False)
# end function (show_page2)
