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
from extronlib.system import Wait

import devices

import utilities
from utilities import DebugPrint

def get_cam3_tilt_speed():
    current_camera_speed_state = devices.system_states.ReadStatus('CameraSpeed', {'Camera Number': 3})

    tilt_speed = utilities.config.get_value('devices/cam3/speed_tilt_{}'.
                                            format(current_camera_speed_state), default_value=40, cast_as='integer')

    DebugPrint('ui_cam3.py/get_cam3_tilt_speed', 'Returning {} as tilt speed'.format(tilt_speed), 'Trace')

    return tilt_speed

def get_cam3_pan_speed():
    current_camera_speed_state = devices.system_states.ReadStatus('CameraSpeed', {'Camera Number': 3})

    pan_speed = utilities.config.get_value('devices/cam3/speed_pan_{}'.
                                            format(current_camera_speed_state), default_value=40, cast_as='integer')

    DebugPrint('ui_cam3.py/get_cam3_pan_speed', 'Returning {} as pan speed'.format(pan_speed), 'Trace')

    return pan_speed

def get_cam3_zoom_speed():
    current_camera_speed_state = devices.system_states.ReadStatus('CameraSpeed', {'Camera Number': 3})

    zoom_speed = utilities.config.get_value('devices/cam3/speed_zoom_{}'.
                                            format(current_camera_speed_state), default_value=40, cast_as='integer')

    DebugPrint('ui_cam3.py/get_cam3_zoom_speed', 'Returning {} as zoom speed'.format(zoom_speed), 'Trace')

    return zoom_speed


lblCam3_PresetUpdatedNotice = Label(devices.TouchPanel, 59)
btnCam3_OnAir    = Button(devices.TouchPanel, 144)
btnCam3_TallyLockout = Button(devices.TouchPanel, 20)

btnCam3_TiltUp   = Button(devices.TouchPanel, 68)
btnCam3_TiltDown = Button(devices.TouchPanel, 69)
btnCam3_PanLeft  = Button(devices.TouchPanel, 70)
btnCam3_PanRight = Button(devices.TouchPanel, 71)
btnCam3_ZoomIn   = Button(devices.TouchPanel, 72)
btnCam3_ZoomOut  = Button(devices.TouchPanel, 73)

btnCam3_Speed1   = Button(devices.TouchPanel, 82)
btnCam3_Speed2   = Button(devices.TouchPanel, 81)
btnCam3_Speed3   = Button(devices.TouchPanel, 80)

cam3_hold_time = 3  # I don't see any point in this being a config file option, but perhaps I am mistaken?
btnCam3_Preset1  = Button(devices.TouchPanel, 12, holdTime=cam3_hold_time)
btnCam3_Preset2  = Button(devices.TouchPanel, 13, holdTime=cam3_hold_time)
btnCam3_Preset3  = Button(devices.TouchPanel, 14, holdTime=cam3_hold_time)
btnCam3_Preset4  = Button(devices.TouchPanel, 15, holdTime=cam3_hold_time)
btnCam3_Preset5  = Button(devices.TouchPanel, 66, holdTime=cam3_hold_time)
btnCam3_Preset6  = Button(devices.TouchPanel, 67, holdTime=cam3_hold_time)
btnCam3_Preset7  = Button(devices.TouchPanel, 84, holdTime=cam3_hold_time)
btnCam3_Preset8  = Button(devices.TouchPanel, 85, holdTime=cam3_hold_time)

lstCam3_SpeedBtns  = [btnCam3_Speed1, btnCam3_Speed2, btnCam3_Speed3]

lstCam3_PTZBtns    = [btnCam3_TiltUp, btnCam3_TiltDown, btnCam3_PanLeft, btnCam3_PanRight,
                      btnCam3_ZoomIn, btnCam3_ZoomOut]

lstCam3_PresetBtns = [btnCam3_Preset1, btnCam3_Preset2, btnCam3_Preset3, btnCam3_Preset4,
                      btnCam3_Preset5, btnCam3_Preset6, btnCam3_Preset7, btnCam3_Preset8]


