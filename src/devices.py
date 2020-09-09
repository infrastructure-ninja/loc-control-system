#from extronlib.interface import (CircuitBreakerInterface, ContactInterface,
#    DigitalInputInterface, DigitalIOInterface, EthernetClientInterface,
#    EthernetServerInterfaceEx, FlexIOInterface, IRInterface, PoEInterface,
#    RelayInterface, SerialInterface, SWACReceptacleInterface, SWPowerInterface,
#    VolumeInterface)
#from extronlib.ui import Button, Knob, Label, Level, Slider
#from extronlib.system import Clock, MESet, Timer, Wait

from extronlib.device import ProcessorDevice, UIDevice
from extronlib import event, Version
from extronlib.system import Wait

from utilities import DebugPrint


ControlProcessor = ProcessorDevice('ExtronProcessor')
#TouchPanel = UIDevice('ExtronPanel')


import ross_carbonite_solo_frame as CarboniteSolo109
carbonite = CarboniteSolo109.EthernetClass('172.16.200.220', 5253, Model='Carbonite Black Solo 109')

#import driver_extr_matrix_DXPHD4k_Series_v1_3_3_0 as MatrixDriver
#matrix = MatrixDriver.EthernetClass('172.16.200.254', 23, Model='DXP 88 HD 4K')

#import driver_extr_sm_SMD101_SMD202_v1_11_4_0 as SMD101Driver
#smd101 = SMD101Driver.SSHClass('172.16.200.253', 22023, Credentials=('admin','extron'))

#import driver_extr_sm_SMP_300_Series_v1_16_3_0 as SMP351Driver
#smp351 = SMP351Driver.SerialClass(ControlProcessor, 'COM1', Baud=38400, Model='SMP 351')

#import driver_yama_dsp_TF1_TF5_TFRack_v1_0_0_0 as SoundboardDriver
#soundboard = SoundboardDriver.EthernetClass('172.16.200.5', 49280, Model='TF5')

#import driver_vadd_controller_QuickConnectUSB_v1_3_0_1 as CameraDriver
#cam1 = CameraDriver.EthernetClass('172.16.200.247', 23)
#cam2 = CameraDriver.EthernetClass('172.16.200.248', 23)


#from helper_connectionhandler import GetConnectionHandler


def ConnectCarbonite():
  result = carbonite.Connect(timeout=10)
  if result != 'Connected':
    DebugPrint('devices.py/ConnectCarbonite', 'Not connected, retrying again in 10 seconds..', 'Error')
    carboniteReconnectWait.Restart()


@event(carbonite, ['Connected', 'Disconnected'])
def CarbonitePhysicalConnectionEvent(interface, state):
  if state == 'Connected':
    DebugPrint('devices.py/CarbonitePhysicalConnectionEvent', 'Carbonite has been successfully connected', 'Info')
    carbonite.SendHandshake()
    carboniteReconnectWait.Cancel()

  elif state == 'Disconnected':
    DebugPrint('devices.py/CarbonitePhysicalConnectionEvent', 'Carbonite has been disconnected from the system. Attempting to reconnect..', 'Error')
    carbonite.Disconnect()
    carboniteReconnectWait.Restart()


carboniteReconnectWait = Wait(10, ConnectCarbonite)


def CarboniteReceivedDataHandler(command, value, qualifier):
  print('Received stuff: [{0}] [{1}] [{2}]'.format(command, value, qualifier))





carbonite.SubscribeStatus('ConnectionStatus', None, CarboniteReceivedDataHandler)
carbonite.SubscribeStatus('MLEBackgroundSource', None, CarboniteReceivedDataHandler)
carbonite.SubscribeStatus('MLEPresetSource', None, CarboniteReceivedDataHandler)
carbonite.SubscribeStatus('KeySource', None, CarboniteReceivedDataHandler)
carbonite.SubscribeStatus('AuxSource', None, CarboniteReceivedDataHandler)
carbonite.SubscribeStatus('ProductName', None, CarboniteReceivedDataHandler)





def InitializeAll():
    ConnectCarbonite()

    carbonite.Update('ProductName')