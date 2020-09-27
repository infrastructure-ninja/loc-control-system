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


# Main Menu Buttons
btnMainMenuR1C1 = Button(devices.TouchPanel, 1000)
btnMainMenuR2C1 = Button(devices.TouchPanel, 1001)
btnMainMenuR3C1 = Button(devices.TouchPanel, 1002)
btnMainMenuR4C1 = Button(devices.TouchPanel, 1003)

btnMainMenuR1C2 = Button(devices.TouchPanel, 1004)
btnMainMenuR2C2 = Button(devices.TouchPanel, 1005)
btnMainMenuR3C2 = Button(devices.TouchPanel, 1006)
btnMainMenuR4C2 = Button(devices.TouchPanel, 1007)

btnMainMenuR1C3 = Button(devices.TouchPanel, 1008)
btnMainMenuR2C3 = Button(devices.TouchPanel, 1009)
btnMainMenuR3C3 = Button(devices.TouchPanel, 1010)
btnMainMenuR4C3 = Button(devices.TouchPanel, 1011)

btnMainMenuR1C4 = Button(devices.TouchPanel, 1012)
btnMainMenuR2C4 = Button(devices.TouchPanel, 1013)
btnMainMenuR3C4 = Button(devices.TouchPanel, 1014)
btnMainMenuR4C4 = Button(devices.TouchPanel, 1015)

btnMainMenuR1C5 = Button(devices.TouchPanel, 1016)
btnMainMenuR1C5.SetText('Recording Control')

btnMainMenuR2C5 = Button(devices.TouchPanel, 1017)
btnMainMenuR2C5.SetText('Audio Control')

btnMainMenuR3C5 = Button(devices.TouchPanel, 1018)
btnMainMenuR3C5.SetText('System\nOptions')

btnMainMenuR4C5 = Button(devices.TouchPanel, 1019)
btnMainMenuR4C5.SetText('Refresh Configuration')

lstMainPopupButtons = [
                    btnMainMenuR1C1, btnMainMenuR2C1, btnMainMenuR3C1, btnMainMenuR4C1,
                    btnMainMenuR1C2, btnMainMenuR2C2, btnMainMenuR3C2, btnMainMenuR4C2,
                    btnMainMenuR1C3, btnMainMenuR2C3, btnMainMenuR3C3, btnMainMenuR4C3,
                    btnMainMenuR1C4, btnMainMenuR2C4, btnMainMenuR3C4, btnMainMenuR4C4,
                    btnMainMenuR1C5, btnMainMenuR2C5, btnMainMenuR3C5, btnMainMenuR4C5
                    ]


@event(lstMainPopupButtons, 'Pressed')
def main_menu_buttons_pressed(button, state):
    DebugPrint('interface/main_menu_buttons_pressed', 'Button was pressed: [{}]'.format(button.Name), 'Debug')

#                    btnMainMenuR1C1, btnMainMenuR2C1, btnMainMenuR3C1, btnMainMenuR4C1,
#                    btnMainMenuR1C2, btnMainMenuR2C2, btnMainMenuR3C2, btnMainMenuR4C2,
#                    btnMainMenuR1C3, btnMainMenuR2C3, btnMainMenuR3C3, btnMainMenuR4C3,
#                    btnMainMenuR1C4, btnMainMenuR2C4, btnMainMenuR3C4, btnMainMenuR4C4,
#                    btnMainMenuR1C5, btnMainMenuR2C5, btnMainMenuR3C5, btnMainMenuR4C5

    if button is btnMainMenuR1C5:   # Recording Control
        devices.TouchPanel.ShowPopup('POP - Recording Control')
        devices.system_states.Set('ActivePopup', 'POP - Recording Control')

    elif button is btnMainMenuR2C5:   # Audio Control
        devices.TouchPanel.ShowPopup('POP - Audio Control')
        devices.system_states.Set('ActivePopup', 'POP - Audio Control')

    elif button is btnMainMenuR3C5:   # System Options
        devices.TouchPanel.ShowPopup('POP - Options - Main')
        devices.system_states.Set('ActivePopup', 'POP - Options - Main')

    elif button is btnMainMenuR4C5:   # Refresh Configuration
        DebugPrint('interface/main_menu_buttons_pressed', 'Running a refresh of the configuration file', 'Info')
        utilities.config.reload()
        interface.initialize_all()


