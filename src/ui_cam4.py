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

def get_cam4_tilt_speed():
    current_camera_speed_state = devices.system_states.ReadStatus('CameraSpeed', {'Camera Number': 4})

    tilt_speed = utilities.config.get_value('devices/cam4/speed_tilt_{}'.
                                            format(current_camera_speed_state), default_value=40, cast_as='integer')

    DebugPrint('ui_cam4.py/get_cam4_tilt_speed', 'Returning {} as tilt speed'.format(tilt_speed), 'Trace')

    return tilt_speed

def get_cam4_pan_speed():
    current_camera_speed_state = devices.system_states.ReadStatus('CameraSpeed', {'Camera Number': 4})

    pan_speed = utilities.config.get_value('devices/cam4/speed_pan_{}'.
                                            format(current_camera_speed_state), default_value=40, cast_as='integer')

    DebugPrint('ui_cam4.py/get_cam4_pan_speed', 'Returning {} as pan speed'.format(pan_speed), 'Trace')

    return pan_speed

def get_cam4_zoom_speed():
    current_camera_speed_state = devices.system_states.ReadStatus('CameraSpeed', {'Camera Number': 4})

    zoom_speed = utilities.config.get_value('devices/cam4/speed_zoom_{}'.
                                            format(current_camera_speed_state), default_value=40, cast_as='integer')

    DebugPrint('ui_cam4.py/get_cam4_zoom_speed', 'Returning {} as zoom speed'.format(zoom_speed), 'Trace')

    return zoom_speed


lblCam4_PresetUpdatedNotice = Label(devices.TouchPanel, 60)
btnCam4_OnAir    = Button(devices.TouchPanel, 145)
btnCam4_TallyLockout = Button(devices.TouchPanel, 21)

btnCam4_TiltUp   = Button(devices.TouchPanel, 184)
btnCam4_TiltDown = Button(devices.TouchPanel, 185)
btnCam4_PanLeft  = Button(devices.TouchPanel, 186)
btnCam4_PanRight = Button(devices.TouchPanel, 187)
btnCam4_ZoomIn   = Button(devices.TouchPanel, 188)
btnCam4_ZoomOut  = Button(devices.TouchPanel, 189)

btnCam4_Speed1   = Button(devices.TouchPanel, 192)
btnCam4_Speed2   = Button(devices.TouchPanel, 191)
btnCam4_Speed3   = Button(devices.TouchPanel, 190)

cam4_hold_time = 3  # I don't see any point in this being a config file option, but perhaps I am mistaken?
btnCam4_Preset1  = Button(devices.TouchPanel, 92, holdTime=cam4_hold_time)
btnCam4_Preset2  = Button(devices.TouchPanel, 93, holdTime=cam4_hold_time)
btnCam4_Preset3  = Button(devices.TouchPanel, 94, holdTime=cam4_hold_time)
btnCam4_Preset4  = Button(devices.TouchPanel, 95, holdTime=cam4_hold_time)
btnCam4_Preset5  = Button(devices.TouchPanel, 96, holdTime=cam4_hold_time)
btnCam4_Preset6  = Button(devices.TouchPanel, 97, holdTime=cam4_hold_time)
btnCam4_Preset7  = Button(devices.TouchPanel, 194, holdTime=cam4_hold_time)
btnCam4_Preset8  = Button(devices.TouchPanel, 195, holdTime=cam4_hold_time)

lstCam4_SpeedBtns  = [btnCam4_Speed1, btnCam4_Speed2, btnCam4_Speed3]

lstCam4_PTZBtns    = [btnCam4_TiltUp, btnCam4_TiltDown, btnCam4_PanLeft, btnCam4_PanRight,
                      btnCam4_ZoomIn, btnCam4_ZoomOut]

lstCam4_PresetBtns = [btnCam4_Preset1, btnCam4_Preset2, btnCam4_Preset3, btnCam4_Preset4,
                      btnCam4_Preset5, btnCam4_Preset6, btnCam4_Preset7, btnCam4_Preset8]


