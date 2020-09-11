from extronlib.interface import EthernetClientInterface
from extronlib.system import ProgramLog
from extronlib.system import Wait

import re
from struct import pack, unpack

class DeviceClass:

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 5
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {}

        self.HandshakeCompleted = False
        self.__KeepAliveSeconds = 5
        self.KeepAliveTimerObject = None
        
        # These video source IDs are used in a lot of the switcher commands.
        # Putting them here keeps future updates easier.
        self.VideoSourceIDsByName = {
            'Black'     :      0,
            'No Source' :      9,
            'Background':     10,
            'Cam 1'     :   1000,
            'Cam 2'     :   1001,
            'Cam 3'     :   1002,
            'Cam 4'     :   1003,
            'Cam 5'     :   1004,
            'Cam 6'     :   1005,
            'HDMI 1'    :   1006,
            'HDMI 2'    :   1007,
            'HDMI 3'    :   1008,
            'ClipPlyr'  :   1009,
            'M1'        :    100,
            'M2'        :    101,
            'M3'        :    102,
            'M4'        :    103,
            'ME1MW'     :  11004,
            'ME1MWA'    :  11005,
            'Aux 1'     :   9000,
            'Aux 2'     :   9001,
            'Aux 3'     :   9002,
            'Aux 4'     :   9003,
            'Aux 5'     :   9004,
            'Aux 6'     :   9005,
            'Aux 7'     :   9006,
            'Aux 8'     :   9007,
            'Aux 9'     :   9008,
            'Aux 10'    :   9009,
            'Aux 11'    :   9010,
            'Aux 12'    :   9011,
            'Aux 13'    :   9012,
            'Aux 14'    :   9013,
            'Aux 15'    :   9014,
            'Aux 16'    :   9015,
            'MinME1'    :  25000,
            'MinME2'    :  25100,
            'ME1Bg'     :  60000,
            'ME1Pst'    :  60001,
            'ME1K1V'    :  60010,
            'ME1K1A'    :  60011,
            'ME1K2V'    :  60020,
            'ME1K2A'    :  60021,
            'ME1K3V'    :  60030,
            'ME1K3A'    :  60031,
            'ME1K4V'    :  60040,
            'ME1K4A'    :  60041,
            'MM1Bg'     :  80000,
            'MM1Pst'    :  80001,
            'MM1K1V'    :  80010,
            'MM1K2V'    :  80020,
            'MM1K2A'    :  80021,
            'MM2Bg'     :  80210,
            'MM2Pst'    :  80211,
            'MM2K1V'    :  80220,
            'MM2K2V'    :  80230,
            'MM2K2A'    :  80231,
            'MS1Bg '    : 100000,
            'MS1Pst'    : 100001,
            'MS1K1V'    : 100010,
            'MS1K2V'    : 100020,
            'MS1K2A'    : 100021
        }

        # This creates an reverse-lookup dictionary for looking up the 
        # "friendly name" of the video source from its ID number.
        self.VideoSourceNamesByID = {}
        for key, value in self.VideoSourceIDsByName.items():
            self.VideoSourceNamesByID.update ( {value : key } )


        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'ProductName': {'Status': {}},

            #'RunMacro': {'Status': {}},
            #'Transition': {'Parameters': ['Transition Style', 'Next Transition', 'Style', 'Background', 'Key 1', 'Key 2', 'Key 3', 'Key 4'], 'Status': {}},

            'Auto': {'Status': {}},
            'Cut': {'Status': {}},
            'KeySource': {'Parameters': ['Keyer'], 'Status': {}},
            'KeyerStatus': {'Parameters': ['Keyer'], 'Status': {}},
            'AuxSource': {'Parameters': ['Aux Bus'], 'Status': {}},
            'MLEBackgroundSource': {'Parameters': ['Source'], 'Status': {}},
            'MLEPresetSource': {'Parameters': ['Source'], 'Status': {}},
            #'NextTransition': {'Parameters': ['Style','Background', 'Key 1', 'Key 2', 'Key 3', 'Key4'], 'Status': {}},
            'NextTransitionLayers': {'Parameters': ['Layer'], 'Status': {}},
            
            
            #'ClipProgress': {'Status': {}},
        }


        if self.Unidirectional == 'False':
            #self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00\xca\x00\x08\x00\x61\x62'), self.__MatchClipProgress, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca]\x00\x08\x00\x0e\x06\x04([\x00-\xFF]{4})'), self.__MatchMLEBackgroundSource, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca]\x00\x08\x00\x0e\x07\x04([\x00-\xFF]{4})'), self.__MatchMLEPresetSource, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca]\x00\x08\x00(\x0d[\xf6\xf7\xf8\xf9])\x04([\x00-\xFF]{4})'), self.__MatchKeySource, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca]\x00\x08\x00(\x0D\xFE|\x0D\xFF|\x0E\x00|\x0E\x01|\x0E\x02|\x0E\x03)\x04([\x00-\xFF]{4})'), self.__MatchAuxSource, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca]\x00\x08\x00(\x09\x92|\x09\x96|\x09\x9a|\x09\x9e)\x04([\x00-\xFF]{4})'), self.__MatchKeyerStatus, None)

            #self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca]\x00\x08\x00(\x09\x8d|\x09\x95|\x09\x99|\x09\x9d|\x09\xa1)\x04([\x00-\xFF]{4})'), self.__MatchNextTransitionLayers, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00\xcd\x00\x0a\x00\x09\x90(\x00[\x00-\x04])\x04([\x00-\xFF]{4})'), self.__MatchNextTransitionLayers, None)
                       
            #self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca][\x00-\xFF][\x00-\xFF]\x00\x1e\xe6([\x00-\xFF])([\x00-\xFF]{0,254})\x00(\xba\xd2){0,1}'), self.__MatchProductName, None)
            self.AddMatchString(re.compile(b'\xba\xd2\xac\xe5\x10\x00[\xc9\xca][\x00-\xFF][\x00-\xFF]\x00\x1e\xe6([\x00-\xFF])([\x20-\x7f]*?)\x00(\xba\xd2){0,1}'), self.__MatchProductName, None)

    def SetAuto(self, value, qualifier):
        AutoCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, 0x98D, 0x04, 0x1)
        self.__SetHelper('Auto', AutoCmdString, value, qualifier)

    def SetCut(self, value, qualifier):
        CutCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, 0x98C, 0x04, 0x1)
        self.__SetHelper('Auto', CutCmdString, value, qualifier)



    def SetMLEBackgroundSource(self, value, qualifier):
                
        try:
            MLEBackgroundSourceValue = self.VideoSourceIDsByName[value]
        
        except KeyError:
            ProgramLog('[SetMLEBackgroundSource] Invalid source name specified.', 'error')

        MLEBackgroundSourceOID = 0xE06
        
        SetMLEBackgroundSourceCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, MLEBackgroundSourceOID, 0x04, MLEBackgroundSourceValue)
        self.__SetHelper('MLEBackgroundSource', SetMLEBackgroundSourceCmdString, value, qualifier)

    def UpdateMLEBackgroundSource(self, value, qualifier):
        
        oidMLEBackgroundSource = 0xE06
        UpdateMLEBackgroundSourceCmdString =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, oidMLEBackgroundSource)

        self.__UpdateHelper('MLEBackgroundSource', UpdateMLEBackgroundSourceCmdString, value, qualifier)


    def __MatchMLEBackgroundSource(self, match, tag):
        
        value = unpack('>l', match.group(1))[0]
        if value in self.VideoSourceNamesByID:
            self.WriteStatus('MLEBackgroundSource', self.VideoSourceNamesByID[value])
        else:
            self.WriteStatus('MLEBackgroundSource', 'Unknown Source: {}'.format(value))


    def SetMLEPresetSource(self, value, qualifier):
                
        try:
            MLEPresetSourceValue = self.VideoSourceIDsByName[value]
        
        except KeyError:
            ProgramLog('[SetMLEPresetSource] Invalid source name specified.', 'error')
            return False

        MLEPresetSourceOID = 0xE07
        
        SetMLEPresetSourceCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, MLEPresetSourceOID, 0x04, MLEPresetSourceValue)
        self.__SetHelper('MLEPresetSource', SetMLEPresetSourceCmdString, value, qualifier)

    def UpdateMLEPresetSource(self, value, qualifier):
        
        MLEPresetSourceOID = 0xE07
        UpdateMLEPresetSourceCmdString =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, MLEPresetSourceOID)

        self.__UpdateHelper('MLEPresetSource', UpdateMLEPresetSourceCmdString, value, qualifier)

    def __MatchMLEPresetSource(self, match, tag):
        
        value = unpack('>l', match.group(1))[0]
        if value in self.VideoSourceNamesByID:
            self.WriteStatus('MLEPresetSource', self.VideoSourceNamesByID[value])
        else:
            self.WriteStatus('MLEPresetSource', 'Unknown Source: {}'.format(value))



    def SetKeySource(self, value, qualifier):

        try:
            KeyVideoSource = self.VideoSourceIDsByName[value]
        except:
            ProgramLog('[SetKeySource] Invalid source name specified.', 'error')
            return False

        try:
            DestinationKeyerOID = {1: 0xDF6, 2: 0xDF7, 3: 0xDF8, 4: 0xDF9}[qualifier['Keyer']]
        except KeyError:
            ProgramLog('[SetKeySource] Invalid destination Keyer number specified.', 'error')
            return False

        SetKeyVideoSourceCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, DestinationKeyerOID, 0x04, KeyVideoSource)
        self.__SetHelper('KeySource', SetKeyVideoSourceCmdString, value, qualifier)

    def UpdateKeySource(self, value, qualifier):
        
        try:
            KeyerOID = {1: 0xDF6, 2: 0xDF7, 3: 0xDF8, 4: 0xDF9}[qualifier['Keyer']]
        except KeyError:
            ProgramLog('[UpdateKeySource] Invalid Keyer number specified.', 'error')
            return False

        UpdateKeySourceCmdString =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, KeyerOID)
        self.__UpdateHelper('KeySource', UpdateKeySourceCmdString, value, qualifier)

    def __MatchKeySource(self, match, tag):
        
        KeyerVideoSourceOID = unpack('>H', match.group(1))[0]
        KeyerNumber = {0xDF6: 1, 0xDF7: 2, 0xDF8: 3, 0xDF9: 4}[KeyerVideoSourceOID]
        
        value = unpack('>l', match.group(2))[0]
        
        if value in self.VideoSourceNamesByID:
            self.WriteStatus('KeySource', self.VideoSourceNamesByID[value], {'Keyer': KeyerNumber})
        else:
            self.WriteStatus('KeySource', 'Unknown Source: {}'.format(value), {'Keyer': KeyerNumber})



    def SetAuxSource(self, value, qualifier):

        try:
            AuxVideoSource = self.VideoSourceIDsByName[value]
        except:
            ProgramLog('[SetAuxSource] Invalid source name specified.', 'error')
            return False

        try:
            AuxBusDestinationOID = {1: 0xDFE, 2: 0xDFF, 3: 0xE00, 4: 0xE01, 5: 0xE02, 6: 0xE03}[qualifier['Aux Bus']]
        except KeyError:
            ProgramLog('[SetAuxSource] Invalid Aux bus number specified.', 'error')
            return False

        SetAuxSourceCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, AuxBusDestinationOID, 0x04, AuxVideoSource)
        self.__SetHelper('AuxSource', SetAuxSourceCmdString, value, qualifier)

    def UpdateAuxSource(self, value, qualifier):
        
        try:
            AuxBusOID = {0xDFE: 1, 0xDFF: 2, 0xE00: 3, 0xE01: 4, 0xE02: 5, 0xE03: 6}[qualifier['Keyer']]
        except KeyError:
            ProgramLog('[UpdateAuxSource] Invalid Aux bus number specified.', 'error')
            return False

        UpdateAuxSourceCmdString =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, AuxBusOID)
        self.__UpdateHelper('AuxSource', UpdateAuxSourceCmdString, value, qualifier)

    def __MatchAuxSource(self, match, tag):
        
        AuxBusOID = unpack('>H', match.group(1))[0]
        AuxBusNumber = {0xDFE: 1, 0xDFF: 2, 0xE00: 3, 0xE01: 4, 0xE02: 5, 0xE03: 6}[AuxBusOID]
        
        value = unpack('>l', match.group(2))[0]
        
        if value in self.VideoSourceNamesByID:
            self.WriteStatus('AuxSource', self.VideoSourceNamesByID[value], {'Aux Bus': AuxBusNumber})
        else:
            self.WriteStatus('AuxSource', 'Unknown Source: {}'.format(value), {'Aux Bus': AuxBusNumber})




    def SetKeyerStatus(self, value, qualifier):

        try:
            KeyerNumber = qualifier['Keyer']
            KeyerOID = {1: 0x992, 2: 0x996, 3: 0x99A, 4: 0x99E}[KeyerNumber]
        except KeyError:
            ProgramLog('[SetKeyerStatus] Invalid keyer number specified.', 'error')
            return False

        try:
             KeyerStatus = {'Off-Air': 0x00, 'On-Air': 0x01}[value]
        except:
            ProgramLog('[SetKeyerStatus] Invalid keyer status specified.', 'error')
            return False
 
        SetKeyerStatusCmdString = pack('>HHBBBHBHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4A, 0x0008, 0x00, KeyerOID, 0x04, KeyerStatus)
        self.__SetHelper('KeyerStatus', SetKeyerStatusCmdString, value, {'Keyer' : KeyerNumber})

    def UpdateKeyerStatus(self, value, qualifier):
        
        try:
            KeyerNumber = qualifier['Keyer']
            KeyerOID = {1: 0x992, 2: 0x996, 3: 0x99A, 4: 0x99E}[KeyerNumber]
        except KeyError:
            ProgramLog('[UpdateKeyerStatus] Invalid keyer number specified.', 'error')
            return False
            
        UpdateKeyerStatus =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, KeyerOID)
        self.__UpdateHelper('KeyerStatus', UpdateKeyerStatus, value, qualifier)


    def __MatchKeyerStatus(self, match, tag):

        KeyerOID = unpack('>H', match.group(1))[0]
        KeyerNumber = {0x992: 1, 0x996: 2, 0x99A: 3, 0x99E: 4}[KeyerOID]

        value = unpack('>l', match.group(2))[0]
        KeyerStatus = {0x00: 'Off-Air', 0x01: 'On-Air'}[value]
        
        self.WriteStatus('KeyerStatus', KeyerStatus, {'Keyer': KeyerNumber})



    def SetNextTransitionLayers(self, value, qualifier):

        try:
            KeyerIndex = {'BG': 0x0, 'Key 1': 0x1, 'Key 2': 0x2, 'Key 3': 0x3, 'Key 4': 0x4}[qualifier['Layer']]
        except KeyError:
            ProgramLog('[SetNextTransitionLayers] Invalid keyer number specified.', 'error')
            return False

        try:
             KeyerStatus = {'Off': 0x00, 'On': 0x01}[value]
        except KeyError:
            ProgramLog('[SetNextTransitionLayers] Invalid keyer status specified.', 'error')
            return False

        SetNextTransitionLayersCmdString = pack('>HHBBBHBHHBl', 0xBAD2, 0xACE5, 0x00, 0x10, 0x4D, 0x000A, 0x00, 0x990, KeyerIndex, 0x04, KeyerStatus)
        self.__SetHelper('NextTransitionLayers', SetNextTransitionLayersCmdString, value, {'Layer' : value})

    #def UpdateNextTransitionLayers(self, value, qualifier):
        #
        #try:
            #KeyerNumber = qualifier['Keyer']
            #KeyerOID = {1: 0x992, 2: 0x996, 3: 0x99A, 4: 0x99E}[KeyerNumber]
        #except KeyError:
            #ProgramLog('[UpdateKeyerStatus] Invalid keyer number specified.', 'error')
            #return False
            #
        #UpdateKeyerStatus =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, KeyerOID)
        #self.__UpdateHelper('KeyerStatus', UpdateKeyerStatus, value, qualifier)
