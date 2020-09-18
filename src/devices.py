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

from extronlib.device import ProcessorDevice, UIDevice
from extronlib.system import Timer

from helper_connectionhandler import GetConnectionHandler
from helper_systemstate import DeviceClass

from utilities import DummyDriver
from utilities import DebugPrint
import utilities

ControlProcessor = ProcessorDevice('ExtronProcessor')
TouchPanel = UIDevice('ExtronPanel')

import interface

# This dictionary will store all of our device objects, so they can be accessed
# later via our "preset/macro" mechanism.
device_objects = {}

# "system_states" is a custom driver module that provides a way to store various
# system states and trigger callbacks when they change.
system_states = DeviceClass()

def SystemStatesCallbackHandler(command, value, qualifier):
  if command == 'KeyOnPreview':
    DebugPrint('devices.py/SystemStatesCallbackHandler',
               '[{}] [{}] [{}]'.format(command, value, qualifier), 'Trace')

    if qualifier['Keyer'] == 1:
      if value == 'On':
        interface.btnPreview_Key1.SetState(1)
        interface.btnPreview_Key1.SetBlinking('Fast', [0, 1])
      else:
        interface.btnPreview_Key1.SetState(0)

    elif qualifier['Keyer'] == 2:
      if value == 'On':
        interface.btnPreview_Key2.SetState(1)
        interface.btnPreview_Key2.SetBlinking('Fast', [0, 1])
      else:
        interface.btnPreview_Key2.SetState(0)


  # FIXME - this could be more compact and pythonic, when you get bored of everything else
  elif command == 'CameraSpeed' and qualifier['Camera Number'] == 1:
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
system_states.SubscribeStatus('KeyOnPreview', None, SystemStatesCallbackHandler)


if utilities.config.get_value('devices/switcher/enabled', default_value=False, cast_as='boolean'):
  import driver_ross_carboniteblacksolo_v1_0_0 as CarboniteSolo109
  carbonite = GetConnectionHandler(
    CarboniteSolo109.EthernetClass(
      utilities.config.get_value('devices/switcher/ipaddress'),
      utilities.config.get_value('devices/switcher/port', default_value=5253, cast_as='integer'),
      Model='Carbonite Black Solo 109'), 'ProductName')

  if utilities.config.get_value('devices/switcher/tally_enabled', default_value=False, cast_as='boolean'):
    import driver_tslumd_31 as TallyDriver
    tally = TallyDriver.EthernetClass(
      utilities.config.get_value('devices/switcher/tally_port', default_value=5728, cast_as='integer')
    )

  else:
    tally = DummyDriver('TSL UMD Tally Device')


else:
  carbonite = DummyDriver('Carbonite Black Solo 109')
  tally = DummyDriver('TSL UMD Tally Device')

device_objects.update({'carbonite': carbonite})
device_objects.update({'tally': tally})

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
##### Ross Video Carbonite Black Solo Frame 109 #####
################################################
def CarboniteReceivedDataHandler(command, value, qualifier):

  if command == 'ConnectionStatus':
    if   value == 'Connected':
      DebugPrint('devices.py/CarboniteReceivedDataHandler', 'Carbonite has been successfully connected', 'Info')

      for update in lstCarboniteStatusSubscriptions:
        if update == 'ConnectionStatus': continue  # ConnectionStatus does not support Updates
        DebugPrint('devices.py/CarboniteReceivedDataHandler',
                   'Updating status for command: [{}]'.format(update), 'Trace')

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


  elif command == 'NextTransitionLayers':
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    carbonite.Update('KeyOnPreview')

  elif command == 'KeyerStatus':
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    carbonite.Update('KeyOnPreview')

  # Set our "Key 1" and "Key 2" buttons to show what keys are active for the next transition
  # We use blinking (SetBlinking) to make sure they're noticeable on the screen.
  elif command == 'KeyOnPreview':
    DebugPrint('devices.py/CarboniteReceivedDataHandler',
                'Received Carbonite Driver Update: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Debug')

    keyer_button = {1: interface.btnPreview_Key1, 2:  interface.btnPreview_Key2}[qualifier['Keyer']]

    if value == 'On':
      keyer_button.SetState(1)
      keyer_button.SetBlinking('Fast', [0,1])

    else:
      keyer_button.SetState(0)

  else:
    DebugPrint('devices.py/CarboniteReceivedDataHandler', 'Unhandled Carbonite Driver Data: [{0}] [{1}] [{2}]'.format(command, value, qualifier), 'Trace')

