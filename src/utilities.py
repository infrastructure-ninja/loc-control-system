
DebugLevel = 0

def DebugPrint(strFunctionName, strMessage, strMessageLevel = 'Debug' ):

    try:
        intMessageLevel = {'Debug': 0, 'Info': 1, 'Warn': 2, 'Error': 3}[strMessageLevel]

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