#
#
    def __MatchNextTransitionLayers(self, match, tag):
#
#\xca\x00\x08\x00\t\x95\x04\x00\x00\x00\x00
#\xca\x00\x08\x00\t\x99\x04\x00\x00\x00\x02
#\xca\x00\x08\x00\t\x9d\x04\x00\x00\x00\x00
#\xca\x00\x08\x00\t\xa1\x04\x00\x00\x00\x02
#\xca\x00\x08\x00\t\x8d\x04\x00\x00\x00\x00

        #print('NEXT TRANSITION ->', match.group(1), 'VALUE ->', match.group(2))
        #print('MATCHED: ->', match.group(1))
        #print('VALUE  ->', match.group(2))
        #KeyerOID = unpack('>H', match.group(1))[0]
        LayerName = {0x0: 'BG', 0x1: 'Key 1', 0x2: 'Key 2', 0x3: 'Key 3', 0x4: 'Key 4'}[unpack('>H', match.group(1))[0]]
        LayerState = {0x00: 'Off', 0x01: 'On'}[unpack('>l', match.group(2))[0]]
        #print('LAYER NAME ->', LayerName)
        #print('LAYER STATE ->', LayerState)
        
        #value = 
        #try:
        #except KeyError:
        #    print('DID NOT WORK! value: ', value)
        
        
        
        self.WriteStatus('NextTransitionLayers', LayerState, {'Layer': LayerName})

