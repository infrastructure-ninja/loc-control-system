from extronlib.interface import SerialInterface, EthernetClientInterface
import re

class DeviceClass:    
    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {
            'TF5': self.yama_25_2973_A,
            'TF1': self.yama_25_2973_B,
            'TF-Rack': self.yama_25_2973_B,
            }

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'Firmware': {'Status': {}},
            'Preset': {'Parameters': ['Scene', 'Action'], 'Status': {}},
            'InputLevel': {'Parameters': ['Channel'], 'Status': {}},
            'InputMute': {'Parameters': ['Channel'], 'Status': {}},
            'OutputLevel': {'Parameters': ['Channel'], 'Status': {}},
            'OutputMute': {'Parameters': ['Channel'], 'Status': {}},
            'AuxMute': {'Parameters': ['Input Channel', 'Aux Channel'], 'Status': {}},
            'AuxLevel': {'Parameters': ['Input Channel', 'Aux Channel'], 'Status': {}},
            'StereoInLevel' : {'Parameters': ['Channel'], 'Status': {}},
            'StereoInMute': {'Parameters': ['Channel'], 'Status': {}}
        }

        if self.Unidirectional == 'False':
            self.AddMatchString(re.compile(b'OK devinfo version "?(V[\.\d]+)"?\n'), self.__MatchFirmware, None)


            # b'NOTIFY set MIXER:Current/InCh/Fader/On 24 0 0 "OFF"\n'
            # b'NOTIFY set MIXER:Current/InCh/Fader/On 24 0 1 "ON"\n'
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY) (?:set|get) MIXER:Current/InCh/Fader/On ([0-9]{1,2}) 0 (1|0)(?: \"(ON|OFF)\"){0,1}\n'), self.__MatchInputMute, None)
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY|OKm) (?:setn|getn|set|get) MIXER:Current/InCh/Fader/Level ([0-9]{1,2}) 0 ([\-\d]{1,6}) \"[\-\.\d]+\"\n'), self.__MatchInputLevel, None)


            #'NOTIFY set MIXER:Current/Mix/Fader/On 2 0 1 "ON"\n'
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY|Notify) (?:set|get) MIXER:Current/Mix/Fader/On ([0-9]{1,2}) 0 (1|0) \"(ON|OFF)\"\n'), self.__MatchOutputMute, None)

            # NOTIFY set MIXER:Current/Mix/Fader/Level 2 0 -7340 "-73.40"\n
            # NOTIFY set MIXER:Current/Mix/Fader/Level 2 0 -10800 "-108.0"\n
            # NOTIFY set MIXER:Current/Mix/Fader/Level 2 0 -32768 "-?"\n
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY|Notify|OKm) (?:setn|getn|set|get) MIXER:Current/Mix/Fader/Level ([0-9]{1,2}) 0 ([\-\d]{1,6}) \"[\?\-\.\d]+\"\n'), self.__MatchOutputLevel, None)


            # NOTIFY set MIXER:Current/InCh/ToMix/On 24 2 1 "ON"\n
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY|Notify) (?:set|get) MIXER:Current/InCh/ToMix/On ([0-9]{1,2}) ([0-9]{1,2}) (0|1) \"(?:ON|OFF)\"\n'), self.__MatchAuxMute, None)

            # NOTIFY set MIXER:Current/InCh/ToMix/Level 24 2 -2180 "-21.80"\n
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY|Notify|OKm) (?:set|get|setn|getn) MIXER:Current/InCh/ToMix/Level ([0-9]{1,2}) ([0-9]{1,2}) ([\-\d]{1,6})(?: \"[\?\-\.\d]+\"){0,1}\n'), self.__MatchAuxLevel, None)

            # NOTIFY set MIXER:Current/StInCh/Fader/Level 3 0 -1835 "-18.35"\n
            self.AddMatchString(re.compile(b'(?:OK|Notify|NOTIFY|OKm) (?:set|get|setn|getn) MIXER:Current/StInCh/Fader/Level ([0-3]) 0 ([\-\d]{1,6}) \"[\?\-\.\d]+\"\n'), self.__MatchStereoInLevel, None)

            # NOTIFY set MIXER:Current/StInCh/Fader/On 2 0 0 "OFF"\n
            self.AddMatchString(re.compile(b'(?:OK|Notify|NOTIFY) (?:set|get) MIXER:Current/StInCh/Fader/On ([0-3]) 0 ([01]) \"(?:ON|OFF)\"\n'), self.__MatchStereoInMute, None)


            # NOTIFY mtr MIXER:Current/InCh/PostOn level 14 00 00 00
            #NOTIFY)mtr MIXER:Current/Mix/PostOn level
            #self.AddMatchString(re.compile(b'(?:OK|Notify|NOTIFY) (?:set|get) MIXER:Current/StInCh/Fader/On ([0-3]) 0 ([01]) \"(?:ON|OFF)\"\n'), self.__MatchLevelResponse, None)


            self.AddMatchString(re.compile(b'(ERROR get InvalidArgument|ERROR unknown UnknownCommand)'), self.__MatchError, None)


    def UpdateFirmware(self, value, qualifier):
        CmdString = 'devinfo version\n'
        self.__UpdateHelper('Firmware', CmdString, value, qualifier)

    def __MatchFirmware(self, match, tag):
        self.WriteStatus('Firmware',  match.group(1).decode() , None)

    def SetInputLevel(self, value, qualifier):
        Channel = int(qualifier['Channel'])

        if 0 <= value <= 1000 and 1 <= Channel <= self.MaxInputChannels:
            CmdString = 'setn MIXER:Current/InCh/Fader/Level {0} 0 {1}\n'.format(Channel-1,value)
            self.__SetHelper('InputLevel', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetInputLevel')

    def UpdateInputLevel(self, value, qualifier):

        Channel = int(qualifier['Channel'])

        if 1 <= Channel <= self.MaxInputChannels:
            CmdString = 'getn MIXER:Current/InCh/Fader/Level {0} 0\n'.format(Channel-1)
            self.__UpdateHelper('InputLevel', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateInputLevel')

    def __MatchInputLevel(self, match, tag):
        self.WriteStatus('InputLevel', int(match.group(2).decode()), {'Channel' : str(int(match.group(1).decode())+1)} )

    def SetInputMute(self, value, qualifier):

        States = {
            'On'  : '1', 
            'Off' : '0'
        }
        Channel = int(qualifier['Channel'])

        if 1 <= Channel <= self.MaxInputChannels:
            CmdString = 'set MIXER:Current/InCh/Fader/On {0} 0 {1}\n'.format(Channel-1,States[value])
            self.__SetHelper('InputMute', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetInputMute')

    def UpdateInputMute(self, value, qualifier):
        Channel = int(qualifier['Channel'])
        if 1 <= Channel <= self.MaxInputChannels:
            CmdString = 'get MIXER:Current/InCh/Fader/On {0} 0\n'.format(Channel-1)
            self.__UpdateHelper('InputMute', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateInputMute')

    def __MatchInputMute(self, match, tag):

        States = {
            '1' : 'On', 
            '0' : 'Off'
        }

        self.WriteStatus('InputMute',  States[match.group(2).decode()] , {'Channel' : str(int(match.group(1).decode())+1)} )

    def SetOutputLevel(self, value, qualifier):

        Channel = int(qualifier['Channel'])

        if 0<= value <= 1000 and 1 <= Channel <= 20:
            CmdString = 'setn MIXER:Current/Mix/Fader/Level {0} 0 {1}\n'.format(Channel-1,value)
            self.__SetHelper('OutputLevel', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetOutputLevel')

    def UpdateOutputLevel(self, value, qualifier):

        Channel = int(qualifier['Channel'])

        if 1 <= Channel <= 40:
            CmdString = 'getn MIXER:Current/Mix/Fader/Level {0} 0\n'.format(Channel-1)
            self.__UpdateHelper('OutputLevel', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateOutputLevel')

    def __MatchOutputLevel(self, match, tag):
        self.WriteStatus('OutputLevel', int(match.group(2).decode()), {'Channel' : str(int(match.group(1).decode())+1)} )

    def SetOutputMute(self, value, qualifier):

        States = {
            'On'  : '1', 
            'Off' : '0'
        }
        Channel = int(qualifier['Channel'])
        if 1 <= Channel <= 20:
            CmdString = 'set MIXER:Current/Mix/Fader/On {0} 0 {1}\n'.format(Channel-1,States[value])
            self.__SetHelper('OutputMute', CmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetOutputMute')

    def UpdateOutputMute(self, value, qualifier):

        try:
            Channel = int(qualifier['Channel'])

            if 1 <= Channel <= 40:
                CmdString = 'get MIXER:Current/Mix/Fader/On {0} 0\n'.format(Channel-1)
                self.__UpdateHelper('OutputMute', CmdString, value, qualifier)
            else:
                self.Discard('Invalid Command for UpdateOutputMute')

        except TypeError:
            self.Discard('Invalid Command for UpdateOutputMute')

    def __MatchOutputMute(self, match, tag):

        States = {
            '1' : 'On', 
            '0' : 'Off'
        }

        self.WriteStatus('OutputMute',  States[match.group(2).decode()] , {'Channel' : str(int(match.group(1).decode())+1)} )

    def SetPreset(self, value, qualifier):

        SceneStates = {
            'A' : 'a', 
            'B' : 'b'
        }

        ActionStates = {
            'Recall' : 'recall', 
            'Store'  : 'update'
        }

        action = qualifier['Action']
        scene = qualifier['Scene']
        if action in ActionStates and scene in SceneStates and 0 <= int(value) <= 99:
            CmdString = 'ss{0}_ex scene_{1} {2}\x0A'.format(ActionStates[action],SceneStates[scene],value)
            self.__SetHelper('Preset', CmdString, value, qualifier)


#### AUX Mute ####
    def SetAuxMute(self, value, qualifier):
        """Set AUX Mute
        value: Enum
        qualifier: {'Input Channel' : Enum, 'AUX Channel' : Enum}
        """
        ValueStateValues = {
            'On'  : '1',
            'Off' : '0'
        }

        input_channel = int(qualifier['Input Channel'])
        aux_channel = int(qualifier['Aux Channel'])

        if 1 <= input_channel <= self.MaxInputChannels and 1 <= aux_channel <= 20:
            AuxMuteCmdString = 'set MIXER:Current/InCh/ToMix/On {0} {1} {2}\n'.format(input_channel - 1, aux_channel - 1, ValueStateValues[value])
            self.__SetHelper('AuxMute', AuxMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def UpdateAuxMute(self, value, qualifier):
        """Update AUX Mute
        value: Enum
        qualifier: {'Input Channel' : Enum, 'AUX Channel' : Enum}
        """
        input_channel = int(qualifier['Input Channel'])
        aux_channel = int(qualifier['Aux Channel'])

        if 1 <= input_channel <= self.MaxInputChannels and 1 <= aux_channel <= 20:
            AuxMuteCmdString = 'get MIXER:Current/InCh/ToMix/On {0} {1}\n'.format(input_channel - 1, aux_channel - 1)
            self.__UpdateHelper('AuxMute', AuxMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def __MatchAuxMute(self, match, tag):
        ValueStateValues = {
            '1' : 'On',
            '0' : 'Off'
        }

        qualifier = {}
        qualifier['Input Channel'] = str(int(match.group(1).decode())+1)
        qualifier['Aux Channel'] = str(int(match.group(2).decode())+1)
        value = ValueStateValues[match.group(3).decode()]

        self.WriteStatus('AuxMute', value, qualifier)


### Aux Level ###
    def SetAuxLevel(self, value, qualifier):
        """Set AUX Level
        value: Decimal
        qualifier: {'Input Channel' : Enum, 'AUX Channel' : Enum}
        """
        ValueConstraints = {
            'Min': 0,
            'Max': 1000
            }
        input_channel = int(qualifier['Input Channel'])
        aux_channel = int(qualifier['Aux Channel'])

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max'] and 1 <= input_channel <= self.MaxInputChannels and 1 <= aux_channel <= 20:
            AuxLevelCmdString = 'setn MIXER:Current/InCh/ToMix/Level {0} {1} {2}\n'.format(input_channel - 1, aux_channel - 1, value)
            self.__SetHelper('AuxLevel', AuxLevelCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def UpdateAuxLevel(self, value, qualifier):
        """Update AUX Level
        value: Decimal
        qualifier: {'Input Channel' : Enum, 'AUX Channel' : Enum}
        """
        input_channel = int(qualifier['Input Channel'])
        aux_channel = int(qualifier['Aux Channel'])
        if 1 <= input_channel <= self.MaxInputChannels and 1 <= aux_channel <= 20:
            AuxLevelCmdString = 'get MIXER:Current/InCh/ToMix/Level {0} {1}\n'.format(input_channel - 1, aux_channel - 1)
            self.__UpdateHelper('AuxLevel', AuxLevelCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def __MatchAuxLevel(self, match, tag):
        """AUX Level MatchString Handler
        """
        qualifier = {}
        qualifier['Input Channel'] = str(int(match.group(1).decode())+1)
        qualifier['Aux Channel'] = str(int(match.group(2).decode())+1)
        value = int(match.group(3).decode())

        self.WriteStatus('AuxLevel', value, qualifier)

### Stereo In Level ###
    def SetStereoInLevel(self, value, qualifier):
        """Set Stereo In Level
        value: Decimal
        qualifier: {'Channel' : Enum}
        """
        ChannelStates = {
            '1L': '0',
            '1R': '1',
            '2L': '2',
            '2R': '3'
        }

        channel = qualifier['Channel']
        if channel in ChannelStates and 0 <= value <= 1000:
            StereoInLevelCmdString = 'setn MIXER:Current/StInCh/Fader/Level {0} 0 {1}\n'.format(ChannelStates[channel], value)
            self.__SetHelper('StereoInLevel', StereoInLevelCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def UpdateStereoInLevel(self, value, qualifier):
        """Update Stereo In Level
        value: Decimal
        qualifier: {'Channel' : Enum}
        """
        ChannelStates = {
            '1L': '0',
            '1R': '1',
            '2L': '2',
            '2R': '3'
        }

        channel = qualifier['Channel']
        if channel in ChannelStates:
            StereoInLevelCmdString = 'getn MIXER:Current/StInCh/Fader/Level {0} 0\n'.format(ChannelStates[channel])
            self.__UpdateHelper('StereoInLevel', StereoInLevelCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def __MatchStereoInLevel(self, match, tag):
        """Stereo In Level MatchString Handler
        """
        ChannelStates = {
            '0': '1L',
            '1': '1R',
            '2': '2L',
            '3': '2R'
        }

        qualifier = {
            'Channel': ChannelStates[match.group(1).decode()]
        }
        value = int(match.group(2).decode())
        self.WriteStatus('StereoInLevel', value, qualifier)

### Stereo In Mute ###
    def SetStereoInMute(self, value, qualifier):
        """Set Stereo In Mute
        value: Enum
        qualifier: {'Channel' : Enum}
        """
        ChannelStates = {
            '1L': '0',
            '1R': '1',
            '2L': '2',
            '2R': '3'
        }

        channel = qualifier['Channel']

        ValueStateValues = {
            'On':   '1',
            'Off':  '0'
        }

        if channel in ChannelStates and value in ValueStateValues:
            StereoInMuteCmdString = 'set MIXER:Current/StInCh/Fader/On {0} 0 {1}\n'.format(ChannelStates[channel], ValueStateValues[value])
            self.__SetHelper('StereoInMute', StereoInMuteCmdString, value, qualifier)

        else:
            self.Discard('Invalid Command')

    def UpdateStereoInMute(self, value, qualifier):
        """Update Stereo In Mute
        value: Enum
        qualifier: {'Channel' : Enum}
        """
        ChannelStates = {
            '1L': '0',
            '1R': '1',
            '2L': '2',
            '2R': '3'
        }

        channel = qualifier['Channel']

        if channel in ChannelStates:
            StereoInMuteCmdString = 'get MIXER:Current/StInCh/Fader/On {0} 0\n'.format(ChannelStates[channel])
            self.__UpdateHelper('StereoInMute', StereoInMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def __MatchStereoInMute(self, match, tag):
        """Stereo In Mute MatchString Handler
        """
        ChannelStates = {
            '0': '1L',
            '1': '1R',
            '2': '2L',
            '3': '2R'
        }

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        qualifier = {
            'Channel': ChannelStates[match.group(1).decode()]
        }

        value = ValueStateValues[match.group(2).decode()]

        self.WriteStatus('StereoInMute', value, qualifier)



    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):

        if self.Unidirectional == 'True':
            self.Discard('Inappropriate Command ' + command)
        else:
            self.Send(commandstring)

            if self.initializationChk:
                self.OnConnected()
                self.initializationChk = False

            self.counter = self.counter + 1
            if self.counter > self.connectionCounter and self.connectionFlag:
                self.OnDisconnected()

    def __MatchError(self, match, tag):
        self.Error([match.group(0).decode()])
   
    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0


    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

    def yama_25_2973_A(self):
        self.MaxInputChannels = 40

    def yama_25_2973_B(self):
        self.MaxInputChannels = 32
    ######################################################    
    # RECOMMENDED not to modify the code below this point
    ######################################################
	# Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = getattr(self, 'Set%s' % command)
        if method is not None and callable(method):
            method(value, qualifier)
        else:
            print(command, 'does not support Set.')

    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = getattr(self, 'Update%s' % command)
        if method is not None and callable(method):
            method(None, qualifier)
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
                self.Subscription[command] = {'method':{}}
        
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
        if command in self.Subscription :
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
        #FIXME - testing only!
        #print('YAMAHA RCV ->', data)

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para':arg}
                

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

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self) 
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models: 
                print('Model mismatch')              
            else:
                self.Models[Model]()

    def Error(self, message):
        portInfo = 'IP Address/Host: {0}:{1}'.format(self.Hostname, self.IPPort)
        print('Module: {}'.format(__name__), portInfo, 'Error Message: {}'.format(message[0]), sep='\r\n')
  
    def Discard(self, message):
        self.Error([message])

    def Disconnect(self):
        EthernetClientInterface.Disconnect(self)
        self.OnDisconnected()

