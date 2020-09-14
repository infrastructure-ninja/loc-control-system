from extronlib import event
from extronlib.ui import Button, Label, Level  #,  Slider
from extronlib.system import Wait

import devices
from utilities import DebugPrint
import utilities

# MENU and QuickButtons
btnMainMenu = Button(devices.TouchPanel, 16)
btnQuickButton1 = Button(devices.TouchPanel, 111)
btnQuickButton2 = Button(devices.TouchPanel, 205)
btnQuickButton3 = Button(devices.TouchPanel, 206)
btnQuickButton4 = Button(devices.TouchPanel, 207)
lstMainMenuButtons = [btnMainMenu, btnQuickButton1, btnQuickButton2, btnQuickButton3, btnQuickButton4]

btnCAM1_PTZ = Button(devices.TouchPanel, 1)
btnCAM2_PTZ = Button(devices.TouchPanel, 2)
btnCAM3_PTZ = Button(devices.TouchPanel, 43)
btnCAM4_PTZ = Button(devices.TouchPanel, 46)
lstPTZButtons = [btnCAM1_PTZ, btnCAM2_PTZ, btnCAM3_PTZ, btnCAM4_PTZ]


btnCAM1_Preview = Button(devices.TouchPanel, 33)
btnCAM2_Preview = Button(devices.TouchPanel, 3)
btnCAM3_Preview = Button(devices.TouchPanel, 41)
btnCAM4_Preview = Button(devices.TouchPanel, 42)
btnIN5_Preview  = Button(devices.TouchPanel, 100)
btnIN6_Preview  = Button(devices.TouchPanel, 107)
lstPreviewButtons = [btnCAM1_Preview, btnCAM2_Preview, btnCAM3_Preview,
                     btnCAM4_Preview, btnIN5_Preview, btnIN6_Preview]


btnCAM1_AUX = Button(devices.TouchPanel, 98)
btnCAM2_AUX = Button(devices.TouchPanel, 101)
btnCAM3_AUX = Button(devices.TouchPanel, 102)
btnCAM4_AUX = Button(devices.TouchPanel, 103)
btnIN5_AUX  = Button(devices.TouchPanel, 104)
lstAuxButtons = [btnCAM1_AUX, btnCAM2_AUX, btnCAM3_AUX, btnCAM4_AUX, btnIN5_AUX]

btnCUT = Button(devices.TouchPanel, 5)
btnMIX = Button(devices.TouchPanel, 52)

btnPlaybackControls = Button(devices.TouchPanel, 47)
btnBottomBar4 = Button(devices.TouchPanel, 59)
btnBottomBar5 = Button(devices.TouchPanel, 60)
btnBottomBar6 = Button(devices.TouchPanel, 99)
btnBottomBar3 = Button(devices.TouchPanel, 110)

#FIXME - REMOVE THESE?
btnPreview_KeyOFF = Button(devices.TouchPanel, 106)
btnPreview_Key1and2 = Button(devices.TouchPanel, 183)
##

btnPreview_Key1 = Button(devices.TouchPanel, 108)
btnPreview_Key2 = Button(devices.TouchPanel, 182)

btnCloseNoButtonsA = Button(devices.TouchPanel, 11)
btnCloseNoButtonsB = Button(devices.TouchPanel, 115)


### PLAYBACK CONTROLS (and LABELS) ###
lblPlayback_CurrentClipLength = Label(devices.TouchPanel, 127)
lblPlayback_CurrentTimeCode   = Label(devices.TouchPanel, 128)
lblPlaybackTimeCodeRemaining  = Label(devices.TouchPanel, 203)
lblPlayback_CurrentPlaylist   = Label(devices.TouchPanel, 131)
lblPlayback_CurrentSourceItem = Label(devices.TouchPanel, 132)
lblPlayback_CurrentState      = Label(devices.TouchPanel, 150)
lvlPlayback_ClipPosition      = Level(devices.TouchPanel, 116)