####################

    def __KeepAliveTimerHandler(self):
        print('Staying alive...')
        if self.connectionFlag:
            self.KeepAliveTimerObject.Restart()
            self.UpdateProductName(None, None)

    def UpdateProductName(self, value, qualifier):
        ProductNameOID = 0x1EE6
        UpdateProductNameString =   pack('>HHHBHBH', 0xBAD2, 0xACE5, 0x0010, 0x49, 0x0003, 0x00, ProductNameOID)
        self.__UpdateHelper('ProductName', UpdateProductNameString, value, qualifier)

    def __MatchProductName(self, match, tag):
        EncodedProductName = match.group(2)   #.decode() #.rstrip('\x00')
        #BinaryProductName = unpack('>' + 'c'*len(EncodedProductName) , match.group(2))  #.decode() #.rstrip('\x00')
        
        #tmp = b''
        #tmp.join (BinaryProductName)
        try:
            ProductName = EncodedProductName.decode('ascii')
        
        except:
            print('COULD NOT DECODE THIS: [{}]'.format(EncodedProductName))
        
            ProductName = 'COULD NOT DECODE'
        
        #ProgramLog(ProductName, 'info')
        self.WriteStatus('ProductName', ProductName)
#        except:
#            ProgramLog('COULD NOT PARSE PRODUCTNAME!', 'error')
################################
## STUFF BELOW THIS LINE IS PROBABLY VESTIGIAL?


    def __MatchClipProgress(self, match, tag):
        pass
