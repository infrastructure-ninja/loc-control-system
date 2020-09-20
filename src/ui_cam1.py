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

from utilities import DebugPrint

btnCAM1_OnAir    = Button(devices.TouchPanel, 141)
btnCAM1_TiltUp   = Button(devices.TouchPanel, 23)
btnCAM1_TiltDown = Button(devices.TouchPanel, 24)
btnCAM1_PanLeft  = Button(devices.TouchPanel, 25)
btnCAM1_PanRight = Button(devices.TouchPanel, 26)
btnCAM1_ZoomIn   = Button(devices.TouchPanel, 27)
btnCAM1_ZoomOut  = Button(devices.TouchPanel, 28)
btnCAM1_Speed1   = Button(devices.TouchPanel, 31)
btnCAM1_Speed2   = Button(devices.TouchPanel, 30)
btnCAM1_Speed3   = Button(devices.TouchPanel, 29)
btnCAM1_Preset1  = Button(devices.TouchPanel, 34)
btnCAM1_Preset2  = Button(devices.TouchPanel, 35)
btnCAM1_Preset3  = Button(devices.TouchPanel, 36)
btnCAM1_Preset4  = Button(devices.TouchPanel, 37)
btnCAM1_Preset5  = Button(devices.TouchPanel, 38)
btnCAM1_Preset6  = Button(devices.TouchPanel, 39)
btnCAM1_Preset7  = Button(devices.TouchPanel, 40)
btnCAM1_Preset8  = Button(devices.TouchPanel, 44)
lstCAM1_SpeedBtns  = [btnCAM1_Speed1, btnCAM1_Speed2, btnCAM1_Speed3]

lstCAM1_PTZBtns    = [btnCAM1_TiltUp, btnCAM1_TiltDown, btnCAM1_PanLeft, btnCAM1_PanRight,
                      btnCAM1_ZoomIn, btnCAM1_ZoomOut]

lstCAM1_PresetBtns = [btnCAM1_Preset1, btnCAM1_Preset2, btnCAM1_Preset3, btnCAM1_Preset4,
                      btnCAM1_Preset5, btnCAM1_Preset6, btnCAM1_Preset7, btnCAM1_Preset8]


# FIXME - this needs to be controlled by the buttons/system state
def get_cam1_tilt_speed():
    return 10

# FIXME - this needs to be controlled by the buttons/system state
def get_cam1_pan_speed():
    return 10

# FIXME - this needs to be controlled by the buttons/system state
def get_cam1_zoom_speed():
    return 10


@event(lstCAM1_PresetBtns, 'Pressed')
@event(lstCAM1_PTZBtns, ['Pressed', 'Released'])
@event([btnCAM1_Speed1, btnCAM1_Speed2, btnCAM1_Speed3], 'Pressed')
def cam1_buttons_pressed_released(button, state):

    DebugPrint('interface/Cam1ButtonsPressedAndReleased', 'CAM1 PTZ button: [{}] was [{}]'.
               format(button.Name, state), 'Debug')

    # Each button map entry uses a tuple as a key. This tuple is a combination of the button
    # object and the 'Pressed' or 'Released' state. The value for this dictionary entry returns
    # a tuple that contains the 'command', the 'value', and the proper qualifier parameter to pass
    # to our device driver class. Finally it returns a function that will return the necessary
    # qualifier value at the time of execution.
    #
    # While it might look really complex, it reduces redundant 'if/elif' blocks and removes the
    # need for tons of additional lines of code!
    #

    ptz_button_map = {
        (btnCAM1_TiltUp, 'Pressed'):    ('Tilt', 'Up',   'Tilt Speed', get_cam1_tilt_speed),
        (btnCAM1_TiltUp, 'Released'):   ('Tilt', 'Stop', 'Tilt Speed', get_cam1_tilt_speed),
        (btnCAM1_TiltDown, 'Pressed'):  ('Tilt', 'Down', 'Tilt Speed', get_cam1_tilt_speed),
        (btnCAM1_TiltDown, 'Released'): ('Tilt', 'Stop', 'Tilt Speed', get_cam1_tilt_speed),

        (btnCAM1_PanLeft, 'Pressed'):   ('Pan', 'Left',  'Pan Speed', get_cam1_pan_speed),
        (btnCAM1_PanLeft, 'Released'):  ('Pan', 'Stop',  'Pan Speed', get_cam1_pan_speed),
        (btnCAM1_PanRight, 'Pressed'):  ('Pan', 'Right', 'Pan Speed', get_cam1_pan_speed),
        (btnCAM1_PanRight, 'Released'): ('Pan', 'Stop',  'Pan Speed', get_cam1_pan_speed),

        (btnCAM1_ZoomIn, 'Pressed'):    ('Zoom', 'In',   'Zoom Speed', get_cam1_zoom_speed),
        (btnCAM1_ZoomIn, 'Released'):   ('Zoom', 'Stop', 'Zoom Speed', get_cam1_zoom_speed),
        (btnCAM1_ZoomOut, 'Pressed'):   ('Zoom', 'Out',  'Zoom Speed', get_cam1_zoom_speed),
        (btnCAM1_ZoomOut, 'Released'):  ('Zoom', 'Stop', 'Zoom Speed', get_cam1_zoom_speed)
    }

    if button in lstCAM1_PTZBtns:
        command, value, qualifier_parameter, qualifier_function = ptz_button_map[(button, state)]

        qualifier = {qualifier_parameter: qualifier_function()}

        DebugPrint('interface.py/cam1_buttons_pressed_released', '[{}] [{}] [{}]'.
                   format(command, value, qualifier))

        devices.cam1.Set(command, value, qualifier)

    elif button in lstCAM1_PresetBtns:
        preset_btn_map = {
            btnCAM1_Preset1: '1', btnCAM1_Preset2: '2', btnCAM1_Preset3: '3', btnCAM1_Preset4: '4',
            btnCAM1_Preset5: '5', btnCAM1_Preset6: '6', btnCAM1_Preset7: '7', btnCAM1_Preset8: '8'
        }
        devices.cam1.Set('PresetRecall', preset_btn_map[button])

    elif button in [btnCAM1_Speed1, btnCAM1_Speed2, btnCAM1_Speed3]:
        button_map = {btnCAM1_Speed1: 'Slow', btnCAM1_Speed2: 'Medium', btnCAM1_Speed3: 'Fast'}
        devices.system_states.Set('CameraSpeed', button_map[button], {'Camera Number': 1})

#end function (cam1_buttons_pressed_released)