btnPlayback_PLAY      = Button(devices.TouchPanel, 125)
btnPlayback_PAUSE     = Button(devices.TouchPanel, 126)
btnPlayback_STOP      = Button(devices.TouchPanel, 124)
btnPlayback_Playlist1 = Button(devices.TouchPanel, 135)
btnPlayback_Playlist2 = Button(devices.TouchPanel, 136)
btnPlayback_Playlist3 = Button(devices.TouchPanel, 147)
btnPlayback_Playlist4 = Button(devices.TouchPanel, 146)
btnPlayback_Playlist5 = Button(devices.TouchPanel, 148)
btnPlayback_Playlist6 = Button(devices.TouchPanel, 149)
lstPlaybackTransportButtons = [btnPlayback_PLAY, btnPlayback_PAUSE, btnPlayback_STOP]
lstPlayListButtons = [btnPlayback_Playlist1, btnPlayback_Playlist2, btnPlayback_Playlist3,
                      btnPlayback_Playlist4, btnPlayback_Playlist5,  btnPlayback_Playlist6]

def initialize_all():
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')

    # We want these things hidden until it's show by other code/events
    lvlPlayback_ClipPosition.SetVisible(False)
    lblPlaybackTimeCodeRemaining.SetVisible(False)

    # Initialize a bunch of buttons using text pulled from our configuration file
    # This dictionary stores the button object we want to "SetText' on, and the configuration
    # path where we will be able to retrieve the name. The loop at the bottom makes it happen.
    init_button_name_dict = {
        btnPlayback_Playlist1: 'devices/playback/playlist_1_name',
        btnPlayback_Playlist2: 'devices/playback/playlist_2_name',
        btnPlayback_Playlist3: 'devices/playback/playlist_3_name',
        btnPlayback_Playlist4: 'devices/playback/playlist_4_name',
        btnPlayback_Playlist5: 'devices/playback/playlist_5_name',
        btnPlayback_Playlist6: 'devices/playback/playlist_6_name',

        btnCAM1_Preset1: 'devices/cam1/preset_1_name',
        btnCAM1_Preset2: 'devices/cam1/preset_2_name',
        btnCAM1_Preset3: 'devices/cam1/preset_3_name',
        btnCAM1_Preset4: 'devices/cam1/preset_4_name',
        btnCAM1_Preset5: 'devices/cam1/preset_5_name',
        btnCAM1_Preset6: 'devices/cam1/preset_6_name',
        btnCAM1_Preset7: 'devices/cam1/preset_7_name',
        btnCAM1_Preset8: 'devices/cam1/preset_8_name',

        btnCAM2_Preset1: 'devices/cam2/preset_1_name',
        btnCAM2_Preset2: 'devices/cam2/preset_2_name',
        btnCAM2_Preset3: 'devices/cam2/preset_3_name',
        btnCAM2_Preset4: 'devices/cam2/preset_4_name',
        btnCAM2_Preset5: 'devices/cam2/preset_5_name',
        btnCAM2_Preset6: 'devices/cam2/preset_6_name',
        btnCAM2_Preset7: 'devices/cam2/preset_7_name',
        btnCAM2_Preset8: 'devices/cam2/preset_8_name',

        btnQuickButton1: 'interface/quickbuttons/button_1_name',
        btnQuickButton2: 'interface/quickbuttons/button_2_name',
        btnQuickButton3: 'interface/quickbuttons/button_3_name',
        btnQuickButton4: 'interface/quickbuttons/button_4_name',
    }

    for button, config_key in init_button_name_dict.items():
        button.SetText(utilities.config.get_value(config_key, default_value='(unused)'))

    # Show/Hide our "sidebar buttons" based on whether they are enabled in the configuration or not
    init_button_visible_dict = {
        btnQuickButton1: 'interface/quickbuttons/button_1_enabled',
        btnQuickButton2: 'interface/quickbuttons/button_2_enabled',
        btnQuickButton3: 'interface/quickbuttons/button_3_enabled',
        btnQuickButton4: 'interface/quickbuttons/button_4_enabled'
    }

    for button, config_key in init_button_visible_dict.items():
        button.SetVisible(utilities.config.get_value(config_key, default_value=False, cast_as='boolean'))


    # Show/Hide our Camera UI buttons based on whether the camera is disabled in the configuration
    cam1_is_enabled = utilities.config.get_value('devices/cam1/enabled', default_value=False, cast_as='boolean')
    for i in [btnCAM1_PTZ, btnCAM1_Preview, btnCAM1_AUX]:
        i.SetVisible(cam1_is_enabled)

    cam2_is_enabled = utilities.config.get_value('devices/cam2/enabled', default_value=False,cast_as='boolean')
    for i in [btnCAM2_PTZ, btnCAM2_Preview, btnCAM2_AUX]:
        i.SetVisible(cam2_is_enabled)

    cam3_is_enabled = utilities.config.get_value('devices/cam3/enabled', default_value=False, cast_as='boolean')
    for i in [btnCAM3_PTZ, btnCAM3_Preview, btnCAM3_AUX]:
        i.SetVisible(cam3_is_enabled)

    # Hide the CAM3 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam3_is_enabled:
        # HIDE
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x87\x04\x00\x00\x00\x00') #MV Box3 Label (0xc87)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x00\x00') #MV Box3 Source (0xc84)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1a\x04\x00\x00\x00\x00') #MV Box3 Border (0x191a)

    else:
        # SHOW
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x87\x04\x00\x00\x00\x01') #MV Box3 Label (0xc87)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x84\x04\x00\x00\x03\xea') #MV Box3 Source (0xc84)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1a\x04\x00\x00\x00\x01') #MV Box3 Border (0x191a)

    cam4_is_enabled = utilities.config.get_value('devices/cam4/enabled', default_value=False, cast_as='boolean')
    for i in [btnCAM4_PTZ, btnCAM4_Preview, btnCAM4_AUX]:
        i.SetVisible(cam4_is_enabled)

    # Hide the CAM4 window on the multiview of the Carbonite switcher
    # We're just sending raw commands since we don't care about feedback on this, it does not
    # seem worth implementing this in the driver.
    if not cam4_is_enabled:
        # HIDE
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8e\x04\x00\x00\x00\x00') #MV Box4 Label (0xc8e)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8b\x04\x00\x00\x00\x00') #MV Box4 Source (0xc8b)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1b\x04\x00\x00\x00\x00') #MV Box4 Border (0x191b)

    else:
        # SHOW
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8e\x04\x00\x00\x00\x01') #MV Box4 Label (0xc8e)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x0c\x8b\x04\x00\x00\x03\xeb') #MV Box4 Source (0xc8b)
        devices.carbonite.Send(b'\xba\xd2\xac\xe5\x00\x10\x4a\x00\x08\x00\x19\x1b\x04\x00\x00\x00\x01') #MV Box4 Border (0x191b)