#end function (CarboniteReceivedDataHandler)

lstCarboniteStatusSubscriptions = ['ConnectionStatus', 'MLEBackgroundSource', 'MLEPresetSource',
                                'KeySource', 'AuxSource', 'ProductName','NextTransitionLayers',
                                'KeyerStatus', 'KeyOnPreview']
for status in lstCarboniteStatusSubscriptions:
  carbonite.SubscribeStatus(status, None, CarboniteReceivedDataHandler)


def TallyReceivedDataHandler(command, value, qualifier):
  DebugPrint('devices.py/TallyReceivedDataHandler', 'Tally Data Received: -> [{}] [{}] [{}]'.format(
    command, value, qualifier), 'Trace')

  if qualifier['Input'] == 'Cam 1':
    temp_button_list = interface.lstCAM1_PTZBtns + interface.lstCAM1_PresetBtns + interface.lstCAM1_SpeedBtns

    if (value == 'Off') or (value == 'Green'):
      interface.btnCAM1_OnAir.SetState(0)
      interface.btnCAM1_OnAir.SetVisible(False)

      for single_button in temp_button_list:
        single_button.SetEnable(True)
        single_button.SetState(0)

    elif (value == 'Red') or (value == 'Red & Green'):
      interface.btnCAM1_OnAir.SetBlinking('Fast', [0, 1])
      interface.btnCAM1_OnAir.SetVisible(True)

      for single_button in temp_button_list:
        single_button.SetEnable(False)
        single_button.SetState(2)

  elif qualifier['Input'] == 'Cam 2':
    temp_button_list = interface.lstCAM2_PTZBtns + interface.lstCAM2_PresetBtns + interface.lstCAM2_SpeedBtns

    if (value == 'Off') or (value == 'Green'):
      interface.btnCAM2_OnAir.SetState(0)
      interface.btnCAM2_OnAir.SetVisible(False)

      for single_button in temp_button_list:
        single_button.SetEnable(True)
        single_button.SetState(0)

    elif (value == 'Red') or (value == 'Red & Green'):
      interface.btnCAM2_OnAir.SetBlinking('Fast', [0, 1])
      interface.btnCAM2_OnAir.SetVisible(True)

      for single_button in temp_button_list:
        single_button.SetEnable(False)
        single_button.SetState(2)

  if qualifier['Input'] == 'HDMI 2':
    if (value == 'Off') or (value == 'Green'):
      interface.btnPlayback_OnAir.SetState(0)
      interface.btnPlayback_OnAir.SetVisible(False)

    elif (value == 'Red') or (value == 'Red & Green'):
      interface.btnPlayback_OnAir.SetBlinking('Fast', [0, 1])
      interface.btnPlayback_OnAir.SetVisible(True)

#end function (TallyReceivedDataHandler)

tally.SubscribeStatus('Tally', None, TallyReceivedDataHandler)


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

  result = tally.StartListen()
  if result == 'Listening':
    DebugPrint('devices.py/InitializeAll', 'TSL UMD Tally Driver is listening on {}/TCP..'.format(tally.IPPort), 'Info')

  else:
    DebugPrint('devices.py/InitializeAll', 'TSL UMD Tally Driver is NOT LISTENING! Return status was: [{}]'.format(result), 'Error')


  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to DXP 88 HD device..', 'Info')
  matrix.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to SMD101 device..', 'Info')
  smd101.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to SMP351 device..', 'Info')
  smp351.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Yamaha TF5 device..', 'Info')
  soundboard.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Camera #1 device..', 'Info')
  cam1.Connect()

  DebugPrint('devices.py/InitializeAll', 'Attempting to connect to Camera #2 device..', 'Info')
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

