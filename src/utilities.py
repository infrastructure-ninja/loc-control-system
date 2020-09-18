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

import datetime

from helper_configmgr import ConfigManager

DebugLevel = 0

config = ConfigManager('configuration.json')


def DebugPrint(strFunctionName, strMessage, strMessageLevel = 'Debug' ):

    try:
        intMessageLevel = {'Trace': 0, 'Debug': 1, 'Info': 2, 'Warn': 3, 'Error': 4}[strMessageLevel]

        if DebugLevel <= intMessageLevel:
            print ('[{}] [{}] {}'.format(strMessageLevel, strFunctionName, strMessage))
    
    except KeyError:
        return False
#end function (DebugPrint)

def ConvertTimecodeToSeconds(timecode):

    try:
        hours, minutes, seconds = timecode.split(':')
        seconds = (int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds)
        return seconds
    except:
        return 0
#end function (ConvertTimecodeToSeconds)


def ConvertSecondsToTimeCode(seconds):
    try:
        return str(datetime.timedelta(seconds=seconds))
    except:
        return '00:00:00'
#end function (ConvertSecondsToTimeCode)


class DummyDriver:
    def __init__(self, friendly_name):
        self.friendly_name = friendly_name
        DebugPrint('utilities/DummyDriver', 'Initializing Dummy Driver for -> [{}]..', self.friendly_name)

    def Connect(self, *args, **kwargs):
        pass

    def Set(self, *args, **kwargs):
        pass

    def Update(self, *args, **kwargs):
        pass

    def SubscribeStatus(self, *args, **kwargs):
        pass

    def ReadStatus(self, *args, **kwargs):
        pass

    def StartListen(selfs, *args, **kwargs):
        return 'DUMMY DRIVER LOADED'