#end function (Initialize)


ActivePopup = None
def ShowPopup(PopupName):
    global ActivePopup
    devices.TouchPanel.ShowPopup(PopupName)
    ActivePopup = PopupName
#end function (ShowPopup)




@event(lstMainMenuButtons, 'Pressed')
def MainMenuButtonsPressed(button, state):
    DebugPrint('interface/MainMenuButtonsPressed', 'Main Menu Button Pressed: [{}]'.format(button.Name), 'Debug')

    if button is btnMainMenu:
        devices.Touchpanel.ShowPopup('POP - Main Menu')

    elif button is btnQuickButton1:
        execute_command(button, utilities.config.get_value(
            'interface/quickbuttons/button_1_function', default_value=None))

    elif button is btnQuickButton2:
        execute_command(button, utilities.config.get_value(
            'interface/quickbuttons/button_2_function', default_value=None))

    elif button is btnQuickButton3:
        execute_command(button, utilities.config.get_value(
            'interface/quickbuttons/button_3_function', default_value=None))

    elif button is btnQuickButton4:
        execute_command(button, utilities.config.get_value(
            'interface/quickbuttons/button_4_function', default_value=None))

#end function (MainMenuButtonsPressed)


@event(lstPlayListButtons, 'Pressed')
@event(lstPlaybackTransportButtons, 'Pressed')
def PlaybackButtonsPressed(button, state):

    #FIXME - this should eventually come from a configuration file construct
    PlaylistMap = {
        btnPlayback_Playlist1 : 'intro.m3u',
        btnPlayback_Playlist2 : 'music2.m3u',
        btnPlayback_Playlist3 : 'music3.m3u',
        btnPlayback_Playlist4 : 'music4.m3u',
        btnPlayback_Playlist5 : 'music5.m3u',
        btnPlayback_Playlist6 : 'outro.m3u'
    }

    if   button is btnPlayback_PLAY:
        devices.smd101.Set('Playback', 'Play')
        DebugPrint('interface/PlaybackButtonsPressed', 'Playback button activated', 'Debug')

    elif button is btnPlayback_PAUSE:
        devices.smd101.Set('Playback', 'Pause')
        DebugPrint('interface/PlaybackButtonsPressed', 'Pause button activated', 'Debug')

    elif button is btnPlayback_STOP:
        devices.smd101.Set('Playback', 'Stop')
        DebugPrint('interface/PlaybackButtonsPressed', 'Stop button activated', 'Debug')

    elif button in lstPlayListButtons:
        devices.smd101.Set('LoadPlaylistCommand ', PlaylistMap[button])
        DebugPrint('interface/PlaybackButtonsPressed', 'Loading playlist: [{}]'.format(PlaylistMap[button]), 'Debug')

