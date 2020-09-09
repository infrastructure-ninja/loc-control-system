from extronlib import event
from extronlib.ui import Button, Label  #, Level, Slider
from extronlib.system import Wait

import devices
from utilities import DebugPrint


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
lstPreviewButtons = [btnCAM1_Preview, btnCAM2_Preview, btnCAM3_Preview, btnCAM4_Preview, btnIN5_Preview, btnIN6_Preview]


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

def Initialize():
    devices.TouchPanel.ShowPage('Main Page')
    devices.TouchPanel.ShowPopup('POP - Default Home Popup')



@event(lstPTZButtons, 'Pressed')
def PTZButtonsPressed(button, state):
    if   button is btnCAM1_PTZ:
        devices.TouchPanel.ShowPopup('POP - CAM1-Control')
        
    elif button is btnCAM2_PTZ:
        devices.TouchPanel.ShowPopup('POP - CAM2-Control')
        
    elif button is btnCAM3_PTZ:
        devices.TouchPanel.ShowPopup('POP - CAM3-Control')
        
    elif button is btnCAM4_PTZ:
        devices.TouchPanel.ShowPopup('POP - CAM4-Control')


@event(btnPlaybackControls, 'Pressed')
def btnPlaybackControlsPressed(button, state):
    devices.TouchPanel.ShowPopup('POP - Playback Control')


@event([btnMIX, btnCUT], 'Pressed')
def TransitionButtons(button, state):
    if button is btnMIX:
        devices.carbonite.Set('Auto', None)

    elif button is btnCUT:
        devices.carbonite.Set('Cut', None)


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

    devices.carbonite.Set('MLEPresetSource', PresetSource)


    if   button is btnCAM1_Preview:
        devices.carbonite.Set('MLEPresetSource', 'Cam 1')
    
    elif button is btnCAM2_Preview:
        devices.carbonite.Set('MLEPresetSource', 'Cam 2')

    elif button is btnCAM3_Preview:
        devices.carbonite.Set('MLEPresetSource', 'Cam 3')

    elif button is btnCAM4_Preview:
        devices.carbonite.Set('MLEPresetSource', 'Cam 4')

    elif button is btnIN5_Preview:
        devices.carbonite.Set('MLEPresetSource', 'HDMI 1')

    elif button is btnIN6_Preview:
        devices.carbonite.Set('MLEPresetSource', 'HDMI 2')


@event(lstAuxButtons, 'Pressed')
def AUXButtonsPressed(button, state):
    if   button is btnCAM1_AUX:
        pass
        
    elif button is btnCAM2_AUX:
        pass
        
    elif button is btnCAM3_AUX:
        pass
        
    elif button is btnCAM4_AUX:
        pass
        
    elif button is btnIN5_AUX:
        pass

@event(btnPreview_KeyOFF, 'Pressed')
def btnPreview_KeyOFFPressed(button, state):
    pass

@event(btnPreview_Key1, 'Pressed')
def btnPreview_Key1Pressed(button, state):
    pass

@event(btnPreview_Key2, 'Pressed')
def btnPreview_Key2Pressed(button, state):
    pass

@event(btnPreview_Key1and2, 'Pressed')
def btnPreview_Key1and2Pressed(button, state):
    pass


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