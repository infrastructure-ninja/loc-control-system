
DebugLevel = 0

def DebugPrint(strFunctionName, strMessage, strMessageLevel = 'Debug' ):

    try:
        intMessageLevel = {'Debug': 0, 'Info': 1, 'Warn': 2, 'Error': 3}[strMessageLevel]

        if DebugLevel <= intMessageLevel:
            print ('[{}] [{}] {}'.format(strMessageLevel, strFunctionName, strMessage))
    
    except KeyError:
        return False
    
