from extronlib.interface import SerialInterface, EthernetClientInterface
from re import compile, search
from extronlib.system import Wait, ProgramLog


class DeviceClass:
    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self.__receiveBuffer = b''
        self.__maxBufferSize = 2048
        self.__matchStringDict = {}
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {
            'DMP 128 Plus'       : self.extr_25_2513_128,
            'DMP 128 Plus C'     : self.extr_25_2513_128,
            'DMP 128 Plus C AT'  : self.extr_25_2513_128AT,
            'DMP 128 Plus AT'    : self.extr_25_2513_128AT,
            'DMP 128 Plus C V'   : self.extr_25_2513_128V,
            'DMP 128 Plus C V AT': self.extr_25_2513_128VAT,
        }

        self.Commands = {
            'ConnectionStatus'              : {'Status': {}},
            'AutoAnswerDelay'               : {'Parameters': ['Line'], 'Status': {}},
            'AutoAnswerMode'                : {'Parameters': ['Line'], 'Status': {}},
            'AutomixerGateSet'              : {'Parameters': ['Input'], 'Status': {}},
            'AutomixerGateStatus'           : {'Parameters': ['Input'], 'Status': {}},
            'AuxInputGain'                  : {'Parameters': ['Input'], 'Status': {}},
            'AuxInputMute'                  : {'Parameters': ['Input'], 'Status': {}},
            'AuxInputPremixerGain'          : {'Parameters': ['Input'], 'Status': {}},
            'AuxInputPremixerMute'          : {'Parameters': ['Input'], 'Status': {}},
            'AuxOutputGain'                 : {'Parameters': ['Output'], 'Status': {}},
            'AuxOutputMute'                 : {'Parameters': ['Output'], 'Status': {}},
            'AuxOutputPostmixerTrim'        : {'Parameters': ['Output'], 'Status': {}},
            'CallDuration'                  : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'CallerExtension'               : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'CallerID'                      : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'CallerName'                    : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'CallStatus'                    : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'Dial'                          : {'Parameters': ['Line'], 'Status': {}},
            'DialDTMF'                      : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'DoNotDisturb'                  : {'Parameters': ['Line'], 'Status': {}},
            'DigitalInputStatus'            : {'Parameters': ['Input'], 'Status': {}},
            'DigitalInputGain'              : {'Parameters': ['Input'], 'Status': {}},
            'ExpansionBusMixpointGain'      : {'Parameters': ['Input', 'Output'], 'Status': {}},
            'ExpansionBusMixpointMute'      : {'Parameters': ['Input', 'Output'], 'Status': {}},
            'ExpansionInputPremixerGain'    : {'Parameters': ['Input'], 'Status': {}},
            'ExpansionInputPremixerMute'    : {'Parameters': ['Input'], 'Status': {}},
            'ExpansionOutputAttenuation'    : {'Parameters': ['Output'], 'Status': {}},
            'ExpansionOutputMute'           : {'Parameters': ['Output'], 'Status': {}},
            'ExpansionOutputPostmixerTrim'  : {'Parameters': ['Output'], 'Status': {}},
            'GroupBassInputFilter'          : {'Parameters': ['Group'], 'Status': {}},
            'GroupBassVirtualReturnFilter'  : {'Parameters': ['Group'], 'Status': {}},
            'GroupMicLineInputGain'         : {'Parameters': ['Group'], 'Status': {}},
            'GroupMixpointGain'             : {'Parameters': ['Group'], 'Status': {}},
            'GroupMute'                     : {'Parameters': ['Group'], 'Status': {}},
            'GroupOutputAttenuation'        : {'Parameters': ['Group'], 'Status': {}},
            'GroupPostMixerTrim'            : {'Parameters': ['Group'], 'Status': {}},
            'GroupPreMixerGain'             : {'Parameters': ['Group'], 'Status': {}},
            'GroupTrebleInputFilter'        : {'Parameters': ['Group'], 'Status': {}},
            'GroupTrebleVirtualReturnFilter': {'Parameters': ['Group'], 'Status': {}},
            'GroupVirtualReturnGain'        : {'Parameters': ['Group'], 'Status': {}},
            'Hook'                          : {'Parameters': ['Line', 'Appearance'], 'Status': {}},
            'InputGain'                     : {'Parameters': ['Input'], 'Status': {}},
            'InputMute'                     : {'Parameters': ['Input'], 'Status': {}},
            'InputSignalLevelMonitor'       : {'Parameters': ['Input', 'Monitoring Threshold'], 'Status': {}},
            'Macro'                         : {'Parameters': ['Macro'], 'Status': {}},
            'MixpointGain'                  : {'Parameters': ['Input', 'Output'], 'Status': {}},
            'MixpointMute'                  : {'Parameters': ['Input', 'Output'], 'Status': {}},
            'OutputMute'                    : {'Parameters': ['Output'], 'Status': {}},
            'OutputPostmixerTrim'           : {'Parameters': ['Output'], 'Status': {}},
            'OutputAttenuation'             : {'Parameters': ['Output'], 'Status': {}},
            'PartNumber'                    : {'Status': {}},
            'PhantomPower'                  : {'Parameters': ['Input'], 'Status': {}},
            'PremixerGain'                  : {'Parameters': ['Input'], 'Status': {}},
            'PremixerMute'                  : {'Parameters': ['Input'], 'Status': {}},
            'PresetRecall'                  : {'Status': {}},
            'RegistrationStatus'            : {'Parameters': ['Line'], 'Status': {}},
            'PlayerControl'                 : {'Parameters': ['Player ID'], 'Status': {}},
            'PlayerFilename'                : {'Parameters': ['Player ID'], 'Status': {}},
            'PlayerFilenameStatus'          : {'Parameters': ['Player ID'], 'Status': {}},
            'PlayerRepeat'                  : {'Parameters': ['Player ID'], 'Status': {}},
            'VirtualReturnGain'             : {'Parameters': ['Input'], 'Status': {}},
            'VirtualReturnMute'             : {'Parameters': ['Input'], 'Status': {}},

            # BEGIN - ADDED BY JDC
            'UnsolicitedMeterGroupNumber' : {'Status': {}},
            'UnsolicitedMeterResponseRate': {'Status': {}},
            'UnsolicitedMeterData'        : {'Parameters': ['OID'], 'Status': {}},
            # END - ADDED BY JDC

        }

        self.GroupFunction = {}
        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'
        self.devicePassword = 'extron'
        self.ReDialString = ''
        self.inputSignalLevelMonitorThreshold = {}

        self.MixpointOutputStateValues = {
            '1'        : '00',
            '2'        : '01',
            '3'        : '02',
            '4'        : '03',
            '5'        : '04',
            '6'        : '05',
            '7'        : '06',
            '8'        : '07',
            'Aux 1'    : '08',
            'Aux 2'    : '09',
            'Aux 3'    : '10',
            'Aux 4'    : '11',
            'Aux 5'    : '12',
            'Aux 6'    : '13',
            'Aux 7'    : '14',
            'Aux 8'    : '15',
            'Exp. 1'   : '32',
            'Exp. 2'   : '33',
            'Exp. 3'   : '34',
            'Exp. 4'   : '35',
            'Exp. 5'   : '36',
            'Exp. 6'   : '37',
            'Exp. 7'   : '38',
            'Exp. 8'   : '39',
            'Exp. 9'   : '40',
            'Exp. 10'  : '41',
            'Exp. 11'  : '42',
            'Exp. 12'  : '43',
            'Exp. 13'  : '44',
            'Exp. 14'  : '45',
            'Exp. 15'  : '46',
            'Exp. 16'  : '47',
            'V. Send A': '16',
            'V. Send B': '17',
            'V. Send C': '18',
            'V. Send D': '19',
            'V. Send E': '20',
            'V. Send F': '21',
            'V. Send G': '22',
            'V. Send H': '23',
            'V. Send I': '24',
            'V. Send J': '25',
            'V. Send K': '26',
            'V. Send L': '27',
            'V. Send M': '28',
            'V. Send N': '29',
            'V. Send O': '30',
            'V. Send P': '31'
        }

        self.MixpointOutputStateNames = {
            '00': '1',
            '01': '2',
            '02': '3',
            '03': '4',
            '04': '5',
            '05': '6',
            '06': '7',
            '07': '8',
            '08': 'Aux 1',
            '09': 'Aux 2',
            '10': 'Aux 3',
            '11': 'Aux 4',
            '12': 'Aux 5',
            '13': 'Aux 6',
            '14': 'Aux 7',
            '15': 'Aux 8',
            '32': 'Exp. 1',
            '33': 'Exp. 2',
            '34': 'Exp. 3',
            '35': 'Exp. 4',
            '36': 'Exp. 5',
            '37': 'Exp. 6',
            '38': 'Exp. 7',
            '39': 'Exp. 8',
            '40': 'Exp. 9',
            '41': 'Exp. 10',
            '42': 'Exp. 11',
            '43': 'Exp. 12',
            '44': 'Exp. 13',
            '45': 'Exp. 14',
            '46': 'Exp. 15',
            '47': 'Exp. 16',
            '16': 'V. Send A',
            '17': 'V. Send B',
            '18': 'V. Send C',
            '19': 'V. Send D',
            '20': 'V. Send E',
            '21': 'V. Send F',
            '22': 'V. Send G',
            '23': 'V. Send H',
            '24': 'V. Send I',
            '25': 'V. Send J',
            '26': 'V. Send K',
            '27': 'V. Send L',
            '28': 'V. Send M',
            '29': 'V. Send N',
            '30': 'V. Send O',
            '31': 'V. Send P'
        }

        self.VirtualChannels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', ]

        self.LevelTypes = {
            'ExpansionBusMixpointGain'      : {'Min': -100, 'Max': 12},
            'GroupBassInputFilter'          : {'Min': -24, 'Max': 24},
            'GroupBassVirtualReturnFilter'  : {'Min': -24, 'Max': 24},
            'GroupMicLineInputGain'         : {'Min': -18, 'Max': 80},
            'GroupMixpointGain'             : {'Min': -100, 'Max': 12},
            'GroupOutputAttenuation'        : {'Min': -100, 'Max': 0},
            'GroupPostMixerTrim'            : {'Min': -12, 'Max': 12},
            'GroupPreMixerGain'             : {'Min': -100, 'Max': 12},
            'GroupTrebleInputFilter'        : {'Min': -24, 'Max': 24},
            'GroupTrebleVirtualReturnFilter': {'Min': -24, 'Max': 24},
            'GroupVirtualReturnGain'        : {'Min': -100, 'Max': 12},
            'InputGain'                     : {'Min': -18, 'Max': 80},
            'MixpointGain'                  : {'Min': -100, 'Max': 12},
            'OutputAttenuation'             : {'Min': -100, 'Max': 0},
            'PremixerGain'                  : {'Min': -100, 'Max': 12},
            'VirtualReturnGain'             : {'Min': -100, 'Max': 12},
            'ExpansionInputPremixerGain'    : {'Min': -100, 'Max': 12},
            'AuxInputPremixerGain'          : {'Min': -100, 'Max': 12},
            'AuxInputGain'                  : {'Min': -18, 'Max': 24},
            'OutputPostmixerTrim'           : {'Min': -12, 'Max': 12},
            'AuxOutputPostmixerTrim'        : {'Min': -12, 'Max': 12},
            'AuxOutputGain'                 : {'Min': -100, 'Max': 0},
            'ExpansionOutputPostmixerTrim'  : {'Min': -12, 'Max': 12},
            'ExpansionOutputAttenuation'    : {'Min': -100, 'Max': 0},
            'DigitalInputGain'              : {'Min': -18, 'Max': 24},
        }

        if self.Unidirectional == 'False':
            self.AddMatchString(compile(b'DsJ(590[0-9]{2})\*([0-9]{1,4})\r\n'), self.__MatchAutomixerGateSet, None)
            self.AddMatchString(compile(b'DsV(590[0-9]{2})\*[10]\*([0-9]{1,4})\*?\d?\r\n'),
                                self.__MatchAutomixerGateStatus,
                                None)  # this accounts for old fw and new fw 1.2 (\*?\d?)
            self.AddMatchString(compile(b'VoipAD([1-8]),([0-9]+)\r\n'), self.__MatchAutoAnswerDelay, None)
            self.AddMatchString(compile(b'VoipAA([1-8]),([0-2])\r\n'), self.__MatchAutoAnswerMode, None)
            self.AddMatchString(compile(b'DsG(4001[2-9])\*([0-9 -]{1,5})\r\n'), self.__MatchAuxInputGain, None)
            self.AddMatchString(compile(b'DsM(4001[2-9])\*([01])\r\n'), self.__MatchAuxInputMute, None)
            self.AddMatchString(compile(b'DsG(4011[2-9])\*([0-9 -]{1,5})\r\n'), self.__MatchAuxInputPremixerGain, None)
            self.AddMatchString(compile(b'DsM(4011[2-9])\*([01])\r\n'), self.__MatchAuxInputPremixerMute, None)
            self.AddMatchString(compile(b'DsG(60008|60009|60010|60011|60012|60013|60014|60015)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchAuxOutputGain, None)
            self.AddMatchString(compile(b'DsM(60008|60009|60010|60011|60012|60013|60014|60015)\*([01])\r\n'),
                                self.__MatchAuxOutputMute, None)
            self.AddMatchString(compile(b'DsG(60108|60109|60110|60111|60112|60113|60114|60115)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchAuxOutputPostmixerTrim, None)
            self.AddMatchString(compile(b'VoipIncoming([1-8]),([0-5]),([^,]*),([0-9*#]+),.*\r\n'), self.__MatchCallerID,
                                None)
            self.AddMatchString(compile(b'VoipNAME([1-8]),([0-5]),([^,]*),([0-9*#]+)\r\n'), self.__MatchCallerName,
                                None)
            self.AddMatchString(compile(b'VoipNAME([1-8]),([0-5]),none,none\r\n'), self.__MatchCallerName, 'none')
            self.AddMatchString(compile(b'DsH400([01][0-9])\*([0-9 -]{1,5})\r\n'), self.__MatchDigitalInputGain, None)
            self.AddMatchString(compile(b'Gpi([1-8])\*([0-1])\r\n'), self.__MatchDigitalInputStatus, None)
            self.AddMatchString(compile(b'VoipDND([1-8]),([0-1])\r\n'), self.__MatchDoNotDisturb, None)
            self.AddMatchString(compile(b'VoipDUR([1-8]),([1-8]),([0-9]+)\r\n'), self.__MatchCallDuration, None)
            self.AddMatchString(compile(b'(Pno60-151[1-3]-(01|10))\r\n'), self.__MatchPartNumber, None)
            self.AddMatchString(compile(b'DsG(502[0-9]{2})\*([0-9 -]{1,5})\r\n'),
                                self.__MatchExpansionInputPremixerGain, None)
            self.AddMatchString(compile(b'DsM(502[0-9]{2})\*([01])\r\n'), self.__MatchExpansionInputPremixerMute, None)
            self.AddMatchString(compile(
                b'DsG(60016|60017|60018|60019|60020|60021|60022|60023|60024|60025|60026|60027|60028|60029|60030|60031)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchExpansionOutputAttenuation, None)
            self.AddMatchString(compile(
                b'DsM(60016|60017|60018|60019|60020|60021|60022|60023|60024|60025|60026|60027|60028|60029|60030|60031)\*([01])\r\n'),
                                self.__MatchExpansionOutputMute, None)
            self.AddMatchString(compile(
                b'DsG(60116|60117|60118|60119|60120|60121|60122|60123|60124|60125|60126|60127|60128|60129|60130|60131)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchExpansionOutputPostmixerTrim, None)
            self.AddMatchString(compile(b'GrpmD([0-9]{1,2})\*([0-9 -]{1,5})\r\n'), self.__MatchGroup, None)

            # BEGIN - ADDED BY JDC
            # GrpmV1*198*1445
            self.AddMatchString(compile(b'GrpmV([0-9]{1,2})((?:\*[0-9]{1,4})+)\r\n'), self.__MatchUnsolicitedMeterData, None)
            # END - ADDED BY JDC

            self.AddMatchString(compile(
                b'DsG(40000|40001|40002|40003|40004|40005|40006|40007|40008|40009|40010|40011)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchInputGain, None)
            self.AddMatchString(
                compile(b'DsM(40000|40001|40002|40003|40004|40005|40006|40007|40008|40009|40010|40011)\*([01])\r\n'),
                self.__MatchInputMute, None)
            self.AddMatchString(compile(b'DsV(400[01][0-9])\*[01]\*([0-9]{1,4})\*[01]\r\n'),
                                self.__MatchInputSignalLevelMonitor, None)
            self.AddMatchString(compile(b'DsG2([0-9]{2})([0-9]{2})\*([0-9 -]{1,5})\r\n'), self.__MatchMixpointGain,
                                None)
            self.AddMatchString(compile(b'DsM2([0-9]{2})([0-9]{2})\*([01])\r\n'), self.__MatchMixpointMute, None)
            self.AddMatchString(compile(b'DsM(6000[0-7])\*([01])\r\n'), self.__MatchOutputMute, None)
            self.AddMatchString(compile(b'DsG(6010[0-7])\*([0-9 -]{1,5})\r\n'), self.__MatchOutputPostmixerTrim, None)
            self.AddMatchString(compile(b'DsG(6000[0-7])\*([0-9 -]{1,5})\r\n'), self.__MatchOutputAttenuation, None)
            self.AddMatchString(compile(b'DsZ4000([0-7])\*([01])\r\n'), self.__MatchPhantomPower, None)
            self.AddMatchString(compile(b'Play([1-8])\*([01])\r\n'), self.__MatchPlayerControl, None)
            self.AddMatchString(compile(b'CplyA([1-8])\*([ \s\S]+?)\r\n'), self.__MatchPlayerFilenameStatus, None)
            self.AddMatchString(compile(b'CplyM([1-8])\*([01])\r\n'), self.__MatchPlayerRepeat, None)
            self.AddMatchString(compile(
                b'DsG(40100|40101|40102|40103|40104|40105|40106|40107|40108|40109|40110|40111)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchPremixerGain, None)
            self.AddMatchString(
                compile(b'DsM(40100|40101|40102|40103|40104|40105|40106|40107|40108|40109|40110|40111)\*([01])\r\n'),
                self.__MatchPremixerMute, None)
            self.AddMatchString(compile(
                b'DsG(50100|50101|50102|50103|50104|50105|50106|50107|50108|50109|50110|50111|50112|50113|50114|50115)\*([0-9 -]{1,5})\r\n'),
                                self.__MatchVirtualReturnGain, None)
            self.AddMatchString(compile(
                b'DsM(50100|50101|50102|50103|50104|50105|50106|50107|50108|50109|50110|50111|50112|50113|50114|50115)\*([01])\r\n'),
                                self.__MatchVirtualReturnMute, None)
            self.AddMatchString(
                compile(b'VoipLS([1-8]),([0-5]),([0-5]),([0-5]),([0-5]),([0-5]),([0-5]),([0-5]),([0-5])\r\n'),
                self.__MatchCallStatus, 'LineStatus')
            self.AddMatchString(compile(b'Voip(Busy|Rejected|Unreachable|Terminated)([1-8]),([1-8])\r\n'),
                                self.__MatchCallStatus, 'CallStatus')
            self.AddMatchString(compile(b'VoipRS([1-8]),([0-4])\r\n'), self.__MatchRegistrationStatus, None)
            self.AddMatchString(compile(b'VoipREJ([1-8]),([1-8]),[01]\r\n'), self.__MatchReject, None)
            self.AddMatchString(compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)
            self.AddMatchString(compile(b'E([0-9]{2})\r\n'), self.__MatchError, None)

            if 'Serial' not in self.ConnectionType:
                self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
                self.AddMatchString(compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
                self.AddMatchString(compile(b'Login User\r\n'), self.__MatchLoginUser, None)


    # BEGIN - ADDED BY JDC
    def __MatchUnsolicitedMeterData(self, match, tag):
        SignalFloorThreshold = 850

        for i, value in enumerate(match.group(2).decode().split('*')[1:]):
            value = int(value)
            qualifier = {'OID': i}

            if value < SignalFloorThreshold:
                self.WriteStatus('UnsolicitedMeterData', value, qualifier)
            else:
                self.WriteStatus('UnsolicitedMeterData', SignalFloorThreshold, qualifier)


    def SetUnsolicitedMeterGroupNumber(self, value, qualifier):
        if 0 < int(value) < 65:
            UnsolicitedMeterGroupNumberCmdString = '\x1BG{0}GRPU\r\n'.format(value)
            self.__SetHelper('UnsolicitedMeterGroupNumber', UnsolicitedMeterGroupNumberCmdString, value, qualifier)

        else:
            self.Discard('Invalid Command for SetUnsolicitedMeterGroupNumber')

    # END - ADDED BY JDC

    def UpdatePartNumber(self, value, qualifier):
        cmdString = 'n'
        self.__UpdateHelper('PartNumber', cmdString, None, None)

    def __MatchPartNumber(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('PartNumber', value, None)

    def SetPassword(self):
        if self.devicePassword:
            self.Send('{0}\r\n'.format(self.devicePassword))
        else:
            self.MissingCredentialsLog('Password')

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 1:
            self.Error(['Log in failed. Please supply proper Admin password'])
            self.Authenticated = 'None'
        else:
            self.SetPassword()

    def __MatchLoginAdmin(self, match, tag):

        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):

        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        self.Error(['Logged in as User. May have limited functionality.'])

    ####################################################
    def __MatchVerboseMode(self, match, qualifier):
        self.OnConnected()
        self.VerboseDisabled = False

    ####################################################
    def __MatchReject(self, match, qualifier):
        Line = match.group(1).decode()
        Appearance = match.group(2).decode()
        self.WriteStatus('CallStatus', 'Inactive', {'Line': Line, 'Appearance': Appearance})

        ####################################################

    def SetAutoAnswerDelay(self, value, qualifier):

        if 0 < int(qualifier['Line']) < 9:
            AutoAnswerDelayCmdString = '\x1BAD{0},{1}VOIP\r\n'.format(qualifier['Line'], value)
            self.__SetHelper('AutoAnswerDelay', AutoAnswerDelayCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAutoAnswerDelay')

    def UpdateAutoAnswerDelay(self, value, qualifier):

        if 0 < int(qualifier['Line']) < 9:
            AutoAnswerDelayCmdString = '\x1BAD{0}VOIP\r\n'.format(qualifier['Line'])
            self.__UpdateHelper('AutoAnswerDelay', AutoAnswerDelayCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAutoAnswerDelay')

    def __MatchAutoAnswerDelay(self, match, tag):

        Line = match.group(1).decode()
        value = match.group(2).decode()
        self.WriteStatus('AutoAnswerDelay', '{0}'.format(value), {'Line': Line})

    def SetAutoAnswerMode(self, value, qualifier):

        ValueStateValues = {
            'Disable'          : '0',
            'Delay'            : '1',
            'Follow SIP Header': '2'
        }
        if 0 < int(qualifier['Line']) < 9:
            AutoAnswerModeCmdString = '\x1BAA{0},{1}VOIP\r\n'.format(qualifier['Line'], ValueStateValues[value])
            self.__SetHelper('AutoAnswerMode', AutoAnswerModeCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAutoAnswerMode')

    def UpdateAutoAnswerMode(self, value, qualifier):

        if 0 < int(qualifier['Line']) < 9:
            AutoAnswerModeCmdString = '\x1BAA{0}VOIP\r\n'.format(qualifier['Line'])
            self.__UpdateHelper('AutoAnswerMode', AutoAnswerModeCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAutoAnswerMode')

    def __MatchAutoAnswerMode(self, match, tag):

        ValueStateValues = {
            '0': 'Disable',
            '1': 'Delay',
            '2': 'Follow SIP Header',
        }
        Line = match.group(1).decode()
        value = match.group(2).decode()
        self.WriteStatus('AutoAnswerMode', ValueStateValues[value], {'Line': Line})

    def SetAutomixerGateSet(self, value, qualifier):

        InputStates = {
            'Aux 1'  : '59012',
            'Aux 2'  : '59013',
            'Aux 3'  : '59014',
            'Aux 4'  : '59015',
            'Aux 5'  : '59016',
            'Aux 6'  : '59017',
            'Aux 7'  : '59018',
            'Aux 8'  : '59019',
            'Mic 1'  : '59000',
            'Mic 2'  : '59001',
            'Mic 3'  : '59002',
            'Mic 4'  : '59003',
            'Mic 5'  : '59004',
            'Mic 6'  : '59005',
            'Mic 7'  : '59006',
            'Mic 8'  : '59007',
            'Mic 9'  : '59008',
            'Mic 10' : '59009',
            'Mic 11' : '59010',
            'Mic 12' : '59011',
            'Exp. 1' : '59020',
            'Exp. 2' : '59021',
            'Exp. 3' : '59022',
            'Exp. 4' : '59023',
            'Exp. 5' : '59024',
            'Exp. 6' : '59025',
            'Exp. 7' : '59026',
            'Exp. 8' : '59027',
            'Exp. 9' : '59028',
            'Exp. 10': '59029',
            'Exp. 11': '59030',
            'Exp. 12': '59031',
            'Exp. 13': '59032',
            'Exp. 14': '59033',
            'Exp. 15': '59034',
            'Exp. 16': '59035',
            'Exp. 17': '59036',
            'Exp. 18': '59037',
            'Exp. 19': '59038',
            'Exp. 20': '59039',
            'Exp. 21': '59040',
            'Exp. 22': '59041',
            'Exp. 23': '59042',
            'Exp. 24': '59043',
            'Exp. 25': '59044',
            'Exp. 26': '59045',
            'Exp. 27': '59046',
            'Exp. 28': '59047',
            'Exp. 29': '59048',
            'Exp. 30': '59049',
            'Exp. 31': '59050',
            'Exp. 32': '59051',
            'Exp. 33': '59052',
            'Exp. 34': '59053',
            'Exp. 35': '59054',
            'Exp. 36': '59055',
            'Exp. 37': '59056',
            'Exp. 38': '59057',
            'Exp. 39': '59058',
            'Exp. 40': '59059',
            'Exp. 41': '59060',
            'Exp. 42': '59061',
            'Exp. 43': '59062',
            'Exp. 44': '59063',
            'Exp. 45': '59064',
            'Exp. 46': '59065',
            'Exp. 47': '59066',
            'Exp. 48': '59067'
        }

        ValueStateValues = {
            'Enable' : 1024,
            'Disable': 0
        }

        newinput = InputStates[qualifier['Input']]
        if newinput:
            AutomixerGateSetCmdString = 'wj{0}*{1}Au\r'.format(newinput, ValueStateValues[value])
            self.__SetHelper('AutomixerGateSet', AutomixerGateSetCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAutomixerGateSet')

    def __MatchAutomixerGateSet(self, match, tag):

        InputStates = {
            '59012': 'Aux 1',
            '59013': 'Aux 2',
            '59014': 'Aux 3',
            '59015': 'Aux 4',
            '59016': 'Aux 5',
            '59017': 'Aux 6',
            '59018': 'Aux 7',
            '59019': 'Aux 8',
            '59000': 'Mic 1',
            '59001': 'Mic 2',
            '59002': 'Mic 3',
            '59003': 'Mic 4',
            '59004': 'Mic 5',
            '59005': 'Mic 6',
            '59006': 'Mic 7',
            '59007': 'Mic 8',
            '59008': 'Mic 9',
            '59009': 'Mic 10',
            '59010': 'Mic 11',
            '59011': 'Mic 12',
            '59020': 'Exp. 1',
            '59021': 'Exp. 2',
            '59022': 'Exp. 3',
            '59023': 'Exp. 4',
            '59024': 'Exp. 5',
            '59025': 'Exp. 6',
            '59026': 'Exp. 7',
            '59027': 'Exp. 8',
            '59028': 'Exp. 9',
            '59029': 'Exp. 10',
            '59030': 'Exp. 11',
            '59031': 'Exp. 12',
            '59032': 'Exp. 13',
            '59033': 'Exp. 14',
            '59034': 'Exp. 15',
            '59035': 'Exp. 16',
            '59036': 'Exp. 17',
            '59037': 'Exp. 18',
            '59038': 'Exp. 19',
            '59039': 'Exp. 20',
            '59040': 'Exp. 21',
            '59041': 'Exp. 22',
            '59042': 'Exp. 23',
            '59043': 'Exp. 24',
            '59044': 'Exp. 25',
            '59045': 'Exp. 26',
            '59046': 'Exp. 27',
            '59047': 'Exp. 28',
            '59048': 'Exp. 29',
            '59049': 'Exp. 30',
            '59050': 'Exp. 31',
            '59051': 'Exp. 32',
            '59052': 'Exp. 33',
            '59053': 'Exp. 34',
            '59054': 'Exp. 35',
            '59055': 'Exp. 36',
            '59056': 'Exp. 37',
            '59057': 'Exp. 38',
            '59058': 'Exp. 39',
            '59059': 'Exp. 40',
            '59060': 'Exp. 41',
            '59061': 'Exp. 42',
            '59062': 'Exp. 43',
            '59063': 'Exp. 44',
            '59064': 'Exp. 45',
            '59065': 'Exp. 46',
            '59066': 'Exp. 47',
            '59067': 'Exp. 48'
        }
        channel = match.group(1).decode()
        qualifier = {'Input': InputStates[channel]}
        value = int(match.group(2))
        if value >= 1024:
            self.WriteStatus('AutomixerGateSet', 'Enable', qualifier)
        else:
            self.WriteStatus('AutomixerGateSet', 'Disable', qualifier)
            self.WriteStatus('AutomixerGateStatus', 'Off', qualifier)

    def __MatchAutomixerGateStatus(self, match, tag):

        InputStates = {
            '59012': 'Aux 1',
            '59013': 'Aux 2',
            '59014': 'Aux 3',
            '59015': 'Aux 4',
            '59016': 'Aux 5',
            '59017': 'Aux 6',
            '59018': 'Aux 7',
            '59019': 'Aux 8',
            '59000': 'Mic 1',
            '59001': 'Mic 2',
            '59002': 'Mic 3',
            '59003': 'Mic 4',
            '59004': 'Mic 5',
            '59005': 'Mic 6',
            '59006': 'Mic 7',
            '59007': 'Mic 8',
            '59008': 'Mic 9',
            '59009': 'Mic 10',
            '59010': 'Mic 11',
            '59011': 'Mic 12',
            '59020': 'Exp. 1',
            '59021': 'Exp. 2',
            '59022': 'Exp. 3',
            '59023': 'Exp. 4',
            '59024': 'Exp. 5',
            '59025': 'Exp. 6',
            '59026': 'Exp. 7',
            '59027': 'Exp. 8',
            '59028': 'Exp. 9',
            '59029': 'Exp. 10',
            '59030': 'Exp. 11',
            '59031': 'Exp. 12',
            '59032': 'Exp. 13',
            '59033': 'Exp. 14',
            '59034': 'Exp. 15',
            '59035': 'Exp. 16',
            '59036': 'Exp. 17',
            '59037': 'Exp. 18',
            '59038': 'Exp. 19',
            '59039': 'Exp. 20',
            '59040': 'Exp. 21',
            '59041': 'Exp. 22',
            '59042': 'Exp. 23',
            '59043': 'Exp. 24',
            '59044': 'Exp. 25',
            '59045': 'Exp. 26',
            '59046': 'Exp. 27',
            '59047': 'Exp. 28',
            '59048': 'Exp. 29',
            '59049': 'Exp. 30',
            '59050': 'Exp. 31',
            '59051': 'Exp. 32',
            '59052': 'Exp. 33',
            '59053': 'Exp. 34',
            '59054': 'Exp. 35',
            '59055': 'Exp. 36',
            '59056': 'Exp. 37',
            '59057': 'Exp. 38',
            '59058': 'Exp. 39',
            '59059': 'Exp. 40',
            '59060': 'Exp. 41',
            '59061': 'Exp. 42',
            '59062': 'Exp. 43',
            '59063': 'Exp. 44',
            '59064': 'Exp. 45',
            '59065': 'Exp. 46',
            '59066': 'Exp. 47',
            '59067': 'Exp. 48'
        }

        channel = match.group(1).decode()
        qualifier = {'Input': InputStates[channel]}
        value = int(match.group(2))
        if value >= 1024:
            self.WriteStatus('AutomixerGateStatus', 'On', qualifier)
        else:
            self.WriteStatus('AutomixerGateStatus', 'Off', qualifier)

    def SetAuxInputGain(self, value, qualifier):
        channel = qualifier['Input']
        if 0 < int(channel) < 9 and self.__CheckValidLevelValue('AuxInputGain', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 40011
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('AuxInputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxInputGain')

    def UpdateAuxInputGain(self, value, qualifier):

        channel = qualifier['Input']
        if 0 < int(channel) < 9:
            ChannelValue = int(channel) + 40011
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('AuxInputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxInputGain')

    def __MatchAuxInputGain(self, match, tag):

        channel = str(int(match.group(1)) - 40011)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('AuxInputGain', value, qualifier)

    def SetAuxInputMute(self, value, qualifier):

        ValueStateValues = {
            'On' : '1',
            'Off': '0'
        }

        channel = int(qualifier['Input'])
        if 1 <= channel <= 8:
            commandString = 'wM{0}*{1}AU\r\n'.format(int(channel) + 40011, ValueStateValues[value])
            self.__SetHelper('AuxInputMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxInputMute')

    def UpdateAuxInputMute(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 8:
            AuxInputMuteCmdString = 'wM{0}AU\r\n'.format(int(channel) + 40011)
            self.__UpdateHelper('AuxInputMute', AuxInputMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxInputMute')

    def __MatchAuxInputMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 40011)
        qualifier = {'Input': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('AuxInputMute', value, qualifier)

    def SetAuxInputPremixerGain(self, value, qualifier):

        channel = qualifier['Input']
        if 0 < int(channel) <= 8 and self.__CheckValidLevelValue('AuxInputPremixerGain', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 40111
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('AuxInputPremixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxInputPremixerGain')

    def UpdateAuxInputPremixerGain(self, value, qualifier):

        channel = qualifier['Input']
        if 0 < int(channel) <= 8:
            ChannelValue = int(channel) + 40111
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('AuxInputPremixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxInputPremixerGain')

    def __MatchAuxInputPremixerGain(self, match, tag):

        channel = str(int(match.group(1)) - 40111)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('AuxInputPremixerGain', value, qualifier)

    def SetAuxInputPremixerMute(self, value, qualifier):

        ValueStateValues = {
            'On' : '1',
            'Off': '0'
        }

        channel = qualifier['Input']
        if 0 < int(channel) <= 8:
            AuxInputPremixerMuteCmdString = 'wM{0}*{1}AU\r\n'.format(int(channel) + 40111, ValueStateValues[value])
            self.__SetHelper('AuxInputPremixerMute', AuxInputPremixerMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxInputPremixerMute')

    def UpdateAuxInputPremixerMute(self, value, qualifier):

        channel = qualifier['Input']
        if 0 < int(channel) <= 8:
            AuxInputPremixerMuteCmdString = 'wM{0}AU\r\n'.format(int(channel) + 40111)
            self.__UpdateHelper('AuxInputPremixerMute', AuxInputPremixerMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxInputPremixerMute')

    def __MatchAuxInputPremixerMute(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 40111)
        qualifier = {'Input': channel}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('AuxInputPremixerMute', value, qualifier)

    def SetAuxOutputGain(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) <= self.MAX_AUX_OUTPUTS and self.__CheckValidLevelValue('AuxOutputGain', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 60007
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('AuxOutputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxOutputGain')

    def UpdateAuxOutputGain(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) <= self.MAX_AUX_OUTPUTS:
            ChannelValue = int(channel) + 60007
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('AuxOutputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxOutputGain')

    def __MatchAuxOutputGain(self, match, tag):

        channel = str(int(match.group(1)) - 60007)
        qualifier = {'Output': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('AuxOutputGain', value, qualifier)

    def SetAuxOutputMute(self, value, qualifier):

        ValueStateValues = {
            'On' : '1',
            'Off': '0'
        }
        channel = qualifier['Output']
        if 0 < int(channel) <= self.MAX_AUX_OUTPUTS:
            AuxOutputMuteCmdString = 'wM{0}*{1}AU\r\n'.format(int(channel) + 60007, ValueStateValues[value])
            self.__SetHelper('AuxOutputMute', AuxOutputMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxOutputMute')

    def UpdateAuxOutputMute(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) <= self.MAX_AUX_OUTPUTS:
            AuxOutputMuteCmdString = 'wM{0}AU\r\n'.format(int(channel) + 60007)
            self.__UpdateHelper('AuxOutputMute', AuxOutputMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxOutputMute')

    def __MatchAuxOutputMute(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 60007)
        qualifier = {'Output': channel}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('AuxOutputMute', value, qualifier)

    def SetAuxOutputPostmixerTrim(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) <= self.MAX_AUX_OUTPUTS and self.__CheckValidLevelValue('AuxOutputPostmixerTrim', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 60107
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('AuxOutputPostmixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetAuxOutputPostmixerTrim')

    def UpdateAuxOutputPostmixerTrim(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) <= self.MAX_AUX_OUTPUTS:
            ChannelValue = int(channel) + 60107
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('AuxOutputPostmixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateAuxOutputPostmixerTrim')

    def __MatchAuxOutputPostmixerTrim(self, match, tag):

        channel = str(int(match.group(1)) - 60107)
        qualifier = {'Output': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('AuxOutputPostmixerTrim', value, qualifier)

    def __MatchCallerID(self, match, tag):

        Line = match.group(1).decode()
        Appaerance = match.group(2).decode()
        name = match.group(3).decode()
        extension = match.group(4).decode()
        self.WriteStatus('CallerID', '{0} X{1}'.format(name, extension), {'Line': Line, 'Appearance': Appaerance})

    def UpdateCallerName(self, value, qualifier):

        ctime = time.monotonic()
        if ctime - self.lastCallerNameUpdate > 3:
            self.lastCallerNameUpdate = 0
            if 0 < int(qualifier['Line']) < 9 and 0 < int(qualifier['Appearance']):
                cmdString = '\x1BNAME{0},{1}VOIP\r\n'.format(qualifier['Line'], qualifier['Appearance'])
                self.__UpdateHelper('CallerName', cmdString, value, qualifier)
            else:
                self.Discard('Invalid Command for UpdateCallerName')
        else:
            self.Discard('Invalid Command for UpdateCallerName')

    def __MatchCallerName(self, match, tag):

        lineValue = match.group(1).decode()
        appearanceValue = match.group(2).decode()

        if tag == 'none':
            self.WriteStatus('CallerName', '', {'Line': lineValue, 'Appearance': appearanceValue})
            self.WriteStatus('CallerExtension', '', {'Line': lineValue, 'Appearance': appearanceValue})
        else:
            name = match.group(3).decode()
            extension = match.group(4).decode()
            self.WriteStatus('CallerName', name, {'Line': lineValue, 'Appearance': appearanceValue})
            self.WriteStatus('CallerExtension', extension, {'Line': lineValue, 'Appearance': appearanceValue})

    def UpdateCallStatus(self, value, qualifier):

        if 8 < int(qualifier['Line']) < 1:
            self.Discard('Invalid Command for UpdateCallStatus')
        elif 8 < int(qualifier['Appearance']) < 1:
            self.Discard('Invalid Command for UpdateCallStatus')
        else:

            cmdString = '\x1BLS{0}VOIP\r\n'.format(qualifier['Line'])
            self.__UpdateHelper('CallStatus', cmdString, value, qualifier)

    def __MatchCallStatus(self, match, tag):

        DigitalInputStates = {
            '0': 'N/A',
            '1': 'Inactive',
            '2': 'Active',
            '3': 'On Hold',
            '4': 'Incoming',
            '5': 'Outgoing',
        }

        if tag == 'LineStatus':
            Line = match.group(1).decode()
            Appaerance1 = match.group(2).decode()
            Appaerance2 = match.group(3).decode()
            Appaerance3 = match.group(4).decode()
            Appaerance4 = match.group(5).decode()
            Appaerance5 = match.group(6).decode()
            Appaerance6 = match.group(7).decode()
            Appaerance7 = match.group(8).decode()
            Appaerance8 = match.group(9).decode()

            if Appaerance1 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '1'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance1], {'Line': Line, 'Appearance': '1'})
            if Appaerance2 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '2'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance2], {'Line': Line, 'Appearance': '2'})
            if Appaerance3 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '3'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance3], {'Line': Line, 'Appearance': '3'})
            if Appaerance4 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '4'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance4], {'Line': Line, 'Appearance': '4'})
            if Appaerance5 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '5'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance5], {'Line': Line, 'Appearance': '5'})
            if Appaerance6 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '6'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance6], {'Line': Line, 'Appearance': '6'})
            if Appaerance7 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '7'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance7], {'Line': Line, 'Appearance': '7'})
            if Appaerance8 != '4':
                self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': '8'})
            self.WriteStatus('CallStatus', DigitalInputStates[Appaerance8], {'Line': Line, 'Appearance': '8'})
        else:
            Line = match.group(2).decode()
            Appaerance = match.group(3).decode()
            value = match.group(1).decode()
            self.WriteStatus('CallerID', '', {'Line': Line, 'Appearance': Appaerance})
            self.WriteStatus('CallStatus', value, {'Line': Line, 'Appearance': Appaerance})

    def UpdateCallDuration(self, value, qualifier):

        if 1 <= int(qualifier['Line']) <= 8 and 1 <= int(qualifier['Appearance']) <= 8:
            CallDurationCmdString = '\x1BDUR{0},{1}VOIP\r\n'.format(qualifier['Line'], qualifier['Appearance'])
            self.__UpdateHelper('CallDuration', CallDurationCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateCallDuration')

    def __MatchCallDuration(self, match, tag):

        lineValue = match.group(1).decode()
        appearanceValue = match.group(2).decode()

        if int(match.group(3).decode()) == 0:
            self.WriteStatus('CallDuration', '', {'Line': lineValue, 'Appearance': appearanceValue})
        else:
            minutes, seconds = divmod(int(match.group(3).decode()), 60)
            hours, minutes = divmod(minutes, 60)
            duration = '%02d:%02d:%02d' % (hours, minutes, seconds)
            self.WriteStatus('CallDuration', duration, {'Line': lineValue, 'Appearance': appearanceValue})

    def UpdateCallerExtension(self, value, qualifier):

        self.UpdateCallerName(value, qualifier)

    def SetDoNotDisturb(self, value, qualifier):

        ValueStateValues = {
            'Disable': '0',
            'Enable' : '1',
        }
        if 8 < int(qualifier['Line']) < 1:
            self.Discard('Invalid Command for SetDoNotDisturb')
        else:
            DoNotDisturbCmdString = '\x1BDND{0},{1}VOIP\r\n'.format(qualifier['Line'], ValueStateValues[value])
            self.__SetHelper('DoNotDisturb', DoNotDisturbCmdString, value, qualifier)

    def UpdateDoNotDisturb(self, value, qualifier):

        DoNotDisturbCmdString = '\x1BDND{0}VOIP\r\n'.format(qualifier['Line'])
        self.__UpdateHelper('DoNotDisturb', DoNotDisturbCmdString, value, qualifier)

    def __MatchDoNotDisturb(self, match, tag):

        ValueStateValues = {
            '0': 'Disable',
            '1': 'Enable',
        }
        Line = match.group(1).decode()
        value = match.group(2).decode()
        self.WriteStatus('DoNotDisturb', '{0}'.format(ValueStateValues[value]), {'Line': Line})

    def SetDial(self, value, qualifier):

        if value == 'Dial':
            number = qualifier['Number']
            if number:
                self.__SetHelper('Dial', '\x1BDIAL{0},{1}VOIP\r\n'.format(qualifier['Line'], number), value, qualifier)
                try:
                    self.ReDialString = qualifier
                except:
                    self.ReDialString = ''
                    self.ReDialString = qualifier
        elif value == 'Redial':
            try:
                if self.ReDialString:
                    self.__SetHelper('Dial', self.ReDialString, value, qualifier)
                else:
                    self.Error(['Invalid Command'])
            except KeyError:
                self.ReDialString = ''

        elif value == 'Clear Redial':
            try:
                if self.ReDialString:
                    self.ReDialString = ''

            except KeyError:
                self.ReDialString = ''

    def SetDialDTMF(self, value, qualifier):

        self.__SetHelper('DialDTMF',
                         '\x1BDD{0},{1},{2}VOIP\r\n'.format(qualifier['Line'], qualifier['Appearance'], value), value,
                         qualifier)

    def UpdateDigitalInputStatus(self, value, qualifier):

        if 1 <= int(qualifier['Input']) <= 8:
            cmdString = '\x1B{0}GPI\r\n'.format(qualifier['Input'])
            self.__UpdateHelper('DigitalInputStatus', cmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateDigitalInputStatus')

    def __MatchDigitalInputStatus(self, match, tag):

        DigitalInputStates = {
            '0': 'Logic Low',
            '1': 'Logic High'
        }

        Value = match.group(2).decode()
        qualifier = {'Input': match.group(1).decode()}
        self.WriteStatus('DigitalInputStatus', DigitalInputStates[Value], qualifier)

    def SetDigitalInputGain(self, value, qualifier):
        channel = int(qualifier['Input'])
        if 1 <= channel <= 12 and self.__CheckValidLevelValue('DigitalInputGain', value):
            level = round(value * 10)
            DigitalInputGainCmdString = 'wH{0}*{1:05d}AU\r\n'.format(channel + 39999, level)
            self.__SetHelper('DigitalInputGain', DigitalInputGainCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def UpdateDigitalInputGain(self, value, qualifier):
        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            DigitalInputGainCmdString = 'wH{0}AU\r\n'.format(channel + 39999)
            self.__UpdateHelper('DigitalInputGain', DigitalInputGainCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def __MatchDigitalInputGain(self, match, tag):
        channel = str(int(match.group(1)) + 1)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('DigitalInputGain', value, qualifier)

    def SetExpansionBusMixpointGain(self, value, qualifier):

        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.ExpansionBusInputStateValues and Output in self.MixpointOutputStateValues and self.__CheckValidLevelValue(
                'MixpointGain', value):
            inputValue = self.ExpansionBusInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            level = round(value * 10)
            commandString = 'wG2{0}{1}*{2:05d}AU\r\n'.format(inputValue, outputValue, level)
            self.__SetHelper('ExpansionBusMixpointGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetExpansionBusMixpointGain')

    def UpdateExpansionBusMixpointGain(self, value, qualifier):
        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.ExpansionBusInputStateValues and Output in self.MixpointOutputStateValues:
            inputValue = self.ExpansionBusInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            commandString = 'wG2{0}{1}AU\r\n'.format(inputValue, outputValue)
            self.__UpdateHelper('ExpansionBusMixpointGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def SetExpansionBusMixpointMute(self, value, qualifier):

        ValueStateValues = {
            'On' : '1',
            'Off': '0'
        }
        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.ExpansionBusInputStateValues and Output in self.MixpointOutputStateValues:
            inputValue = self.ExpansionBusInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            ExpansionBusMixpointMuteCmdString = 'wM2{0}{1}*{2}AU\r\n'.format(inputValue, outputValue,
                                                                             ValueStateValues[value])
            self.__SetHelper('ExpansionBusMixpointMute', ExpansionBusMixpointMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def UpdateExpansionBusMixpointMute(self, value, qualifier):
        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.ExpansionBusInputStateValues and Output in self.MixpointOutputStateValues:
            inputValue = self.ExpansionBusInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            ExpansionBusMixpointMuteCmdString = 'wM2{0}{1}AU\r\n'.format(inputValue, outputValue)
            self.__UpdateHelper('ExpansionBusMixpointMute', ExpansionBusMixpointMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def SetExpansionInputPremixerGain(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= self.MAX_EXPANSION_INPUTS and self.__CheckValidLevelValue('ExpansionInputPremixerGain',
                                                                                     value):
            level = round(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 50199, level)
            self.__SetHelper('ExpansionInputPremixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetExpansionInputPremixerGain')

    def UpdateExpansionInputPremixerGain(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= self.MAX_EXPANSION_INPUTS:
            commandString = 'wG{0}AU\r\n'.format(channel + 50199)
            self.__UpdateHelper('ExpansionInputPremixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateExpansionInputPremixerGain')

    def __MatchExpansionInputPremixerGain(self, match, tag):

        channel = str(int(match.group(1)) - 50199)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('ExpansionInputPremixerGain', value, qualifier)

    def SetExpansionInputPremixerMute(self, value, qualifier):

        ValueStateValues = {
            'On' : '1',
            'Off': '0'
        }

        channel = int(qualifier['Input'])
        if 1 <= channel <= self.MAX_EXPANSION_INPUTS:
            ExpansionInputPremixerMuteCmdString = 'wM{0}*{1}AU\r\n'.format(int(channel) + 50199,
                                                                           ValueStateValues[value])
            self.__SetHelper('ExpansionInputPremixerMute', ExpansionInputPremixerMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetExpansionInputPremixerMute')

    def UpdateExpansionInputPremixerMute(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= self.MAX_EXPANSION_INPUTS:
            ExpansionInputPremixerMuteCmdString = 'wM{0}AU\r\n'.format(int(channel) + 50199)
            self.__UpdateHelper('ExpansionInputPremixerMute', ExpansionInputPremixerMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateExpansionInputPremixerMute')

    def __MatchExpansionInputPremixerMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 50199)
        qualifier = {'Input': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('ExpansionInputPremixerMute', value, qualifier)

    def SetExpansionOutputAttenuation(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) < 17 and self.__CheckValidLevelValue('ExpansionOutputAttenuation', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 60015
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('ExpansionOutputAttenuation', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetExpansionOutputAttenuation')

    def UpdateExpansionOutputAttenuation(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) < 17:
            ChannelValue = int(channel) + 60015
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('ExpansionOutputAttenuation', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateExpansionOutputAttenuation')

    def __MatchExpansionOutputAttenuation(self, match, tag):

        channel = str(int(match.group(1)) - 60015)
        qualifier = {'Output': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('ExpansionOutputAttenuation', value, qualifier)

    def SetExpansionOutputMute(self, value, qualifier):

        ValueStateValues = {
            'On' : '1',
            'Off': '0'
        }

        channel = qualifier['Output']
        if 0 < int(channel) <= 16:
            ExpansionOutputMuteCmdString = 'wM{0}*{1}AU\r\n'.format(int(channel) + 60015, ValueStateValues[value])
            self.__SetHelper('ExpansionOutputMute', ExpansionOutputMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetExpansionOutputMute')

    def UpdateExpansionOutputMute(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) <= 16:
            ExpansionOutputMuteCmdString = 'wM{0}AU\r\n'.format(int(channel) + 60015)
            self.__UpdateHelper('ExpansionOutputMute', ExpansionOutputMuteCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateExpansionOutputMute')

    def __MatchExpansionOutputMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 60015)
        qualifier = {'Output': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('ExpansionOutputMute', value, qualifier)

    def SetExpansionOutputPostmixerTrim(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) < 17 and self.__CheckValidLevelValue('ExpansionOutputPostmixerTrim', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 60115
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('ExpansionOutputPostmixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetExpansionOutputPostmixerTrim')

    def UpdateExpansionOutputPostmixerTrim(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) < 17:
            ChannelValue = int(channel) + 60115
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('ExpansionOutputPostmixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateExpansionOutputPostmixerTrim')

    def __MatchExpansionOutputPostmixerTrim(self, match, tag):

        channel = str(int(match.group(1)) - 60115)
        qualifier = {'Output': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('ExpansionOutputPostmixerTrim', value, qualifier)

    def SetGroupMicLineInputGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupMicLineInputGain', value):
            level = round(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupMicLineInputGain'
            self.__SetHelper('GroupMicLineInputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupMicLineInputGain')

    def UpdateGroupMicLineInputGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupMicLineInputGain'
            self.__UpdateHelper('GroupMicLineInputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupMicLineInputGain')

    def SetGroupBassInputFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupBassInputFilter', value):
            level = round(value * 10)
            GroupBassInputFilterCmdString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupBassInputFilter'
            self.__SetHelper('GroupBassInputFilter', GroupBassInputFilterCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupBassInputFilter')

    def UpdateGroupBassInputFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            GroupBassInputFilterCmdString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupBassInputFilter'
            self.__UpdateHelper('GroupBassInputFilter', GroupBassInputFilterCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupBassInputFilter')

    def SetGroupBassVirtualReturnFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupBassVirtualReturnFilter', value):
            level = round(value * 10)
            GroupBassVirtualReturnFilterCmdString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupBassVirtualReturnFilter'
            self.__SetHelper('GroupBassVirtualReturnFilter', GroupBassVirtualReturnFilterCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupBassVirtualReturnFilter')

    def UpdateGroupBassVirtualReturnFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            GroupBassVirtualReturnFilterCmdString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupBassVirtualReturnFilter'
            self.__UpdateHelper('GroupBassVirtualReturnFilter', GroupBassVirtualReturnFilterCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupBassVirtualReturnFilter')

    def SetGroupMixpointGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupMixpointGain', value):
            level = round(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupMixpointGain'
            self.__SetHelper('GroupMixpointGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupMixpointGain')

    def UpdateGroupMixpointGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupMixpointGain'
            self.__UpdateHelper('GroupMixpointGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupMixpointGain')

    def SetGroupMute(self, value, qualifier):

        GroupMuteStateValues = {
            'On' : '1',
            'Off': '0'
        }
        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}*{1}grpm\r\n'.format(group, GroupMuteStateValues[value])
            self.GroupFunction[group] = 'GroupMute'
            self.__SetHelper('GroupMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupMute')

    def UpdateGroupMute(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupMute'
            self.__UpdateHelper('GroupMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupMute')

    def SetGroupOutputAttenuation(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupOutputAttenuation', value):
            level = round(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupOutputAttenuation'
            self.__SetHelper('GroupOutputAttenuation', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupOutputAttenuation')

    def UpdateGroupOutputAttenuation(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupOutputAttenuation'
            self.__UpdateHelper('GroupOutputAttenuation', commandString, value, qualifier)

    def SetGroupPostMixerTrim(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupPostMixerTrim', value):
            level = round(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupPostMixerTrim'
            self.__SetHelper('GroupPostMixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupPostMixerTrim')

    def UpdateGroupPostMixerTrim(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupPostMixerTrim'
            self.__UpdateHelper('GroupPostMixerTrim', commandString, value, qualifier)

    def SetGroupPreMixerGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupPreMixerGain', value):
            level = round(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupPreMixerGain'
            self.__SetHelper('GroupPreMixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupPreMixerGain')

    def UpdateGroupPreMixerGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupPreMixerGain'
            self.__UpdateHelper('GroupPreMixerGain', commandString, value, qualifier)

    def SetGroupTrebleInputFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupTrebleInputFilter', value):
            level = round(value * 10)
            GroupTrebleInputFilterCmdString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupTrebleInputFilter'
            self.__SetHelper('GroupTrebleInputFilter', GroupTrebleInputFilterCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupTrebleInputFilter')

    def UpdateGroupTrebleInputFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            GroupTrebleInputFilterCmdString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupTrebleInputFilter'
            self.__UpdateHelper('GroupTrebleInputFilter', GroupTrebleInputFilterCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupTrebleInputFilter')

    def SetGroupTrebleVirtualReturnFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupTrebleVirtualReturnFilter', value):
            level = round(value * 10)
            GroupTrebleVirtualReturnFilterCmdString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupTrebleVirtualReturnFilter'
            self.__SetHelper('GroupTrebleVirtualReturnFilter', GroupTrebleVirtualReturnFilterCmdString, value,
                             qualifier)
        else:
            self.Discard('Invalid Command for SetGroupTrebleVirtualReturnFilter')

    def UpdateGroupTrebleVirtualReturnFilter(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            GroupTrebleVirtualReturnFilterCmdString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupTrebleVirtualReturnFilter'
            self.__UpdateHelper('GroupTrebleVirtualReturnFilter', GroupTrebleVirtualReturnFilterCmdString, value,
                                qualifier)
        else:
            self.Discard('Invalid Command for UpdateGroupTrebleVirtualReturnFilter')

    def SetGroupVirtualReturnGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64 and self.__CheckValidLevelValue('GroupVirtualReturnGain', value):
            level = round(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupVirtualReturnGain'
            self.__SetHelper('GroupVirtualReturnGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetGroupVirtualReturnGain')

    def UpdateGroupVirtualReturnGain(self, value, qualifier):

        group = qualifier['Group']
        if 1 <= int(group) <= 64:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupVirtualReturnGain'
            self.__UpdateHelper('GroupVirtualReturnGain', commandString, value, qualifier)

    def SetHook(self, value, qualifier):

        HookStateValues = {
            'End Call': 'END',
            'Answer'  : 'ANS',
            'Reject'  : 'REJ',
            'Hold On' : '1',
            'Hold Off': '0',
        }

        if 8 < int(qualifier['Line']) < 1:
            self.Discard('Invalid Command for SetHook')
        elif 8 < int(qualifier['Appearance']) < 1:
            self.Discard('Invalid Command for SetHook')
        else:

            if value in ['Hold On', 'Hold Off']:
                self.__SetHelper('Hook',
                                 '\x1BHOLD{0},{1},{2}VOIP\r\n'.format(qualifier['Line'], qualifier['Appearance'],
                                                                      HookStateValues[value]), value, qualifier)
            else:
                self.__SetHelper('Hook', '\x1B{0}{1},{2}VOIP\r\n'.format(HookStateValues[value], qualifier['Line'],
                                                                         qualifier['Appearance']), value, qualifier)

    def __MatchGroup(self, match, tag):
        group = str(int(match.group(1)))
        if group in self.GroupFunction:
            command = self.GroupFunction[group]
            if command == 'GroupMute':
                GroupMuteStateNames = {
                    '1': 'On',
                    '0': 'Off'
                }
                qualifier = {'Group': group}
                value = match.group(2).decode()[-1]
                self.WriteStatus(command, GroupMuteStateNames[value], qualifier)
            elif command in ['GroupPreMixerGain', 'GroupOutputAttenuation',
                             'GroupMixpointGain', 'GroupPostMixerTrim',
                             'GroupVirtualReturnGain', 'GroupMicLineInputGain',
                             'GroupBassInputFilter', 'GroupBassVirtualReturnFilter',
                             'GroupTrebleInputFilter', 'GroupTrebleVirtualReturnFilter']:
                qualifier = {'Group': group}
                value = int(match.group(2)) / 10
                self.WriteStatus(command, value, qualifier)

    ####################################################
    def SetInputGain(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 12 and self.__CheckValidLevelValue('InputGain', value):
            level = round(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 39999, level)
            self.__SetHelper('InputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetInputGain')

    def UpdateInputGain(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            commandString = 'wG{0}AU\r\n'.format(channel + 39999)
            self.__UpdateHelper('InputGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateInputGain')

    def __MatchInputGain(self, match, tag):

        channel = str(int(match.group(1)) - 39999)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('InputGain', value, qualifier)

    def SetInputMute(self, value, qualifier):

        MuteStateValues = {
            'On' : '1',
            'Off': '0'
        }
        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            commandString = 'wM{0}*{1}AU\r\n'.format(channel + 39999, MuteStateValues[value])
            self.__SetHelper('InputMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetInputMute')

    def UpdateInputMute(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            commandString = 'wM{0}AU\r\n'.format(channel + 39999)
            self.__UpdateHelper('InputMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateInputMute')

    def __MatchInputMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 39999)
        qualifier = {'Input': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('InputMute', value, qualifier)

    def UpdateInputSignalLevelMonitor(self, value, qualifier):

        ChannelValues = {
            '1'    : 1,
            '2'    : 2,
            '3'    : 3,
            '4'    : 4,
            '5'    : 5,
            '6'    : 6,
            '7'    : 7,
            '8'    : 8,
            '9'    : 9,
            '10'   : 10,
            '11'   : 11,
            '12'   : 12,
            'Aux 1': 13,
            'Aux 2': 14,
            'Aux 3': 15,
            'Aux 4': 16,
            'Aux 5': 17,
            'Aux 6': 18,
            'Aux 7': 19,
            'Aux 8': 20
        }
        channel = ChannelValues[qualifier['Input']]
        threshold = qualifier['Monitoring Threshold']
        if 1 <= channel <= 20 and -150 <= threshold <= 0:
            self.inputSignalLevelMonitorThreshold[channel] = threshold
            thresholdStr = str(abs(threshold) * 10)
            InputSignalLevelMonitorCmdString = 'wJ{0}*{1}AU\r'.format(channel + 39999, thresholdStr.zfill(4))
            self.__SetHelper('InputSignalLevelMonitor', InputSignalLevelMonitorCmdString, value, qualifier)

    def __MatchInputSignalLevelMonitor(self, match, tag):
        ChannelValues = {
            1 : '1',
            2 : '2',
            3 : '3',
            4 : '4',
            5 : '5',
            6 : '6',
            7 : '7',
            8 : '8',
            9 : '9',
            10: '10',
            11: '11',
            12: '12',
            13: 'Aux 1',
            14: 'Aux 2',
            15: 'Aux 3',
            16: 'Aux 4',
            17: 'Aux 5',
            18: 'Aux 6',
            19: 'Aux 7',
            20: 'Aux 8'
        }

        # print(match.group(0))
        channel = int(match.group(1)) - 39999
        try:
            qualifier = {
                'Input'               : ChannelValues[channel],
                'Monitoring Threshold': self.inputSignalLevelMonitorThreshold[channel]
            }
            thresholdStr = abs(self.inputSignalLevelMonitorThreshold[channel]) * 10
            if int(match.group(2)) > int(thresholdStr):
                self.WriteStatus('InputSignalLevelMonitor', 'Off', qualifier)
            else:
                self.WriteStatus('InputSignalLevelMonitor', 'On', qualifier)
        except KeyError:
            # if user set a threshold on the DMP using DSP or DataViewer,
            # this will give out a key Error as the resposne is not expected,
            pass

    def SetMacro(self, value, qualifier):

        if 0 < int(qualifier['Macro']) < 65:
            ValueStateValues = {
                'Run' : 'R',
                'Kill': 'K'
            }

            MacroCmdString = '\x1b{0}{1}MCRO\r\n'.format(ValueStateValues[value], qualifier['Macro'])
            self.__SetHelper('Macro', MacroCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetMacro')

    def SetMixpointGain(self, value, qualifier):

        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.MixpointInputStateValues and Output in self.MixpointOutputStateValues and self.__CheckValidLevelValue(
                'MixpointGain', value):
            inputValue = self.MixpointInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            level = round(value * 10)
            commandString = 'wG2{0}{1}*{2:05d}AU\r\n'.format(inputValue, outputValue, level)
            self.__SetHelper('MixpointGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetMixpointGain')

    def UpdateMixpointGain(self, value, qualifier):
        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.MixpointInputStateValues and Output in self.MixpointOutputStateValues:
            inputValue = self.MixpointInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            commandString = 'wG2{0}{1}AU\r\n'.format(inputValue, outputValue)
            self.__UpdateHelper('MixpointGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command')

    def __MatchMixpointGain(self, match, tag):

        if 0 <= int(match.group(1).decode()) <= 35:
            Input = self.MixpointInputStateNames[match.group(1).decode()]
            Output = self.MixpointOutputStateNames[match.group(2).decode()]
            value = int(match.group(3)) / 10
            qualifier = {'Input': Input, 'Output': Output}
            self.WriteStatus('MixpointGain', value, qualifier)
        else:
            Input = self.ExpansionBusInputStateNames[match.group(1).decode()]
            Output = self.MixpointOutputStateNames[match.group(2).decode()]
            value = int(match.group(3)) / 10
            qualifier = {'Input': Input, 'Output': Output}
            self.WriteStatus('ExpansionBusMixpointGain', value, qualifier)

    def SetMixpointMute(self, value, qualifier):

        MuteStateValues = {
            'On' : '1',
            'Off': '0'
        }
        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.MixpointInputStateValues and Output in self.MixpointOutputStateValues:
            inputValue = self.MixpointInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            commandString = 'wM2{0}{1}*{2}AU\r\n'.format(inputValue, outputValue, MuteStateValues[value])
            self.__SetHelper('MixpointMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for Set MixpointMute')

    def UpdateMixpointMute(self, value, qualifier):

        Input, Output = qualifier['Input'], qualifier['Output']
        if Input in self.MixpointInputStateValues and Output in self.MixpointOutputStateValues:
            inputValue = self.MixpointInputStateValues[Input]
            outputValue = self.MixpointOutputStateValues[Output]
            commandString = 'wM2{0}{1}AU\r\n'.format(inputValue, outputValue)
            self.__UpdateHelper('MixpointMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for Update MixpointMute')

    def __MatchMixpointMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        if 0 <= int(match.group(1).decode()) <= 35:
            Input = self.MixpointInputStateNames[match.group(1).decode()]
            Output = self.MixpointOutputStateNames[match.group(2).decode()]
            value = MuteStateNames[match.group(3).decode()]
            qualifier = {'Input': Input, 'Output': Output}
            self.WriteStatus('MixpointMute', value, qualifier)
        else:
            Input = self.ExpansionBusInputStateNames[match.group(1).decode()]
            Output = self.MixpointOutputStateNames[match.group(2).decode()]
            value = MuteStateNames[match.group(3).decode()]
            qualifier = {'Input': Input, 'Output': Output}
            self.WriteStatus('ExpansionBusMixpointMute', value, qualifier)

    def SetOutputMute(self, value, qualifier):

        MuteStateValues = {
            'On' : '1',
            'Off': '0'
        }
        channel = int(qualifier['Output'])
        if 1 <= channel <= 8:
            commandString = 'wM{0}*{1}AU\r\n'.format(channel + 59999, MuteStateValues[value])
            self.__SetHelper('OutputMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetOutputMute')

    def UpdateOutputMute(self, value, qualifier):

        channel = int(qualifier['Output'])
        if 1 <= channel <= 8:
            commandString = 'wM{0}AU\r\n'.format(channel + 59999)
            self.__UpdateHelper('OutputMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateOutputMute')

    def __MatchOutputMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 59999)
        qualifier = {'Output': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('OutputMute', value, qualifier)

    def SetOutputPostmixerTrim(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) < 9 and self.__CheckValidLevelValue('OutputPostmixerTrim', value):
            level = round(value * 10)
            ChannelValue = int(channel) + 60099
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('OutputPostmixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetOutputPostmixerTrim')

    def UpdateOutputPostmixerTrim(self, value, qualifier):

        channel = qualifier['Output']
        if 0 < int(channel) < 9:
            ChannelValue = int(channel) + 60099
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('OutputPostmixerTrim', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateOutputPostmixerTrim')

    def __MatchOutputPostmixerTrim(self, match, tag):

        channel = str(int(match.group(1)) - 60099)
        qualifier = {'Output': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('OutputPostmixerTrim', value, qualifier)

    def SetOutputAttenuation(self, value, qualifier):

        channel = int(qualifier['Output'])
        if 1 <= channel <= 8 and self.__CheckValidLevelValue('OutputAttenuation', value):
            level = round(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 59999, level)
            self.__SetHelper('OutputAttenuation', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetOutputAttenuation')

    def UpdateOutputAttenuation(self, value, qualifier):

        channel = int(qualifier['Output'])
        if 1 <= channel <= 8:
            commandString = 'wG{0}AU\r\n'.format(channel + 59999)
            self.__UpdateHelper('OutputAttenuation', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateOutputAttenuation')

    def __MatchOutputAttenuation(self, match, tag):

        channel = str(int(match.group(1)) - 59999)
        qualifier = {'Output': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('OutputAttenuation', value, qualifier)

    def SetPhantomPower(self, value, qualifier):

        state = {
            'Enable' : '1',
            'Disable': '0'
        }[value]

        inputVal = int(qualifier['Input'])
        if 1 <= inputVal <= 8:
            PhantomPowerCmdString = 'wZ4000{0}*{1}AU\r'.format(inputVal - 1, state)
            self.__SetHelper('PhantomPower', PhantomPowerCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetPhantomPower')

    def UpdatePhantomPower(self, value, qualifier):

        inputVal = int(qualifier['Input'])
        if 1 <= inputVal <= 8:
            PhantomPowerCmdString = 'wZ4000{0}AU\r'.format(inputVal - 1)
            self.__UpdateHelper('PhantomPower', PhantomPowerCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdatePhantomPower')

    def __MatchPhantomPower(self, match, tag):

        value = {
            '1': 'Enable',
            '0': 'Disable'
        }[match.group(2).decode()]

        qualifier = {}
        qualifier['Input'] = str(int(match.group(1).decode()) + 1)
        self.WriteStatus('PhantomPower', value, qualifier)

    def SetPlayerControl(self, value, qualifier):
        ValueStateValues = {
            'Start': '1',
            'Stop' : '0'
        }
        playerID = qualifier['Player ID']
        if 1 <= int(playerID) <= 8:
            PlayerControlCmdString = 'w{0}*{1}PLAY\r'.format(playerID, ValueStateValues[value])
            self.__SetHelper('PlayerControl', PlayerControlCmdString, value, qualifier)
        else:
            self.Discard('Player ID for SetPlayerControl is Invalid')

    def UpdatePlayerControl(self, value, qualifier):
        playerID = qualifier['Player ID']
        if 1 <= int(playerID) <= 8:
            PlayerControlCmdString = 'w{}PLAY\r'.format(playerID)
            self.__UpdateHelper('PlayerControl', PlayerControlCmdString, value, qualifier)
        else:
            self.Discard('Player ID for UpdatePlayerControl is Invalid')

    def __MatchPlayerControl(self, match, tag):
        ValueStateValues = {
            '1': 'Start',
            '0': 'Stop'
        }

        qualifier = {'Player ID': match.group(1).decode()}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('PlayerControl', value, qualifier)

    def _SetPlayerFilenameCommand(self, value, qualifier):
        playerID = qualifier['Player ID']
        filename = value
        if 1 <= int(playerID) <= 8:
            if not filename or filename.isspace():
                PlayerFilenameCommandCmdString = 'wA{}* CPLY\r'.format(playerID)
            else:
                PlayerFilenameCommandCmdString = 'wA{0}*{1}CPLY\r'.format(playerID, filename)

            self.__SetHelper('PlayerFilenameCommand', PlayerFilenameCommandCmdString, filename, qualifier)
        else:
            self.Discard('Player ID for SetPlayerFilenameCommand is Invalid')

    # Begin PlayerFilenameStatus
    def UpdatePlayerFilenameStatus(self, value, qualifier):
        playerID = qualifier['Player ID']
        if 1 <= int(playerID) <= 8:
            PlayerFilenameStatusCmdString = 'wA{}CPLY\r'.format(playerID)
            self.__UpdateHelper('PlayerFilenameStatus', PlayerFilenameStatusCmdString, value, qualifier)
        else:
            self.Discard('Player ID for UpdatePlayerFilenameCommand is Invalid')

    def __MatchPlayerFilenameStatus(self, match, tag):
        qualifier = {'Player ID': match.group(1).decode()}
        value = match.group(2).decode()
        self.WriteStatus('PlayerFilenameStatus', value, qualifier)

    def SetPlayerRepeat(self, value, qualifier):
        ValueStateValues = {
            'Play Once': '0',
            'Repeat'   : '1'
        }
        playerID = qualifier['Player ID']
        if 1 <= int(playerID) <= 8:
            PlayerRepeatCmdString = 'wM{0}*{1}CPLY\r'.format(playerID, ValueStateValues[value])
            self.__SetHelper('PlayerRepeat', PlayerRepeatCmdString, value, qualifier)
        else:
            self.Discard('Player ID for SetPlayerRepeat is Invalid')

    def UpdatePlayerRepeat(self, value, qualifier):
        playerID = qualifier['Player ID']
        if 1 <= int(playerID) <= 8:
            PlayerRepeatCmdString = 'wM{}CPLY\r'.format(playerID)
            self.__UpdateHelper('PlayerRepeat', PlayerRepeatCmdString, value, qualifier)
        else:
            self.Discard('Player ID for UpdatePlayerRepeat is Invalid')

    def __MatchPlayerRepeat(self, match, tag):
        ValueStateValues = {
            '0': 'Play Once',
            '1': 'Repeat'
        }

        qualifier = {'Player ID': match.group(1).decode()}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('PlayerRepeat', value, qualifier)

    def SetPremixerGain(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 12 and self.__CheckValidLevelValue('PremixerGain', value):
            level = round(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 40099, level)
            self.__SetHelper('PremixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetPremixerGain')

    def UpdatePremixerGain(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            commandString = 'wG{0}AU\r\n'.format(channel + 40099)
            self.__UpdateHelper('PremixerGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdatePremixerGain')

    def __MatchPremixerGain(self, match, tag):

        channel = str(int(match.group(1)) - 40099)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('PremixerGain', value, qualifier)

    def SetPremixerMute(self, value, qualifier):

        MuteStateValues = {
            'On' : '1',
            'Off': '0'
        }
        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            commandString = 'wM{0}*{1}AU\r\n'.format(channel + 40099, MuteStateValues[value])
            self.__SetHelper('PremixerMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetPremixerMute')

    def UpdatePremixerMute(self, value, qualifier):

        channel = int(qualifier['Input'])
        if 1 <= channel <= 12:
            commandString = 'wM{0}AU\r\n'.format(channel + 40099)
            self.__UpdateHelper('PremixerMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdatePremixerMute')

    def __MatchPremixerMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 40099)
        qualifier = {'Input': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('PremixerMute', value, qualifier)

    def SetPresetRecall(self, value, qualifier):

        if 0 < int(value) <= 32:
            commandString = '{0}.'.format(value)
            self.__SetHelper('PresetRecall', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetPresetRecall')

    def SetStartPlayer(self, value, qualifier):

        if 0 < int(qualifier['Player ID']) < 9 and 0 <= qualifier['Repeat Delay'] <= 300:
            StartPlayerCmdString = '\x1b{0}*1*{1}PLAY\r\n'.format(qualifier['Player ID'], qualifier['Repeat Delay'])
            self.__SetHelper('StartPlayer', StartPlayerCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetStartPlayer')

    def SetStopPlayer(self, value, qualifier):

        if 0 < int(qualifier['Player ID']) < 9:
            StopPlayerCmdString = '\x1b{0}*0*0PLAY\r\n'.format(qualifier['Player ID'])
            self.__SetHelper('StopPlayer', StopPlayerCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetStopPlayer')

    def UpdateRegistrationStatus(self, value, qualifier):

        line = qualifier['Line']
        if 1 <= int(line) <= 8:
            RegistrationStatusCmdString = 'wRS{}VOIP\r'.format(line)
            self.__UpdateHelper('RegistrationStatus', RegistrationStatusCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateRegistrationStatus')

    def __MatchRegistrationStatus(self, match, tag):

        LineStates = {
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8'
        }

        ValueStateValues = {
            '0': 'Unregistered',
            '1': 'Registered to 1st Proxy',
            '2': 'Registered to 2nd Proxy',
            '3': 'None',
            '4': 'Not Registered'
        }

        qualifier = {}
        qualifier['Line'] = LineStates[match.group(1).decode()]
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('RegistrationStatus', value, qualifier)

    def SetVirtualReturnGain(self, value, qualifier):

        channel = qualifier['Input']
        if channel in self.VirtualChannels and self.__CheckValidLevelValue('VirtualReturnGain', value):
            level = round(value * 10)
            ChannelValue = ord(channel) + 50035
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('VirtualReturnGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetVirtualReturnGain')

    def UpdateVirtualReturnGain(self, value, qualifier):

        channel = qualifier['Input']
        if channel in self.VirtualChannels:
            ChannelValue = ord(channel) + 50035
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('VirtualReturnGain', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateVirtualReturnGain')

    def __MatchVirtualReturnGain(self, match, tag):

        channel = chr(int(match.group(1)) - 50035)
        qualifier = {'Input': channel}
        value = int(match.group(2)) / 10
        self.WriteStatus('VirtualReturnGain', value, qualifier)

    def SetVirtualReturnMute(self, value, qualifier):

        MuteStateValues = {
            'On' : '1',
            'Off': '0'
        }
        channel = qualifier['Input']
        if channel in self.VirtualChannels:
            ChannelValue = ord(channel) + 50035
            commandString = 'wM{0}*{1}AU\r\n'.format(ChannelValue, MuteStateValues[value])
            self.__SetHelper('VirtualReturnMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetVirtualReturnMute')

    def UpdateVirtualReturnMute(self, value, qualifier):

        channel = qualifier['Input']
        if channel in self.VirtualChannels:
            ChannelValue = ord(channel) + 50035
            commandString = 'wM{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('VirtualReturnMute', commandString, value, qualifier)
        else:
            self.Discard('Invalid Command for UpdateVirtualReturnMute')

    def __MatchVirtualReturnMute(self, match, tag):

        MuteStateNames = {
            '1': 'On',
            '0': 'Off'
        }

        channel = chr(int(match.group(1)) - 50035)
        qualifier = {'Input': channel}
        value = MuteStateNames[match.group(2).decode()]
        self.WriteStatus('VirtualReturnMute', value, qualifier)

    def __CheckValidLevelValue(self, command, value):
        return self.LevelTypes[command]['Min'] <= value <= self.LevelTypes[command]['Max']

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        if self.VerboseDisabled:
            @Wait(1)
            def SendVerbose():
                self.Send('w3cv\r\n')
                self.Send(commandstring)
        else:
            self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter = self.counter + 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()

        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                self.Discard('Inappropriate Command ' + command)
            else:
                if self.VerboseDisabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        self.Send(commandstring)
                else:
                    self.Send(commandstring)
        else:
            self.Discard('Inappropriate Command ' + command)

    def __MatchError(self, match, tag):

        DeviceErrorCodes = {
            '10': 'Unrecognized command',
            '12': 'Invalid port number',
            '13': 'Invalid parameter (number is out of range)',
            '14': 'Not valid for this configuration',
            '17': 'Invalid command for signal type',
            '18': 'System/command timed out',
            '22': 'Busy',
            '24': 'Privilege violation',
            '25': 'Device is not present',
            '26': 'Maximum connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
            '31': 'Attempt to break port passthrough when not set',
        }
        self.Error([DeviceErrorCodes.get(match.group(1).decode(),
                                         'Unrecognized error code: {0}'.format(match.group(0).decode()))])

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

        if 'Serial' not in self.ConnectionType:
            self.Authenticated = 'Not Needed'
            self.PasswdPromptCount = 0
        self.VerboseDisabled = True
        self.lastCallerNameUpdate = 0

    def extr_25_2513_128(self):
        self.MAX_AUX_OUTPUTS = 4
        self.MAX_EXPANSION_INPUTS = 16
        self.ExpansionBusInputStateValues = {
            '1' : '36',
            '2' : '37',
            '3' : '38',
            '4' : '39',
            '5' : '40',
            '6' : '41',
            '7' : '42',
            '8' : '43',
            '9' : '44',
            '10': '45',
            '11': '46',
            '12': '47',
            '13': '48',
            '14': '49',
            '15': '50',
            '16': '51',
        }

        self.ExpansionBusInputStateNames = {
            '36': '1',
            '37': '2',
            '38': '3',
            '39': '4',
            '40': '5',
            '41': '6',
            '42': '7',
            '43': '8',
            '44': '9',
            '45': '10',
            '46': '11',
            '47': '12',
            '48': '13',
            '49': '14',
            '50': '15',
            '51': '16',
        }

        self.MixpointInputStateValues = {
            '1'          : '00',
            '2'          : '01',
            '3'          : '02',
            '4'          : '03',
            '5'          : '04',
            '6'          : '05',
            '7'          : '06',
            '8'          : '07',
            '9'          : '08',
            '10'         : '09',
            '11'         : '10',
            '12'         : '11',
            'Aux 1'      : '12',
            'Aux 2'      : '13',
            'Aux 3'      : '14',
            'Aux 4'      : '15',
            'Aux 5'      : '16',
            'Aux 6'      : '17',
            'Aux 7'      : '18',
            'Aux 8'      : '19',
            'V. Return A': '20',
            'V. Return B': '21',
            'V. Return C': '22',
            'V. Return D': '23',
            'V. Return E': '24',
            'V. Return F': '25',
            'V. Return G': '26',
            'V. Return H': '27',
            'V. Return I': '28',
            'V. Return J': '29',
            'V. Return K': '30',
            'V. Return L': '31',
            'V. Return M': '32',
            'V. Return N': '33',
            'V. Return O': '34',
            'V. Return P': '35'
        }
        self.MixpointInputStateNames = {
            '00': '1',
            '01': '2',
            '02': '3',
            '03': '4',
            '04': '5',
            '05': '6',
            '06': '7',
            '07': '8',
            '08': '9',
            '09': '10',
            '10': '11',
            '11': '12',
            '12': 'Aux 1',
            '13': 'Aux 2',
            '14': 'Aux 3',
            '15': 'Aux 4',
            '16': 'Aux 5',
            '17': 'Aux 6',
            '18': 'Aux 7',
            '19': 'Aux 8',
            '20': 'V. Return A',
            '21': 'V. Return B',
            '22': 'V. Return C',
            '23': 'V. Return D',
            '24': 'V. Return E',
            '25': 'V. Return F',
            '26': 'V. Return G',
            '27': 'V. Return H',
            '28': 'V. Return I',
            '29': 'V. Return J',
            '30': 'V. Return K',
            '31': 'V. Return L',
            '32': 'V. Return M',
            '33': 'V. Return N',
            '34': 'V. Return O',
            '35': 'V. Return P'
        }

    def extr_25_2513_128AT(self):
        self.MAX_AUX_OUTPUTS = 4
        self.MAX_EXPANSION_INPUTS = 48

        self.ExpansionBusInputStateValues = {
            '1' : '36',
            '2' : '37',
            '3' : '38',
            '4' : '39',
            '5' : '40',
            '6' : '41',
            '7' : '42',
            '8' : '43',
            '9' : '44',
            '10': '45',
            '11': '46',
            '12': '47',
            '13': '48',
            '14': '49',
            '15': '50',
            '16': '51',
            '17': '52',
            '18': '53',
            '19': '54',
            '20': '55',
            '21': '56',
            '22': '57',
            '23': '58',
            '24': '59',
            '25': '60',
            '26': '61',
            '27': '62',
            '28': '63',
            '29': '64',
            '30': '65',
            '31': '66',
            '32': '67',
            '33': '68',
            '34': '69',
            '35': '70',
            '36': '71',
            '37': '72',
            '38': '73',
            '39': '74',
            '40': '75',
            '41': '76',
            '42': '77',
            '43': '78',
            '44': '79',
            '45': '80',
            '46': '81',
            '47': '82',
            '48': '83'
        }

        self.ExpansionBusInputStateNames = {
            '36': '1',
            '37': '2',
            '38': '3',
            '39': '4',
            '40': '5',
            '41': '6',
            '42': '7',
            '43': '8',
            '44': '9',
            '45': '10',
            '46': '11',
            '47': '12',
            '48': '13',
            '49': '14',
            '50': '15',
            '51': '16',
            '52': '17',
            '53': '18',
            '54': '19',
            '55': '20',
            '56': '21',
            '57': '22',
            '58': '23',
            '59': '24',
            '60': '25',
            '61': '26',
            '62': '27',
            '63': '28',
            '64': '29',
            '65': '30',
            '66': '31',
            '67': '32',
            '68': '33',
            '69': '34',
            '70': '35',
            '71': '36',
            '72': '37',
            '73': '38',
            '74': '39',
            '75': '40',
            '76': '41',
            '77': '42',
            '78': '43',
            '79': '44',
            '80': '45',
            '81': '46',
            '82': '47',
            '83': '48'
        }

        self.MixpointInputStateValues = {
            '1'          : '00',
            '2'          : '01',
            '3'          : '02',
            '4'          : '03',
            '5'          : '04',
            '6'          : '05',
            '7'          : '06',
            '8'          : '07',
            '9'          : '08',
            '10'         : '09',
            '11'         : '10',
            '12'         : '11',
            'Aux 1'      : '12',
            'Aux 2'      : '13',
            'Aux 3'      : '14',
            'Aux 4'      : '15',
            'Aux 5'      : '16',
            'Aux 6'      : '17',
            'Aux 7'      : '18',
            'Aux 8'      : '19',
            'V. Return A': '20',
            'V. Return B': '21',
            'V. Return C': '22',
            'V. Return D': '23',
            'V. Return E': '24',
            'V. Return F': '25',
            'V. Return G': '26',
            'V. Return H': '27',
            'V. Return I': '28',
            'V. Return J': '29',
            'V. Return K': '30',
            'V. Return L': '31',
            'V. Return M': '32',
            'V. Return N': '33',
            'V. Return O': '34',
            'V. Return P': '35'
        }

        self.MixpointInputStateNames = {
            '00': '1',
            '01': '2',
            '02': '3',
            '03': '4',
            '04': '5',
            '05': '6',
            '06': '7',
            '07': '8',
            '08': '9',
            '09': '10',
            '10': '11',
            '11': '12',
            '12': 'Aux 1',
            '13': 'Aux 2',
            '14': 'Aux 3',
            '15': 'Aux 4',
            '16': 'Aux 5',
            '17': 'Aux 6',
            '18': 'Aux 7',
            '19': 'Aux 8',
            '20': 'V. Return A',
            '21': 'V. Return B',
            '22': 'V. Return C',
            '23': 'V. Return D',
            '24': 'V. Return E',
            '25': 'V. Return F',
            '26': 'V. Return G',
            '27': 'V. Return H',
            '28': 'V. Return I',
            '29': 'V. Return J',
            '30': 'V. Return K',
            '31': 'V. Return L',
            '32': 'V. Return M',
            '33': 'V. Return N',
            '34': 'V. Return O',
            '35': 'V. Return P'
        }

    def extr_25_2513_128V(self):
        self.MAX_AUX_OUTPUTS = 8
        self.MAX_EXPANSION_INPUTS = 16

        self.ExpansionBusInputStateValues = {
            '1' : '36',
            '2' : '37',
            '3' : '38',
            '4' : '39',
            '5' : '40',
            '6' : '41',
            '7' : '42',
            '8' : '43',
            '9' : '44',
            '10': '45',
            '11': '46',
            '12': '47',
            '13': '48',
            '14': '49',
            '15': '50',
            '16': '51',
        }

        self.ExpansionBusInputStateNames = {
            '36': '1',
            '37': '2',
            '38': '3',
            '39': '4',
            '40': '5',
            '41': '6',
            '42': '7',
            '43': '8',
            '44': '9',
            '45': '10',
            '46': '11',
            '47': '12',
            '48': '13',
            '49': '14',
            '50': '15',
            '51': '16',
        }

        self.MixpointInputStateValues = {
            '1'          : '00',
            '2'          : '01',
            '3'          : '02',
            '4'          : '03',
            '5'          : '04',
            '6'          : '05',
            '7'          : '06',
            '8'          : '07',
            '9'          : '08',
            '10'         : '09',
            '11'         : '10',
            '12'         : '11',
            'Aux 1'      : '12',
            'Aux 2'      : '13',
            'Aux 3'      : '14',
            'Aux 4'      : '15',
            'Aux 5'      : '16',
            'Aux 6'      : '17',
            'Aux 7'      : '18',
            'Aux 8'      : '19',
            'V. Return A': '20',
            'V. Return B': '21',
            'V. Return C': '22',
            'V. Return D': '23',
            'V. Return E': '24',
            'V. Return F': '25',
            'V. Return G': '26',
            'V. Return H': '27',
            'V. Return I': '28',
            'V. Return J': '29',
            'V. Return K': '30',
            'V. Return L': '31',
            'V. Return M': '32',
            'V. Return N': '33',
            'V. Return O': '34',
            'V. Return P': '35'
        }

        self.MixpointInputStateNames = {
            '00': '1',
            '01': '2',
            '02': '3',
            '03': '4',
            '04': '5',
            '05': '6',
            '06': '7',
            '07': '8',
            '08': '9',
            '09': '10',
            '10': '11',
            '11': '12',
            '12': 'Aux 1',
            '13': 'Aux 2',
            '14': 'Aux 3',
            '15': 'Aux 4',
            '16': 'Aux 5',
            '17': 'Aux 6',
            '18': 'Aux 7',
            '19': 'Aux 8',
            '20': 'V. Return A',
            '21': 'V. Return B',
            '22': 'V. Return C',
            '23': 'V. Return D',
            '24': 'V. Return E',
            '25': 'V. Return F',
            '26': 'V. Return G',
            '27': 'V. Return H',
            '28': 'V. Return I',
            '29': 'V. Return J',
            '30': 'V. Return K',
            '31': 'V. Return L',
            '32': 'V. Return M',
            '33': 'V. Return N',
            '34': 'V. Return O',
            '35': 'V. Return P'
        }

    def extr_25_2513_128VAT(self):
        self.MAX_AUX_OUTPUTS = 8
        self.MAX_EXPANSION_INPUTS = 48

        self.ExpansionBusInputStateValues = {
            '1' : '36',
            '2' : '37',
            '3' : '38',
            '4' : '39',
            '5' : '40',
            '6' : '41',
            '7' : '42',
            '8' : '43',
            '9' : '44',
            '10': '45',
            '11': '46',
            '12': '47',
            '13': '48',
            '14': '49',
            '15': '50',
            '16': '51',
            '17': '52',
            '18': '53',
            '19': '54',
            '20': '55',
            '21': '56',
            '22': '57',
            '23': '58',
            '24': '59',
            '25': '60',
            '26': '61',
            '27': '62',
            '28': '63',
            '29': '64',
            '30': '65',
            '31': '66',
            '32': '67',
            '33': '68',
            '34': '69',
            '35': '70',
            '36': '71',
            '37': '72',
            '38': '73',
            '39': '74',
            '40': '75',
            '41': '76',
            '42': '77',
            '43': '78',
            '44': '79',
            '45': '80',
            '46': '81',
            '47': '82',
            '48': '83'
        }

        self.ExpansionBusInputStateNames = {
            '36': '1',
            '37': '2',
            '38': '3',
            '39': '4',
            '40': '5',
            '41': '6',
            '42': '7',
            '43': '8',
            '44': '9',
            '45': '10',
            '46': '11',
            '47': '12',
            '48': '13',
            '49': '14',
            '50': '15',
            '51': '16',
            '52': '17',
            '53': '18',
            '54': '19',
            '55': '20',
            '56': '21',
            '57': '22',
            '58': '23',
            '59': '24',
            '60': '25',
            '61': '26',
            '62': '27',
            '63': '28',
            '64': '29',
            '65': '30',
            '66': '31',
            '67': '32',
            '68': '33',
            '69': '34',
            '70': '35',
            '71': '36',
            '72': '37',
            '73': '38',
            '74': '39',
            '75': '40',
            '76': '41',
            '77': '42',
            '78': '43',
            '79': '44',
            '80': '45',
            '81': '46',
            '82': '47',
            '83': '48'
        }

        self.MixpointInputStateValues = {
            '1'          : '00',
            '2'          : '01',
            '3'          : '02',
            '4'          : '03',
            '5'          : '04',
            '6'          : '05',
            '7'          : '06',
            '8'          : '07',
            '9'          : '08',
            '10'         : '09',
            '11'         : '10',
            '12'         : '11',
            'Aux 1'      : '12',
            'Aux 2'      : '13',
            'Aux 3'      : '14',
            'Aux 4'      : '15',
            'Aux 5'      : '16',
            'Aux 6'      : '17',
            'Aux 7'      : '18',
            'Aux 8'      : '19',
            'V. Return A': '20',
            'V. Return B': '21',
            'V. Return C': '22',
            'V. Return D': '23',
            'V. Return E': '24',
            'V. Return F': '25',
            'V. Return G': '26',
            'V. Return H': '27',
            'V. Return I': '28',
            'V. Return J': '29',
            'V. Return K': '30',
            'V. Return L': '31',
            'V. Return M': '32',
            'V. Return N': '33',
            'V. Return O': '34',
            'V. Return P': '35'
        }

        self.MixpointInputStateNames = {
            '00': '1',
            '01': '2',
            '02': '3',
            '03': '4',
            '04': '5',
            '05': '6',
            '06': '7',
            '07': '8',
            '08': '9',
            '09': '10',
            '10': '11',
            '11': '12',
            '12': 'Aux 1',
            '13': 'Aux 2',
            '14': 'Aux 3',
            '15': 'Aux 4',
            '16': 'Aux 5',
            '17': 'Aux 6',
            '18': 'Aux 7',
            '19': 'Aux 8',
            '20': 'V. Return A',
            '21': 'V. Return B',
            '22': 'V. Return C',
            '23': 'V. Return D',
            '24': 'V. Return E',
            '25': 'V. Return F',
            '26': 'V. Return G',
            '27': 'V. Return H',
            '28': 'V. Return I',
            '29': 'V. Return J',
            '30': 'V. Return K',
            '31': 'V. Return L',
            '32': 'V. Return M',
            '33': 'V. Return N',
            '34': 'V. Return O',
            '35': 'V. Return P'
        }

    ######################################################
    # RECOMMENDED not to modify the code below this point
    ######################################################

    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = getattr(self, 'Set%s' % command, None)
        if method is not None and callable(method):
            method(value, qualifier)
        else:
            raise AttributeError(command, 'does not support Set.')

    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = getattr(self, 'Update%s' % command, None)
        if method is not None and callable(method):
            method(None, qualifier)
        else:
            raise AttributeError(command, 'does not support Update.')

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command, None)
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
            raise KeyError('Invalid command for SubscribeStatus ', command)

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
        Command = self.Commands.get(command, None)
        if Command:
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
        else:
            raise KeyError('Invalid command for ReadStatus: ', command)

    def __ReceiveData(self, interface, data):
        # Handle incoming data
        self.__receiveBuffer += data
        index = 0  # Start of possible good data

        # check incoming data if it matched any expected data from device module
        for regexString, CurrentMatch in self.__matchStringDict.items():
            while True:
                result = search(regexString, self.__receiveBuffer)
                if result:
                    index = result.start()
                    CurrentMatch['callback'](result, CurrentMatch['para'])
                    self.__receiveBuffer = self.__receiveBuffer[:result.start()] + self.__receiveBuffer[result.end():]
                else:
                    break

        if index:
            # Clear out any junk data that came in before any good matches.
            self.__receiveBuffer = self.__receiveBuffer[index:]
        else:
            # In rare cases, the buffer could be filled with garbage quickly.
            # Make sure the buffer is capped.  Max buffer size set in init.
            self.__receiveBuffer = self.__receiveBuffer[-self.__maxBufferSize:]

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self.__matchStringDict:
            self.__matchStringDict[regex_string] = {'callback': callback, 'para': arg}

    def MissingCredentialsLog(self, credential_type):
        if isinstance(self, EthernetClientInterface):
            port_info = 'IP Address: {0}:{1}'.format(self.IPAddress, self.IPPort)
        elif isinstance(self, SerialInterface):
            port_info = 'Host Alias: {0}\r\nPort: {1}'.format(self.Host.DeviceAlias, self.Port)
        else:
            return
        ProgramLog("{0} module received a request from the device for a {1}, "
                   "but device{1} was not provided.\n Please provide a device{1} "
                   "and attempt again.\n Ex: dvInterface.device{1} = '{1}'\n Please "
                   "review the communication sheet.\n {2}"
                   .format(__name__, credential_type, port_info), 'warning')


class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=38400, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0,
                 Mode='RS232', Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay, Mode)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()

    def Error(self, message):
        portInfo = 'Host Alias: {0}, Port: {1}'.format(self.Host.DeviceAlias, self.Port)
        print('Module: {}'.format(__name__), portInfo, 'Error Message: {}'.format(message[0]), sep='\r\n')

    def Discard(self, message):
        self.Error([message])


class SerialOverEthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Serial'
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
