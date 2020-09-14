from extronlib import Version

import datetime

from utilities import DebugPrint

DebugPrint('main.py', '==========================================================================', 'Info')
DebugPrint('main.py', 'Light of Christ Control System v1.0 (SEPT 2020).. (Extron ControlScript v{})'.format(Version()), 'Info')
DebugPrint('main.py', ' - designed, engineered, and implemented by Joel D. Caturia <jcaturia@katratech.com>)', 'Info')
DebugPrint('main.py', 'System initializing at {}'.format(datetime.datetime.now()), 'Info')
DebugPrint('main.py', '==========================================================================', 'Info')

import devices
import interface

def initialize():
    devices.InitializeAll()
    interface.initialize_all()
# end function (Initialize)


initialize()


DebugPrint('main.py', '==========================================================================', 'Info')
DebugPrint('main.py', 'Completed Initialization .. Have a great rest of your day!', 'Info')
DebugPrint('main.py', '==========================================================================', 'Info')
