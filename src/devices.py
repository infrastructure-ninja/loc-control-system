from extronlib.device import ProcessorDevice, UIDevice
from extronlib import event
from extronlib.system import Wait, Timer

from helper_connectionhandler import GetConnectionHandler

from utilities import DummyDriver
from utilities import DebugPrint
import utilities

ControlProcessor = ProcessorDevice('ExtronProcessor')
TouchPanel = UIDevice('ExtronPanel')

import interface

device_objects = {}

from helper_systemstate import DeviceClass
system_states = DeviceClass()

def SystemStatesCallbackHandler(command, value, qualifier):
  #FIXME - this could be more compact and pythonic, when you get bored of everything else
  if command == 'CameraSpeed' and qualifier['Camera Number'] == 1:
    button_map = {
      'Slow': interface.btnCAM1_Speed1,
      'Medium': interface.btnCAM1_Speed2,
      'Fast': interface.btnCAM1_Speed3
    }

    for single_button in button_map.values():
      single_button.SetState(0)

    button_map[value].SetState(1)

  elif command == 'CameraSpeed' and qualifier['Camera Number'] == 2:
    button_map = {
      'Slow': interface.btnCAM2_Speed1,
      'Medium': interface.btnCAM2_Speed2,
      'Fast': interface.btnCAM2_Speed3
    }

    for single_button in button_map.values():
      single_button.SetState(0)

    button_map[value].SetState(1)

#end function (SystemStatesCallbackHandler)

system_states.SubscribeStatus('ActivePopup', None, SystemStatesCallbackHandler)
system_states.SubscribeStatus('CameraSpeed', None, SystemStatesCallbackHandler)


if utilities.config.get_value('devices/switcher/enabled', cast_as='boolean'):
  import ross_carbonite_solo_frame as CarboniteSolo109
  carbonite = GetConnectionHandler(
    CarboniteSolo109.EthernetClass(
      utilities.config.get_value('devices/switcher/ipaddress'),
      utilities.config.get_value('devices/switcher/port', cast_as='integer'),
      Model='Carbonite Black Solo 109'), 'ProductName')
else:
  carbonite = DummyDriver('Carbonite Black Solo 109')

device_objects.update({'carbonite': carbonite})


if utilities.config.get_value('devices/matrix/enabled', cast_as='boolean'):
  import driver_extr_matrix_DXPHD4k_Series_v1_3_3_0 as MatrixDriver
  matrix = GetConnectionHandler(
    MatrixDriver.EthernetClass(
      utilities.config.get_value('devices/matrix/ipaddress'),
      utilities.config.get_value('devices/matrix/port', cast_as='integer'),
      Model='DXP 88 HD 4K'), 'Temperature')
else:
  matrix = DummyDriver('Extron DXP 88 HD 4K Matrix')

device_objects.update({'matrix': matrix})


if utilities.config.get_value('devices/playback/enabled', cast_as='boolean'):
  import driver_extr_sm_SMD101_SMD202_v1_11_4_0 as SMD101Driver
  smd101 = GetConnectionHandler(
    SMD101Driver.SSHClass(
      utilities.config.get_value('devices/playback/ipaddress'),
      utilities.config.get_value('devices/playback/port', cast_as='integer'),
      Credentials=(
        utilities.config.get_value('devices/playback/username'),
        utilities.config.get_value('devices/playback/password'),
      )), 'Temperature')
else:
  smd101 = DummyDriver('Extron SMD101 Playback Unit')

device_objects.update({'smd101': smd101})


import driver_extr_sm_SMP_300_Series_v1_16_3_0 as SMP351Driver
smp351 = GetConnectionHandler(
    SMP351Driver.SerialClass(ControlProcessor, 'COM1', Baud=38400, Model='SMP 351'),
    'Alarm')
device_objects.update({'smp351': smp351})


if utilities.config.get_value('devices/playback/enabled', cast_as='boolean'):
  import driver_yama_dsp_TF1_TF5_TFRack_v1_0_0_0 as SoundboardDriver
  soundboard = GetConnectionHandler(
    SoundboardDriver.EthernetClass(
      utilities.config.get_value('devices/soundboard/ipaddress'),
      utilities.config.get_value('devices/soundboard/port', cast_as='integer'),
      Model='TF5'), 'Firmware')
else:
  soundboard = DummyDriver('Yamaha TF5 Sound Console')

device_objects.update({'soundboard': soundboard})


