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
#
#
# REVISION HISTORY:
# - (initial revision)
#
#

from extronlib import Version

import datetime

from utilities import DebugPrint

DebugPrint('main.py',
           '==========================================================================', 'Info')
DebugPrint('main.py',
           'Light of Christ Control System v1.2 (NOVEMBER 2022).. (Extron ControlScript v{})'.
           format(Version()), 'Info')

DebugPrint('main.py',
           ' - designed, engineered, and implemented by Joel D. Caturia <jcaturia@katratech.com>)', 'Info')

DebugPrint('main.py',
           'System initializing at {}'.format(datetime.datetime.now()), 'Info')

DebugPrint('main.py',
           '==========================================================================', 'Info')

import devices
import interface


def initialize():
    devices.initialize_all()
    interface.initialize_all()
# end function (Initialize)


initialize()


DebugPrint('main.py', '==========================================================================', 'Info')
DebugPrint('main.py', 'Completed Initialization .. Have a great rest of your day!', 'Info')
DebugPrint('main.py', '==========================================================================', 'Info')

#from extronlib.ui import Button
#class FeedbackButton(Button):
#    def __init__(self, UIHost, ID, holdTime=None, repeatTime=None):
#        Button.__init__(UIHost, ID, holdTime, repeatTime)
#        pass

# https://172.16.200.250/web/vtlp/a18a6c71e23b5cce2991c782839f032f837448c2/index.html#/main