#end function (PlaybackButtonsPressed)




@event(btnPlaybackControls, 'Pressed')
@event(lstPTZButtons, 'Pressed')
def PTZButtonsPressed(button, state):
    
    PopupMap = {
            btnCAM1_PTZ : 'POP - CAM1-Control',
            btnCAM2_PTZ : 'POP - CAM2-Control',
            btnCAM3_PTZ : 'POP - CAM3-Control',
            btnCAM4_PTZ : 'POP - CAM4-Control',
            btnPlaybackControls : 'POP - Playback Control'
        }
    DebugPrint('interface/PTZButtonsPressed', 'Button [{}] pressed. Loading popup: [{}]'.
               format(button.Name, PopupMap[button]), 'Debug')

    ShowPopup(PopupMap[button])
#end function (PTZButtonsPressed)


@event([btnMIX, btnCUT], 'Pressed')
def TransitionButtons(button, state):
    if button is btnMIX:
        devices.carbonite.Set('Auto', None)
        DebugPrint('interface/TransitionButtons', 'MIX Button pressed', 'Debug')

    elif button is btnCUT:
        devices.carbonite.Set('Cut', None)
        DebugPrint('interface/TransitionButtons', 'CUT Button pressed', 'Debug')

#end function (TransitionButtons)


@event(lstPreviewButtons, 'Pressed')
def PreviewButtonsPressed(button, state):
    
    PresetSource = {
        btnCAM1_Preview : 'Cam 1',
        btnCAM2_Preview : 'Cam 2',
        btnCAM3_Preview : 'Cam 3',
        btnCAM4_Preview : 'Cam 4',
        btnIN5_Preview  : 'HDMI 1',
        btnIN6_Preview  : 'HDMI 2'
    }

    devices.carbonite.Set('MLEPresetSource', PresetSource[button])
    DebugPrint('interface/PreviewButtonsPressed', 'Preset button pressed for input: [{}]'.
               format( PresetSource[button]), 'Debug')

#end function (PreviewButtonsPressed)


@event(lstAuxButtons, 'Pressed')
def AUXButtonsPressed(button, state):

    AUXSource = {
        btnCAM1_AUX     : 'Cam 1',
        btnCAM2_AUX     : 'Cam 2',
        btnCAM4_AUX     : 'Cam 3',
        btnCAM4_Preview : 'Cam 4',
        btnIN5_AUX      : 'HDMI 1',
    }

    devices.carbonite.Set('KeySource', AUXSource[button], {'Keyer': 1})
#end function (AUXButtonsPressed)