if utilities.config.get_value('devices/cam1/enabled', cast_as='boolean'):
  import driver_vadd_controller_QuickConnectUSB_v1_3_0_1 as CameraDriver
  cam1 = GetConnectionHandler(
    CameraDriver.EthernetClass(
      utilities.config.get_value('devices/cam1/ipaddress'),
      utilities.config.get_value('devices/cam1/port', cast_as='integer'),
      ), 'StreamingMode')
else:
  cam1 = DummyDriver('Vaddio USB Quick-Connect (CAM1)')

device_objects.update({'cam1': cam1})


if utilities.config.get_value('devices/cam2/enabled', cast_as='boolean'):
  import driver_vadd_controller_QuickConnectUSB_v1_3_0_1 as CameraDriver
  cam2 = GetConnectionHandler(
    CameraDriver.EthernetClass(
      utilities.config.get_value('devices/cam2/ipaddress'),
      utilities.config.get_value('devices/cam2/port', cast_as='integer'),
      ), 'StreamingMode')
else:
  cam2 = DummyDriver('Vaddio USB Quick-Connect (CAM2)')

device_objects.update({'cam2': cam2})

################################################



################################################
##### Ross Video Carbonite Black Frame 109 #####
################################################
def CarboniteReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/CarboniteReceivedDataHandler', 'Carbonite has been successfully connected', 'Info')

      for update in lstCarboniteStatusSubscriptions:
        if update == 'ConnectionStatus': continue  # ConnectionStatus does not support Updates
        carbonite.Update(update)

    elif value == 'Disconnected':
      DebugPrint('devices.py/CarboniteReceivedDataHandler', 'Carbonite has been disconnected from the system. Will attempt reconnection..', 'Error')

  elif command == 'MLEPresetSource':
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    mle_preset_source_map = {
      'Cam 1': interface.btnCAM1_Preview, 'Cam 2': interface.btnCAM2_Preview,
      'Cam 3': interface.btnCAM3_Preview, 'Cam 4': interface.btnCAM4_Preview,
      'HDMI 1': interface.btnIN5_Preview, 'HDMI 2': interface.btnIN6_Preview
      }

    # Set all buttons to normal state
    for input_name, button in mle_preset_source_map.items():
      button.SetState(0)

    # Set our selected button to slow flash
    if value in mle_preset_source_map:
      mle_preset_source_map[value].SetState(2)
      mle_preset_source_map[value].SetBlinking('Medium', [2,0])

  elif (command == 'KeySource') and qualifier['Keyer'] == 1:
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    keyer1_source_map = {
      'Cam 1': interface.btnCAM1_AUX, 'Cam 2': interface.btnCAM2_AUX,
      'Cam 3': interface.btnCAM3_AUX, 'Cam 4': interface.btnCAM4_AUX,
      'HDMI 1': interface.btnIN5_AUX
      }

    # Set all buttons to normal state
    for input_name, button in keyer1_source_map.items():
      button.SetState(0)

    # Set our selected button to slow flash
    if value in keyer1_source_map:
      keyer1_source_map[value].SetState(2)
      keyer1_source_map[value].SetBlinking('Medium', [2,0])


  # Set our "Key 1" and "Key 2" buttons to show what keys are active for the next transition
  # We use blinking (SetBlinking) to make sure they're noticeable on the screen.
  elif command == 'NextTransitionLayers':
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    carbonite.Update('KeyerStatus')

    #FIXME - this seems vestigial?
    # This dict map allows for easy adjustment of additional/different button states
    #keyer_button_state_map = {'Off': 0, 'On': 2}

    if ('Layer' in qualifier) and qualifier['Layer'] == 'Key 1':
      if value == 'On':
        interface.btnPreview_Key1.SetState(1)
        interface.btnPreview_Key1.SetBlinking('Fast', [0, 1])
      else:
        interface.btnPreview_Key1.SetState(0)

    elif ('Layer' in qualifier) and qualifier['Layer'] == 'Key 2':
      if value == 'On':
        interface.btnPreview_Key2.SetState(1)
        interface.btnPreview_Key2.SetBlinking('Fast', [0, 1])
      else:
        interface.btnPreview_Key2.SetState(0)

  elif command == 'KeyerStatus':
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    carbonite.Update('NextTransitionLayers')

  else:
    DebugPrint('devices.py/CarboniteReceivedDataHandler', 'Unhandled Carbonite Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

#end function (CarboniteReceivedDataHandler)

lstCarboniteStatusSubscriptions = ['ConnectionStatus', 'MLEBackgroundSource', 'MLEPresetSource',
                                'KeySource', 'AuxSource', 'ProductName','NextTransitionLayers',
                                'KeyerStatus']
for status in lstCarboniteStatusSubscriptions:
  carbonite.SubscribeStatus(status, None, CarboniteReceivedDataHandler)





################################################
########### Extron DXP HD 8x8 MATRIX ###########
################################################
def MatrixReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/MatrixReceivedDataHandler', 'Matrix switch has been successfully connected', 'Info')
    
    elif value == 'Disconnected':
      DebugPrint('devices.py/MatrixReceivedDataHandler', 'Matrix has been disconnected from the system. Will attempt reconnection..', 'Error')

  else:
    print('Received Matrix Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier))

#end function (MatrixReceivedDataHandler)

matrix.SubscribeStatus('ConnectionStatus', None, MatrixReceivedDataHandler)
matrix.SubscribeStatus('InputSignalStatus', None, MatrixReceivedDataHandler)
matrix.SubscribeStatus('InputTieStatus', None, MatrixReceivedDataHandler)
matrix.SubscribeStatus('OutputTieStatus', None, MatrixReceivedDataHandler)





################################################
######## Extron SMD 101 Playback Device ########
################################################
def SMD101ReceivedDataHandler(command, value, qualifier):

  DebugPrint('devices.py/SMD101ReceivedDataHandler',
             'Received SMD101 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/SMD101ReceivedDataHandler', 'SMD101 has been successfully connected', 'Info')

      for update in lstSMD101statusSubscriptions:
        if update == 'ConnectionStatus': continue # ConnectionStatus does not support Updates
        smd101.Update(update)

      tmrSMD101_poll_timer.Resume()

    elif value == 'Disconnected':
      DebugPrint('devices.py/SMD101ReceivedDataHandler', 'SMD101 has been disconnected from the system. Will attempt reconnection..', 'Error')
      tmrSMD101_poll_timer.Pause()

  elif command == 'CurrentClipLength':
    interface.lblPlayback_CurrentClipLength.SetText(value)

    timecode_in_seconds = utilities.ConvertTimecodeToSeconds(value)
    if timecode_in_seconds <= 0:
      interface.lvlPlayback_ClipPosition.SetVisible(False)
      interface.lvlPlayback_ClipPosition.SetRange(0, 1)
      interface.lblPlaybackTimeCodeRemaining.SetVisible(False)

    else:
      interface.lvlPlayback_ClipPosition.SetVisible(True)
      interface.lvlPlayback_ClipPosition.SetRange(0, timecode_in_seconds)
      interface.lblPlaybackTimeCodeRemaining.SetVisible(True)

  elif command == 'CurrentTimecode':
    interface.lblPlayback_CurrentTimeCode.SetText(value)

    timecode_in_seconds = utilities.ConvertTimecodeToSeconds(value)
    interface.lvlPlayback_ClipPosition.SetLevel(timecode_in_seconds)
    current_clip_length = utilities.ConvertTimecodeToSeconds(smd101.ReadStatus('CurrentClipLength'))

    remaining_seconds = current_clip_length - timecode_in_seconds
    interface.lblPlaybackTimeCodeRemaining.SetText('(-{})'.format(utilities.ConvertSecondsToTimeCode(remaining_seconds)))

  elif command == 'CurrentPlaylistTrack':
    interface.lblPlayback_CurrentPlaylist.SetText(value)

  elif command == 'CurrentSourceItem':
    interface.lblPlayback_CurrentSourceItem.SetText(value)

  elif command == 'Playback':
    value_text = {'Play': 'Playing', 'Pause': 'Paused', 'Stop': 'Stopped'}[value]
    interface.lblPlayback_CurrentState.SetText(value_text)

  else:
    DebugPrint('devices.py/SMD101ReceivedDataHandler',
               'Unhandled SMD101 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Warn')

#end function (SMD101ReceivedDataHandler)

lstSMD101statusSubscriptions = ['ConnectionStatus', 'Playback', 'CurrentTimecode', 'CurrentSourceItem',
                                'CurrentPlaylistTrack', 'CurrentTimecode', 'CurrentClipLength']

for status in lstSMD101statusSubscriptions:
  smd101.SubscribeStatus(status, None, SMD101ReceivedDataHandler)

def SMD101_poll_function(timer, count):
  smd101.Update('CurrentClipLength')
  smd101.Update('CurrentPlaylistTrack')
  smd101.Update('CurrentSourceItem')
  smd101.Update('CurrentTimecode')
#end function(SMD101_poll_function)


tmrSMD101_poll_timer = Timer(1, SMD101_poll_function)
tmrSMD101_poll_timer.Stop()


################################################
### Extron SMP351 Streading Media Processor ####
################################################
def SMP351ReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/SMP351ReceivedDataHandler', 'SMP351 has been successfully connected', 'Info')
    
    elif value == 'Disconnected':
      DebugPrint('devices.py/SMP351ReceivedDataHandler', 'SMP351 has been disconnected from the system. Will attempt reconnection..', 'Error')

  else:
    print('Received SMP351 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier))

#end function (SMD101ReceivedDataHandler)

smp351.SubscribeStatus('ConnectionStatus', None, SMP351ReceivedDataHandler)
smp351.SubscribeStatus('Alarm', None, SMP351ReceivedDataHandler)
smp351.SubscribeStatus('Record', None, SMP351ReceivedDataHandler)
smp351.SubscribeStatus('RTMPStream', None, SMP351ReceivedDataHandler)





################################################
############# Yamaha TF5 Soundboard ############
################################################
def SoundboardReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/SoundboardReceivedDataHandler', 'Yamaha TF5 soundboard has been successfully connected', 'Info')
    
    elif value == 'Disconnected':
      DebugPrint('devices.py/SoundboardReceivedDataHandler', 'Yamaha TF5 soundboard has been disconnected from the system. Will attempt reconnection..', 'Error')

  else:
    print('Received Yamaha TF5 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier))

#end function (SoundboardReceivedDataHandler)

soundboard.SubscribeStatus('ConnectionStatus', None, SoundboardReceivedDataHandler)
soundboard.SubscribeStatus('InputMute', None, SoundboardReceivedDataHandler)
soundboard.SubscribeStatus('OutputLevel', None, SoundboardReceivedDataHandler)
soundboard.SubscribeStatus('InputLevel', None, SoundboardReceivedDataHandler)





################################################
############### Vaddio Camera #1 ###############
################################################
def Cam1ReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/Cam1ReceivedDataHandler', 'Camera #1 has been successfully connected', 'Info')
    
    elif value == 'Disconnected':
      DebugPrint('devices.py/Cam1ReceivedDataHandler', 'Camera #1 has been disconnected from the system. Will attempt reconnection..', 'Error')

  else:
    print('Received CAM#1 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier))

#end function (Cam1ReceivedDataHandler)

cam1.SubscribeStatus('ConnectionStatus', None, Cam1ReceivedDataHandler)





################################################
############### Vaddio Camera #2 ###############
################################################
def Cam2ReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/Cam1ReceivedDataHandler', 'Camera #2 has been successfully connected', 'Info')
    
    elif value == 'Disconnected':
      DebugPrint('devices.py/Cam1ReceivedDataHandler', 'Camera #2 has been disconnected from the system. Will attempt reconnection..', 'Error')

  else:
    print('Received CAM#2 Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier))

#end function (Cam1ReceivedDataHandler)

cam2.SubscribeStatus('ConnectionStatus', None, Cam2ReceivedDataHandler)





def InitializeAll():
  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Carbonite switcher..', 'Debug')
  carbonite.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to DXP 88 HD device..', 'Debug')
  matrix.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to SMD101 device..', 'Debug')
  smd101.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to SMP351 device..', 'Debug')
  smp351.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Yamaha TF5 device..', 'Debug')
  soundboard.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Camera #1 device..', 'Debug')
  cam1.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Camera #2 device..', 'Debug')
  cam2.Connect()

# Set our system state for the starting camera movement speed
  system_states.Set('CameraSpeed',
                    utilities.config.get_value('devices/cam1/default_speed', default_value='Slow'),
                    {'Camera Number': 1})

  system_states.Set('CameraSpeed',
                    utilities.config.get_value('devices/cam2/default_speed', default_value='Slow'),
                    {'Camera Number': 2})

  system_states.Set('CameraSpeed',
                    utilities.config.get_value('devices/cam3/default_speed', default_value='Slow'),
                    {'Camera Number': 3})

  system_states.Set('CameraSpeed',
                    utilities.config.get_value('devices/cam4/default_speed', default_value='Slow'),
                    {'Camera Number': 4})