#################################        





    def SendHandshake(self):
        
        # If our HandshakeCompleted is FALSE, but we're triggering this ..
        #  it means we're not actually connected yet. We need to send our handshake,
        #  then we can start communicating with the device
        if self.HandshakeCompleted is False:
            HandshakeCmdString = b'\xba\xd2\xac\xe5\x00\x10\x4A\x00\x08\x00\xff\x03\x04\x00\x00\x00\x00'

            #print('SENDING HANDSHAKE TO SWITCHER->', HandshakeCmdString)    
            self.Send(HandshakeCmdString)
            self.HandshakeCompleted = True                               
        
        else:
            return


    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        
        self.Send(commandstring)


    def __UpdateHelper(self, command, commandstring, value, qualifier):

        if self.Unidirectional == 'True':
            print('Inappropriate Command ', command)
        else:
            if self.initializationChk:
                self.OnConnected()
                self.initializationChk = False

            self.counter = self.counter + 1
            if self.counter > self.connectionCounter and self.connectionFlag:
                self.OnDisconnected()

            self.Send(commandstring)


    def OnConnected(self):
        self.SendHandshake()
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        
        #self.KeepAliveTimerObject = Wait(self.__KeepAliveSeconds, self.__KeepAliveTimerHandler) 

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        self.HandshakeCompleted = False
        #self.KeepAliveTimerObject.Cancel()

    ######################################################
    # RECOMMENDED not to modify the code below this point
    ######################################################
    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = 'Set%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(value, qualifier)
        else:
            print(command, 'does not support Set.')
            
    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = 'Update%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(None, qualifier)
        else:
            print(command, 'does not support Update.')

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method': {}}

            Subscribe = self.Subscription[command]
            Method = Subscribe['method']

            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return

            Method['callback'] = callback
            Method['qualifier'] = qualifier
        else:
            print(command, 'does not exist in the module')

    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription:
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)

    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    return None
        try:
            return Status['Live']
        except:
            return None

    def __ReceiveData(self, interface, data):
        # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

        #print('RCV->', self._ReceiveBuffer)
        
    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para': arg}

    # Check incoming unsolicited data to see if it was matched with device expectancy.
    def CheckMatchedString(self):
        for regexString in self._compile_list:
            while True:
                result = re.search(regexString, self._ReceiveBuffer)
                if result:
                    self._compile_list[regexString]['callback'](result, self._compile_list[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True


class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()

    def Disconnect(self):
        EthernetClientInterface.Disconnect(self)
        self.OnDisconnected()
