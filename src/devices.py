from extronlib.device import ProcessorDevice, UIDevice
from extronlib import event
from extronlib.system import Wait, Timer

from helper_connectionhandler import GetConnectionHandler

from utilities import DebugPrint
import utilities

ControlProcessor = ProcessorDevice('ExtronProcessor')
TouchPanel = UIDevice('ExtronPanel')

import interface


import ross_carbonite_solo_frame as CarboniteSolo109
carbonite = GetConnectionHandler(
    CarboniteSolo109.EthernetClass('172.16.200.220', 5253, Model='Carbonite Black Solo 109'),
    'ProductName')

import driver_extr_matrix_DXPHD4k_Series_v1_3_3_0 as MatrixDriver
matrix = GetConnectionHandler(
    MatrixDriver.EthernetClass('172.16.200.254', 23, Model='DXP 88 HD 4K'),
    'Temperature')

import driver_extr_sm_SMD101_SMD202_v1_11_4_0 as SMD101Driver
smd101 = GetConnectionHandler(
    SMD101Driver.SSHClass('172.16.200.253', 22023, Credentials=('admin','extron')),
    'Temperature')

import driver_extr_sm_SMP_300_Series_v1_16_3_0 as SMP351Driver
smp351 = GetConnectionHandler(
    SMP351Driver.SerialClass(ControlProcessor, 'COM1', Baud=38400, Model='SMP 351'),
    'Alarm')

import driver_yama_dsp_TF1_TF5_TFRack_v1_0_0_0 as SoundboardDriver
soundboard = GetConnectionHandler(
    SoundboardDriver.EthernetClass('172.16.200.5', 49280, Model='TF5'),
    'Firmware')

import driver_vadd_controller_QuickConnectUSB_v1_3_0_1 as CameraDriver
cam1 = GetConnectionHandler(CameraDriver.EthernetClass('172.16.200.247', 23), 'StreamingMode')
cam2 = GetConnectionHandler(CameraDriver.EthernetClass('172.16.200.248', 23), 'StreamingMode')



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

    else:
      interface.lvlPlayback_ClipPosition.SetVisible(True)
      interface.lvlPlayback_ClipPosition.SetRange(0, timecode_in_seconds)

  elif command == 'CurrentTimecode':
    interface.lblPlayback_CurrentTimeCode.SetText(value)

    timecode_in_seconds = utilities.ConvertTimecodeToSeconds(value)
    interface.lvlPlayback_ClipPosition.SetLevel(timecode_in_seconds)

  elif command == 'CurrentPlaylistTrack':
    interface.lblPlayback_CurrentPlaylist.SetText(value)

  elif command == 'CurrentSourceItem':
    interface.lblPlayback_CurrentSourceItem.SetText(value)

  elif command == 'Playback':
    interface.lblPlayback_CurrentState.SetText(value)

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
