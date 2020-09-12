from extronlib.interface import SerialInterface, EthernetClientInterface
import re
from extronlib.system import Wait, ProgramLog

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
            'Firmware': { 'Status': {}},
            'InputLevel': {'Parameters':['Channel'], 'Status': {}},
            'InputMute': {'Parameters':['Channel'], 'Status': {}},
            'OutputLevel': {'Parameters':['Channel'], 'Status': {}},
            'OutputMute': {'Parameters':['Channel'], 'Status': {}},
            'Preset': {'Parameters':['Scene','Action'], 'Status': {}},
            }                   

        
        if self.Unidirectional == 'False':
            self.AddMatchString(re.compile(b'OK devinfo version \"(V[\.\d]+)\"\n'), self.__MatchFirmware, None)
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY|OKm) (?:setn|getn|set|get) MIXER:Current/InCh/Fader/Level ([0-9]{1,2}) 0 ([\-\d]{1,4}) \"[\-\.\d]+\"\n'), self.__MatchInputLevel, None)
            self.AddMatchString(re.compile(b'(?:OK|Notify|OKm) (?:setn|getn) MIXER:Current/Mix/Fader/Level ([0-9]{1,2}) 0 (\d{1,4})\n'), self.__MatchOutputLevel, None)
            self.AddMatchString(re.compile(b'(?:OK|NOTIFY) (?:set|get) MIXER:Current/InCh/Fader/On ([0-9]{1,2}) 0 (1|0) \"(ON|OFF)\"\n'), self.__MatchInputMute, None)
            self.AddMatchString(re.compile(b'(?:OK|Notify) (?:set|get) MIXER:Current/Mix/Fader/On ([0-9]{1,2}) 0 (1|0)\n'), self.__MatchOutputMute, None)
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

        Channel = int(qualifier['Channel'])
        if 1 <= Channel <= 40:
            CmdString = 'get MIXER:Current/Mix/Fader/On {0} 0\n'.format(Channel-1)
            self.__UpdateHelper('OutputMute', CmdString, value, qualifier)
        else:
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
        print('YAMAHA RCV ->', data)

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

