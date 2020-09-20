# A GlobalScripter module for the Engineering Solutions, Inc
# "DecaBox Protocol Bridge"
# http://response-box.com/gear/2011/12/decabox-midi-to-rs232-field-programmable/
#
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
#
# Extremely useful page with a neat table for MIDI messages.
# Reproduced below for convenience.
# http://www.personal.kent.edu/~sbirch/Music_Production/MP-II/MIDI/midi_channel_voice_messages.htm
#
# The table below presents a summary of the MIDI Channel Voice Message codes in binary form.
# A MIDI channel voice message consists of a Status Byte followed by one or two Data Bytes.
# Status Byte Data Byte 1 Data Byte 2 Message Legend
# 1000nnnn    0kkkkkkk    0vvvvvvv    Note Off    n=channel* k=key # 0-127(60=middle C) v=velocity (0-127)
# 1001nnnn    0kkkkkkk    0vvvvvvv    Note On n=channel k=key # 0-127(60=middle C) v=velocity (0-127)
# 1010nnnn    0kkkkkkk    0ppppppp    Poly Key Pressure   n=channel k=key # 0-127(60=middle C) p=pressure (0-127)
# 1011nnnn    0ccccccc    0vvvvvvv    Controller Change   n=channel c=controller v=controller value(0-127)
# 1100nnnn    0ppppppp    [none]      Program Change  n=channel p=preset number (0-127)
# 1101nnnn    0ppppppp    [none]      Channel Pressure    n=channel p=pressure (0-127)
# 1101nnnn    0ccccccc    0fffffff    Pitch Bend  n=channel c=coarse f=fine (c+f = 14-bit resolution)

from extronlib.interface import SerialInterface, EthernetClientInterface
import re
from struct import unpack
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
        self.Models = {}

        # Build out some dictionaries for helping us get from MIDI note values (24-119) to letter notation (C0 - B7)
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.base_numbers = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        self.midi_notes_by_number = {}
        self.midi_notes_by_letter = {}

        for octave in range(0, 8):
            for note_tuple in zip(self.notes, self.base_numbers):
                self.midi_notes_by_number.update({(octave * 12) + note_tuple[1]: '{}{}'.format(note_tuple[0], octave)})
                self.midi_notes_by_letter.update({'{}{}'.format(note_tuple[0], octave): (octave * 12) + note_tuple[1]})

        self.Commands = {
            # 'SendMIDI': {'Parameters':['Channel', 'Note', 'Duration'],'Status': {}},
            'IncomingNote': {'Parameters': ['Channel', 'Note'], 'Status': {}},
        }

        if self.Unidirectional == 'False':
            self.AddMatchString(re.compile(b'([\x00-\xff)])([\x00-\x7f)]{2})'), self.__MatchMIDI, None)

    def __MatchMIDI(self, match, tag):

        MIDI_NOTE_OFF = 0x8
        MIDI_NOTE_ON = 0x9
        MIDI_AFTER_TOUCH = 0xA
        MIDI_CONTROL_CHANGE = 0xB

        try:
            status_byte = unpack('>B', match.group(1))[0]
            data_byte_1, data_byte_2 = unpack('>BB', match.group(2))

            # shift the byte four positions to the right, so we keep the 4 bits
            # that make up the "MIDI message"
            midi_message = status_byte >> 4

            # masks out the left 4 bits of the status byte, leaving us with the 4
            # on the right that we care about: MIDI channel)
            # .. binary output will be 0-15, but MIDI channels go from 1-16, so add 1
            midi_channel = (status_byte & int('00001111', 2)) + 1

            # We really only care about NOTE ON and NOTE OFF events right now, but
            # we are well positioned to add CC (control change) events as well if
            # they become necessary/useful.
            if midi_message == MIDI_NOTE_OFF or midi_message == MIDI_NOTE_ON:
                note_number = data_byte_1
                velocity = data_byte_2

                if midi_message == MIDI_NOTE_OFF:
                    value = 'Off'
                else:
                    value = str(velocity)

                qualifier = {}
                qualifier.update({'Channel': midi_channel})
                qualifier.update({'Note': self.midi_notes_by_number[note_number]})

                # Don't use "WriteStatus" here since we want a callback *every time*
                # we see the MIDI data come in.
                self.NewStatus('IncomingNote', value, qualifier)

        except:
            pass

    # def SetSendMIDI(self, value, qualifier)
    #
    ##'Channel', 'Note', 'Duration'
    #
    # channel = qualifier['Channel']
    # note = qualifier['Note']
    # duration = qualifier['Duration']
    #
    # if value == 'Off':
    # SendMIDICmdString = 'I\r'
    # self.__SetHelper('SendMIDI', SendMIDICmdString, value, qualifier)
    #
    # elif 0 <= int(value) <= 127:
    #
    # else:
    # self.Discard('Invalid value for for SetSendMIDI')

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True

        self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):

        if self.Unidirectional == 'True':
            self.Discard('Inappropriate Command ' + command)
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

        # print('RCV ->', data)

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

