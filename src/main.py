from extronlib import Version

import devices
import interface
from utilities import DebugPrint

DebugPrint ('main.py', 'Light of Christ Control System v1.0 .. booting up! (ControlScript v{})'.format(Version()), 'Info')

def Initialize():
    devices.InitializeAll()





Initialize()

DebugPrint ('main.py', 'Finished booting .. Have a great rest of your day!', 'Info')
    