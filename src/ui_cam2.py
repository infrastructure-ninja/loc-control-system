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
from extronlib.ui import Button #, Label, Level

import devices

from utilities import DebugPrint

# FIXME - this needs to be controlled by the buttons/system state
def get_cam2_tilt_speed():
    return 10

# FIXME - this needs to be controlled by the buttons/system state
def get_cam2_pan_speed():
    return 10

# FIXME - this needs to be controlled by the buttons/system state
def get_cam2_zoom_speed():
    return 10

btnCAM2_OnAir    = Button(devices.TouchPanel, 143)
btnCAM2_TiltUp   = Button(devices.TouchPanel, 6)
btnCAM2_TiltDown = Button(devices.TouchPanel, 7)
btnCAM2_PanLeft  = Button(devices.TouchPanel, 8)
btnCAM2_PanRight = Button(devices.TouchPanel, 74)
btnCAM2_ZoomIn   = Button(devices.TouchPanel, 75)
btnCAM2_ZoomOut  = Button(devices.TouchPanel, 76)
btnCAM2_Speed1   = Button(devices.TouchPanel, 79)
btnCAM2_Speed2   = Button(devices.TouchPanel, 78)
btnCAM2_Speed3   = Button(devices.TouchPanel, 77)
btnCAM2_Preset1  = Button(devices.TouchPanel, 10)
btnCAM2_Preset2  = Button(devices.TouchPanel, 61)
btnCAM2_Preset3  = Button(devices.TouchPanel, 62)
btnCAM2_Preset4  = Button(devices.TouchPanel, 63)
btnCAM2_Preset5  = Button(devices.TouchPanel, 64)
btnCAM2_Preset6  = Button(devices.TouchPanel, 65)
btnCAM2_Preset7  = Button(devices.TouchPanel, 138)
btnCAM2_Preset8  = Button(devices.TouchPanel, 139)
lstCAM2_SpeedBtns  = [btnCAM2_Speed1, btnCAM2_Speed2, btnCAM2_Speed3]

lstCAM2_PTZBtns    = [btnCAM2_TiltUp, btnCAM2_TiltDown, btnCAM2_PanLeft, btnCAM2_PanRight,
                      btnCAM2_ZoomIn, btnCAM2_ZoomOut]

lstCAM2_PresetBtns = [btnCAM2_Preset1, btnCAM2_Preset2, btnCAM2_Preset3, btnCAM2_Preset4,
                      btnCAM2_Preset5, btnCAM2_Preset6, btnCAM2_Preset7, btnCAM2_Preset8]


@event(lstCAM2_PresetBtns, 'Pressed')
@event(lstCAM2_PTZBtns, ['Pressed', 'Released'])
@event([btnCAM2_Speed1, btnCAM2_Speed2, btnCAM2_Speed3], 'Pressed')
def cam2_buttons_pressed_released(button, state):

    DebugPrint('interface/Cam1ButtonsPressedAndReleased', 'CAM2 PTZ button: [{}] was [{}]'.
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
        (btnCAM2_TiltUp, 'Pressed'):    ('Tilt', 'Up',   'Tilt Speed', get_cam2_tilt_speed),
        (btnCAM2_TiltUp, 'Released'):   ('Tilt', 'Stop', 'Tilt Speed', get_cam2_tilt_speed),
        (btnCAM2_TiltDown, 'Pressed'):  ('Tilt', 'Down', 'Tilt Speed', get_cam2_tilt_speed),
        (btnCAM2_TiltDown, 'Released'): ('Tilt', 'Stop', 'Tilt Speed', get_cam2_tilt_speed),

        (btnCAM2_PanLeft, 'Pressed'):   ('Pan', 'Left',  'Pan Speed', get_cam2_pan_speed),
        (btnCAM2_PanLeft, 'Released'):  ('Pan', 'Stop',  'Pan Speed', get_cam2_pan_speed),
        (btnCAM2_PanRight, 'Pressed'):  ('Pan', 'Right', 'Pan Speed', get_cam2_pan_speed),
        (btnCAM2_PanRight, 'Released'): ('Pan', 'Stop',  'Pan Speed', get_cam2_pan_speed),

        (btnCAM2_ZoomIn, 'Pressed'):    ('Zoom', 'In',   'Zoom Speed', get_cam2_zoom_speed),
        (btnCAM2_ZoomIn, 'Released'):   ('Zoom', 'Stop', 'Zoom Speed', get_cam2_zoom_speed),
        (btnCAM2_ZoomOut, 'Pressed'):   ('Zoom', 'Out',  'Zoom Speed', get_cam2_zoom_speed),
        (btnCAM2_ZoomOut, 'Released'):  ('Zoom', 'Stop', 'Zoom Speed', get_cam2_zoom_speed)
    }

    if button in lstCAM2_PTZBtns:
        command, value, qualifier_parameter, qualifier_function = ptz_button_map[(button, state)]

        qualifier = {qualifier_parameter: qualifier_function()}

        DebugPrint('interface.py/cam2_buttons_pressed_released', '[{}] [{}] [{}]'.
                   format(command, value, qualifier))

        devices.cam2.Set(command, value, qualifier)

    elif button in lstCAM2_PresetBtns:
        preset_btn_map = {
            btnCAM2_Preset1: '1', btnCAM2_Preset2: '2', btnCAM2_Preset3: '3', btnCAM2_Preset4: '4',
            btnCAM2_Preset5: '5', btnCAM2_Preset6: '6', btnCAM2_Preset7: '7', btnCAM2_Preset8: '8'
        }
        devices.cam2.Set('PresetRecall', preset_btn_map[button])

    elif button in [btnCAM2_Speed1, btnCAM2_Speed2, btnCAM2_Speed3]:
        button_map = {btnCAM2_Speed1: 'Slow', btnCAM2_Speed2: 'Medium', btnCAM2_Speed3: 'Fast'}
        devices.system_states.Set('CameraSpeed', button_map[button], {'Camera Number': 2})

#end function (cam2_buttons_pressed_released)
