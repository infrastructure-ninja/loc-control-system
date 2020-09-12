from extronlib import event
from extronlib.ui import Button, Label, Level  #,  Slider
from extronlib.system import Wait

import devices
from utilities import DebugPrint
import utilities

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

btnBottomBar1 = Button(devices.TouchPanel, 16)
btnPlaybackControls = Button(devices.TouchPanel, 47)
btnBottomBar4 = Button(devices.TouchPanel, 59)
btnBottomBar5 = Button(devices.TouchPanel, 60)
btnBottomBar6 = Button(devices.TouchPanel, 99)
btnBottomBar3 = Button(devices.TouchPanel, 110)
btnBottomBar2 = Button(devices.TouchPanel, 111)

btnPreview_KeyOFF = Button(devices.TouchPanel, 106)
btnPreview_Key1 = Button(devices.TouchPanel, 108)
btnPreview_Key2 = Button(devices.TouchPanel, 182)
btnPreview_Key1and2 = Button(devices.TouchPanel, 183)

btnCloseNoButtonsA = Button(devices.TouchPanel, 11)
btnCloseNoButtonsB = Button(devices.TouchPanel, 115)


### PLAYBACK CONTROLS (and LABELS) ###
lblPlayback_CurrentClipLength = Label(devices.TouchPanel, 127)
lblPlayback_CurrentTimeCode   = Label(devices.TouchPanel, 128)
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


def InitializeAll():
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')

    lvlPlayback_ClipPosition.SetVisible(False) # We want this hidden until it's shown


    #FIXME - this should come from a configuration file
    btnPlayback_Playlist1.SetText('INTRO')
    btnPlayback_Playlist2.SetText('Playlist #2')
    btnPlayback_Playlist3.SetText('Playlist #3')
    btnPlayback_Playlist4.SetText('Playlist #4')
    btnPlayback_Playlist5.SetText('Playlist #5')
    btnPlayback_Playlist6.SetText('OUTRO')
#end function (Initialize)


ActivePopup = None
def ShowPopup(PopupName):
    global ActivePopup
    devices.TouchPanel.ShowPopup(PopupName)
    ActivePopup = PopupName
#end function (ShowPopup)


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

    devices.carbonite.Set('MLEPresetSource', AUXSource[button])
#end function (AUXButtonsPressed)


@event(btnPreview_KeyOFF, 'Pressed')
def btnPreview_KeyOFFPressed(button, state):
    devices.carbonite.Set('NextTransitionLayers', 'Off', {'Layer' : 'Key 1'})
    devices.carbonite.Set('NextTransitionLayers', 'Off', {'Layer' : 'Key 2'})
#endfunction (btnPreview_KeyOFFPressed)


@event(btnPreview_Key1, 'Pressed')
def btnPreview_Key1Pressed(button, state):
    devices.carbonite.Set('NextTransitionLayers', 'On', {'Layer' : 'Key 1'})

@event(btnPreview_Key2, 'Pressed')
def btnPreview_Key2Pressed(button, state):
    devices.carbonite.Set('NextTransitionLayers', 'On', {'Layer' : 'Key 2'})

@event(btnPreview_Key1and2, 'Pressed')
def btnPreview_Key1and2Pressed(button, state):
    devices.carbonite.Set('NextTransitionLayers', 'On', {'Layer' : 'Key 1'})
    devices.carbonite.Set('NextTransitionLayers', 'On', {'Layer' : 'Key 2'})


@event(btnBottomBar1, 'Pressed')
def btnBottomBar1Pressed(button, state):
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')

@event(btnBottomBar2, 'Pressed')
def btnBottomBar2Pressed(button, state):
    devices.TouchPanel.ShowPopup('POP - Service Presets')

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


@event(lstCAM1_PresetBtns, 'Pressed')
@event(lstCAM1_PTZBtns, ['Pressed', 'Released'])
def cam1_buttons_pressed_released(button, state):

    DebugPrint('interface/Cam1ButtonsPressedAndReleased', 'CAM1 PTZ button: [{}] was [{}]'.
               format(button.Name, state), 'Debug')

    # Each button map returns a dictionary for the 'Pressed' state and the 'Released' state,
    # inside each dictionary is a tuple that contains the 'command', the 'value', and the
    # proper qualifier to pass to our device driver class.
    # While it might look really complex, it reduces redundant 'if/elif' blocks and removes the
    # need for tons of additional lines of code!
    #
    ptz_button_map = {
        btnCAM1_TiltUp  : {'Pressed': ('Tilt', 'Up', 'Tilt Speed'),   'Released': ('Tilt', 'Stop', 'Tilt Speed')},
        btnCAM1_TiltDown: {'Pressed': ('Tilt', 'Down', 'Tilt Speed'), 'Released': ('Tilt', 'Stop', 'Tilt Speed')},
        btnCAM1_PanLeft : {'Pressed': ('Pan', 'Left', 'Pan Speed'),   'Released': ('Pan', 'Stop', 'Pan Speed')},
        btnCAM1_PanRight: {'Pressed': ('Pan', 'Right', 'Pan Speed'),  'Released': ('Pan', 'Stop', 'Pan Speed')},
        btnCAM1_ZoomIn  : {'Pressed': ('Zoom', 'In', 'Zoom Speed'),   'Released': ('Zoom', 'Stop', 'Zoom Speed')},
        btnCAM1_ZoomOut : {'Pressed': ('Zoom', 'Out', 'Zoom Speed'),  'Released': ('Zoom', 'Stop', 'Zoom Speed')}
    }

    if button in lstCAM1_PTZBtns:
        command = ptz_button_map[button][state][0]
        value = ptz_button_map[button][state][1]
        qualifier_text = ptz_button_map[button][state][2]

        #FIXME - this needs to be controlled by the buttons/system state
        qualifier = {qualifier_text: '1'}

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

#end function (Cam1ButtonsPressedAndReleased)