@event(lstCam3_PresetBtns, ['Tapped', 'Held'])
@event(lstCam3_PTZBtns, ['Pressed', 'Released'])
@event(lstCam3_SpeedBtns, 'Pressed')
@event(btnCam3_TallyLockout, 'Pressed')
def cam3_buttons_pressed_released(button, state):

    DebugPrint('interface/cam3_buttons_pressed_released', 'CAM3 PTZ button: [{}] was [{}]'.
               format(button.Name, state), 'Trace')

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
        (btnCam3_TiltUp, 'Pressed'):    ('PanTilt', 'Up', 'Speed', get_cam3_tilt_speed),
        (btnCam3_TiltUp, 'Released'):   ('PanTilt', 'Stop', 'Speed', get_cam3_tilt_speed),
        (btnCam3_TiltDown, 'Pressed'):  ('PanTilt', 'Down', 'Speed', get_cam3_tilt_speed),
        (btnCam3_TiltDown, 'Released'): ('PanTilt', 'Stop', 'Speed', get_cam3_tilt_speed),

        (btnCam3_PanLeft, 'Pressed'):   ('PanTilt', 'Left',  'Speed', get_cam3_tilt_speed),
        (btnCam3_PanLeft, 'Released'):  ('PanTilt', 'Stop',  'Speed', get_cam3_tilt_speed),
        (btnCam3_PanRight, 'Pressed'):  ('PanTilt', 'Right', 'Speed', get_cam3_tilt_speed),
        (btnCam3_PanRight, 'Released'): ('PanTilt', 'Stop',  'Speed', get_cam3_tilt_speed),

        (btnCam3_ZoomIn, 'Pressed'):    ('Zoom', 'Tele',   'Speed', get_cam3_tilt_speed),
        (btnCam3_ZoomIn, 'Released'):   ('Zoom', 'Stop', 'Speed', get_cam3_tilt_speed),
        (btnCam3_ZoomOut, 'Pressed'):   ('Zoom', 'Wide',  'Speed', get_cam3_tilt_speed),
        (btnCam3_ZoomOut, 'Released'):  ('Zoom', 'Stop', 'Speed', get_cam3_tilt_speed)
    }

    if button in lstCam3_PTZBtns:
        command, value, qualifier_parameter, qualifier_function = ptz_button_map[(button, state)]

        qualifier = {qualifier_parameter: qualifier_function()}

        DebugPrint('interface.py/cam3_buttons_pressed_released', '[{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

        devices.cam3.cam3.Set(command, value, qualifier)

    elif button in lstCam3_PresetBtns:
        preset_btn_map = {
            btnCam3_Preset1: '1', btnCam3_Preset2: '2', btnCam3_Preset3: '3', btnCam3_Preset4: '4',
            btnCam3_Preset5: '5', btnCam3_Preset6: '6', btnCam3_Preset7: '7', btnCam3_Preset8: '8'
        }

        if state == 'Held':     # A hold will SET a preset
            DebugPrint('ui_cam3.py/cam3_buttons_pressed_released', 'Preset #{} was set'.
                       format(preset_btn_map[button]), 'Debug')

            devices.cam3.cam3.Set('Preset', preset_btn_map[button], {'Type': 'Save'})

            lblCam3_PresetUpdatedNotice.SetVisible(True)

            @Wait(2)
            def hide_notice():
                lblCam3_PresetUpdatedNotice.SetVisible(False)

        else:       # A tap will RECALL the preset
            DebugPrint('ui_cam3.py/cam3_buttons_pressed_released', 'Preset #{} was recalled'.
                       format(preset_btn_map[button]), 'Debug')

            devices.cam3.cam3.Set('Preset', preset_btn_map[button], {'Type': 'Recall'})

    elif button in lstCam3_SpeedBtns:
        button_map = {btnCam3_Speed1: 'Slow', btnCam3_Speed2: 'Medium', btnCam3_Speed3: 'Fast'}
        devices.system_states.Set('CameraSpeed', button_map[button], {'Camera Number': 3})

    elif button is btnCam3_TallyLockout:
        btnCam3_TallyLockout.SetVisible(False)

#end function (cam2_buttons_pressed_released)
