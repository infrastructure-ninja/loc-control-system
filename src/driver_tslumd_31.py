from extronlib.interface import EthernetServerInterfaceEx

import re
from struct import unpack

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

        self.Commands = {
            #'ConnectionStatus': {'Status': {}}
            'Tally': {'Parameters': ['Input'], 'Status': {}}
        }

        if self.Unidirectional == 'False':
            self.AddMatchString(re.compile(b'([\x00-\xff])([\x00-\xff])([\x00-\xff]{16})'), self.__MatchTally, None)


    def __MatchTally(self, match, tag):
        # This list comes from here:
        # http://help.rossvideo.com/carbonite-device/Topics/Devices/UMD/TSL.html
        # 0	BK, BG, no src
        # 1-9	Input 1-9
        # 37	ME 1 BKGD
        # 38	ME 1 PST
        # 39	ME 1 Key 1 Video
        # 40	ME 1 Key 1 Alpha
        # 41	ME 1 Key 2 Video
        # 42	ME 1 Key 2 Alpha
        # 43	ME 1 Key 3 Video
        # 44	ME 1 Key 3 Alpha
        # 45	ME 1 Key 4 Video
        # 46	ME 1 Key 4 Alpha
        # 67-76	Aux 1-10
        # 77-82	Aux 11-16
        # 87	MiniME™ 1 BKGD
        # 88	MiniME™ 1 PST
        # 89	MiniME™ 1 Key 1 Video
        # 90	MiniME™ 1 Key 2 Video
        # 91	MiniME™ 2 BKGD
        # 92	MiniME™ 2 PST
        # 93	MiniME™ 2 Key 1 Video
        # 94	MiniME™ 2 Key 2 Video
        # 101	Media-Store 1
        # 102	Media-Store 2
        # 103	Media-Store 3
        # 104	Media-Store 4
        # 110   Program
        # 111	Preview
        # 112	Clean
        # 113	ME 1 PGM
        # 114	ME 1 PV
        # 115	ME 1 Clean
        # 116	MiniME™ 1
        # 117	MiniME™ 2

        tsl_input_map = {1: 'Cam 1', 2: 'Cam 2', 3: 'Cam 3', 4: 'Cam 4',
                         5: 'Cam 5', 6: 'Cam 6', 7: 'HDMI 1', 8: 'HDMI 2', 9: 'HDMI 3'}

        #PROTOCOL DOCUMENTATION AVAILABLE HERE
        #https://tslproducts.com/media/1959/tsl-umd-protocol.pdf

        header = unpack('>B', match.group(1))[0]
        tally_id = header - 0x80

        control_byte = unpack('>B', match.group(2))[0]

        green_tally = (control_byte & 1 != 0) # returns True or False
        red_tally = (control_byte & 2 != 0)   # returns True or False

        #This is a tuple and a dictionary lookup. The two boolean values together combine in a
        # tuple to get us the value that we want to return.
        tally_value_map = {(False, False): 'Off',
                           (True, False) : 'Green',
                           (False, True) : 'Red',
                           (True, True)  : 'Red & Green'}

        value = tally_value_map[(green_tally, red_tally)]

        display_data = match.group(3).strip(b'\x20')

        if tally_id in tsl_input_map:
            input_name = tsl_input_map[tally_id]

            self.WriteStatus('Tally', value, {'Input': input_name})

        else:
            # What we would od if we received a tally ID we don't handle
            pass
            #print('TALLY ID NOT FOUND -> [{}]'.format(tally_id))

        #Control (1 byte)
        #bit 0 = tally 1 (1 = on, 0 = off )
        #bit 1 = tally 2 (1 = on, 0 = off )
        #bit 2 = tally 3 (1 = on, 0 = off )
        #bit 3 = tally 4 (1 = on, 0 = off )


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
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        
    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

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


class EthernetClass(EthernetServerInterfaceEx, DeviceClass):

    def __init__(self, IPPort, Model=None):
        EthernetServerInterfaceEx.__init__(self, IPPort, 'TCP')
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()
