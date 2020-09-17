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