@event(btnPreview_KeyOFF, 'Pressed')
def btnPreview_KeyOFFPressed(button, state):
    devices.carbonite.Set('NextTransitionLayers', 'Off', {'Layer' : 'Key 1'})
    devices.carbonite.Set('NextTransitionLayers', 'Off', {'Layer' : 'Key 2'})
#endfunction (btnPreview_KeyOFFPressed)


@event([btnPreview_Key1, btnPreview_Key2], 'Pressed')
def KeyButtonsPressed(button, state):

    #FIXME - build and use a toggle helper function?

    if button is btnPreview_Key1:
        if devices.carbonite.ReadStatus('NextTransitionLayers', {'Layer': 'Key 1'}) == 'On':
            devices.carbonite.Set('NextTransitionLayers', 'Off', {'Layer': 'Key 1'})
        else:
            devices.carbonite.Set('NextTransitionLayers', 'On', {'Layer': 'Key 1'})

    elif button is btnPreview_Key2:
        if devices.carbonite.ReadStatus('NextTransitionLayers', {'Layer': 'Key 2'}) == 'On':
            devices.carbonite.Set('NextTransitionLayers', 'Off', {'Layer': 'Key 2'})
        else:
            devices.carbonite.Set('NextTransitionLayers', 'On', {'Layer': 'Key 2'})


@event(btnPreview_Key1and2, 'Pressed')
def btnPreview_Key1and2Pressed(button, state):
    pass

@event(btnBottomBar3, 'Pressed')
def btnBottomBar3Pressed(button, state):
    pass

@event(btnBottomBar4, 'Pressed')
def btnBottomBar4Pressed(button, state):
    devices.TouchPanel.ShowPage('No-Button View')

@event(btnBottomBar5, 'Pressed')
def btnBottomBar5Pressed(button, state):
    devices.TouchPanel.ShowPopup('POP - Options')

@event(btnBottomBar6, 'Pressed')
def btnBottomBar6Pressed(button, state):
    pass


@event([btnCloseNoButtonsA, btnCloseNoButtonsB], 'Pressed')
def btnCloseButtonsPressed(button, state):
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')



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

# FIXME - this needs to be controlled by the buttons/system state
def get_cam2_tilt_speed():
    return 10

# FIXME - this needs to be controlled by the buttons/system state
def get_cam2_pan_speed():
    return 10

# FIXME - this needs to be controlled by the buttons/system state
def get_cam2_zoom_speed():
    return 10


@event(lstCAM1_PresetBtns, 'Pressed')
@event(lstCAM1_PTZBtns, ['Pressed', 'Released'])
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
        pass

#end function (cam1_buttons_pressed_released)


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
lstCAM2_PTZBtns    = [btnCAM2_TiltUp, btnCAM2_TiltDown, btnCAM2_PanLeft, btnCAM2_PanRight,
                      btnCAM2_ZoomIn, btnCAM2_ZoomOut]
lstCAM2_PresetBtns = [btnCAM2_Preset1, btnCAM2_Preset2, btnCAM2_Preset3, btnCAM2_Preset4,
                      btnCAM2_Preset5, btnCAM2_Preset6, btnCAM2_Preset7, btnCAM2_Preset8]


@event(lstCAM2_PresetBtns, 'Pressed')
@event(lstCAM2_PTZBtns, ['Pressed', 'Released'])
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
            btnCAM2_Preset5: '5', btnCAM2_Preset6: '6', btnCAM2_Preset7: '7', btnCAM1_Preset8: '8'
        }
        devices.cam2.Set('PresetRecall', preset_btn_map[button])

    elif button in [btnCAM2_Speed1, btnCAM2_Speed2, btnCAM2_Speed3]:
        pass

#end function (cam2_buttons_pressed_released)


def execute_command(button, macro_string):
#    device:command:value
#    ui:popup:<name>
#    macro:<name>
    DebugPrint('execute_button_macro', 'Button: [{}] Running with: [{}]'.format(button.Name, macro_string), 'Debug')
#end function (execute_button_macro)