


def DebugPrint(self, strFunctionName, strMessage, intMessageLevel = 0 ):

    DebugLevel = 0

    if DebugLevel <= intMessageLevel:
        try:
            severity = ['Debug', 'Info', 'Warn', 'Error'][intMessageLevel]
        
        except KeyError:
            severity = 'Debug'
    
    print ('[{}] [{}] {}'.format(severity, strFunctionName, strMessage))