@event(lstCam4_PresetBtns, ['Tapped', 'Held'])
@event(lstCam4_PTZBtns, ['Pressed', 'Released'])
@event(lstCam4_SpeedBtns, 'Pressed')
@event(btnCam4_TallyLockout, 'Pressed')
def cam4_buttons_pressed_released(button, state):

    DebugPrint('interface/cam4_buttons_pressed_released', 'CAM4 PTZ button: [{}] was [{}]'.
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
        (btnCam4_TiltUp, 'Pressed'):    ('PanTilt', 'Up', 'Speed', get_cam4_tilt_speed),
        (btnCam4_TiltUp, 'Released'):   ('PanTilt', 'Stop', 'Speed', get_cam4_tilt_speed),
        (btnCam4_TiltDown, 'Pressed'):  ('PanTilt', 'Down', 'Speed', get_cam4_tilt_speed),
        (btnCam4_TiltDown, 'Released'): ('PanTilt', 'Stop', 'Speed', get_cam4_tilt_speed),

        (btnCam4_PanLeft, 'Pressed'):   ('PanTilt', 'Left',  'Speed', get_cam4_tilt_speed),
        (btnCam4_PanLeft, 'Released'):  ('PanTilt', 'Stop',  'Speed', get_cam4_tilt_speed),
        (btnCam4_PanRight, 'Pressed'):  ('PanTilt', 'Right', 'Speed', get_cam4_tilt_speed),
        (btnCam4_PanRight, 'Released'): ('PanTilt', 'Stop',  'Speed', get_cam4_tilt_speed),

        (btnCam4_ZoomIn, 'Pressed'):    ('Zoom', 'Tele',   'Speed', get_cam4_tilt_speed),
        (btnCam4_ZoomIn, 'Released'):   ('Zoom', 'Stop', 'Speed', get_cam4_tilt_speed),
        (btnCam4_ZoomOut, 'Pressed'):   ('Zoom', 'Wide',  'Speed', get_cam4_tilt_speed),
        (btnCam4_ZoomOut, 'Released'):  ('Zoom', 'Stop', 'Speed', get_cam4_tilt_speed)
    }

    if button in lstCam4_PTZBtns:
        command, value, qualifier_parameter, qualifier_function = ptz_button_map[(button, state)]

        qualifier = {qualifier_parameter: qualifier_function()}

        DebugPrint('interface.py/cam4_buttons_pressed_released', '[{}] [{}] [{}]'.
                   format(command, value, qualifier), 'Trace')

        devices.cam4.cam4.Set(command, value, qualifier)

    elif button in lstCam4_PresetBtns:
        preset_btn_map = {
            btnCam4_Preset1: '1', btnCam4_Preset2: '2', btnCam4_Preset3: '3', btnCam4_Preset4: '4',
            btnCam4_Preset5: '5', btnCam4_Preset6: '6', btnCam4_Preset7: '7', btnCam4_Preset8: '8'
        }

        if state == 'Held':     # A hold will SET a preset
            DebugPrint('ui_cam4.py/cam4_buttons_pressed_released', 'Preset #{} was set'.
                       format(preset_btn_map[button]), 'Debug')

            devices.cam4.cam4.Set('Preset', preset_btn_map[button], {'Type': 'Save'})

            lblCam4_PresetUpdatedNotice.SetVisible(True)

            @Wait(2)
            def hide_notice():
                lblCam4_PresetUpdatedNotice.SetVisible(False)

        else:       # A tap will RECALL the preset
            DebugPrint('ui_cam4.py/cam4_buttons_pressed_released', 'Preset #{} was recalled'.
                       format(preset_btn_map[button]), 'Debug')

            devices.cam4.cam4.Set('Preset', preset_btn_map[button], {'Type': 'Recall'})

    elif button in lstCam4_SpeedBtns:
        button_map = {btnCam4_Speed1: 'Slow', btnCam4_Speed2: 'Medium', btnCam4_Speed3: 'Fast'}
        devices.system_states.Set('CameraSpeed', button_map[button], {'Camera Number': 4})

    elif button is btnCam4_TallyLockout:
        btnCam4_TallyLockout.SetVisible(False)

#end function (cam2_buttons_pressed_released)
