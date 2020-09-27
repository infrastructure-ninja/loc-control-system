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
from extronlib.ui import Button, Label, Slider

import devices
import utilities
import interface
from utilities import DebugPrint


# Sliders
sliderChannel1 = Slider(devices.TouchPanel, 45)
sliderChannel2 = Slider(devices.TouchPanel, 50)
sliderChannel3 = Slider(devices.TouchPanel, 51)

btnAudio_Channel1 = Button(devices.TouchPanel, 48)


@event(sliderChannel1, ['Pressed', 'Released', 'Changed'])
@event(sliderChannel2, ['Pressed', 'Released', 'Changed'])
@event(sliderChannel3, ['Pressed', 'Released', 'Changed'])
def slider_changed_handler(slider, state, value):
    DebugPrint('ui_audio.py/slider_changed_handler', 'Slider [{}] was changed: [value->{}] [state->{}]'.
               format(slider.Name, value, state), 'Trace')

# end function (slider_changed_handler)