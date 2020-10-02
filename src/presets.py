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

import re

import devices
import interface
import utilities
from utilities import DebugPrint


def execute_command(macro_string, button = None):

    #    device:<object>:<command>:<value>
    #    ui:popup:<name>
    #    macro:<name>
    regex_ui = re.compile(r"^(ui:popup):(.*?)$")
    regex_device = re.compile(r"^(device):(.*?):(.*?):(.*?):(.*?)(?::(int|integer|str|string):(.*?)){0,1}$")
    regex_preset = re.compile(r"^(preset):(.*):(.*)$")

    #ui:popup:POP - CAM1 - Control
    if regex_ui.match(macro_string):
        p = regex_ui.match(macro_string)
        if p.group(2):
            devices.TouchPanel.ShowPopup(p.group(2))
        else:
            DebugPrint('execute_button_macro/regex_ui', 'Attempted to handle a malformed command statement: [{}]'.format(macro_string),
                       'Error')

    #device:carbonite:Cut:None:None
    #device:carbonite:KeyOnPreview:On:Keyer:int:1
    elif regex_device.match(macro_string):
        p = regex_device.match(macro_string)

        if p.group(4):

            try:
                driver_object = devices.device_objects[p.group(2)]
                driver_command = p.group(3)

                if p.group(4).lower() == 'none':
                    driver_value = None

                else:
                    driver_value = p.group(4)


                if p.group(5) and p.group(5).lower() != 'none':
                    if p.group(6) and p.group(7):
                        if p.group(6) == 'int' or p.group(6) == 'integer':
                            qualifier = {p.group(5): int(p.group(7))}

                        elif p.group(6) == 'str' or p.group(6) == 'string':
                            qualifier = {p.group(5): p.group(7)}

                        else:
                            qualifier = None

                else:
                        qualifier = None

                DebugPrint('interface.py/execute_command',
                           'Sending Device Driver Command: [{}] [{}] [{}]'.format(driver_command, driver_value, qualifier),
                           'Trace')

                # Run our driver_command
                driver_object.Set(driver_command, driver_value, qualifier)

            except:
                DebugPrint('execute_button_macro/regex_device',
                           'An error occurred sending a command to driver module. [{}]'.format(macro_string),
                           'Error')

                raise

        else:
            DebugPrint('execute_button_macro/regex_device', 'Attempted to handle a malformed command statement: [{}]'.
                       format(macro_string), 'Error')

    elif regex_preset.match(macro_string):
        p = regex_preset.match(macro_string)
        DebugPrint('execute_button_macro/preset', 'We are loading macro #[{}] [{}] [{}]'.
                   format(p.group(2), p.group(3), macro_string))

        execute_preset(int(p.group(2)), stage=p.group(3))

    else:
        if button is not None:
            DebugPrint('execute_button_macro', 'UNRECOGNIZED MACRO STRING! Button: [{}] Attempted to parse: [{}]'.
                       format(button.Name, macro_string), 'Error')

        else:
            DebugPrint('execute_button_macro', 'UNRECOGNIZED MACRO STRING! Attempted to parse: [{}]'.
                       format(macro_string), 'Error')

#end function (execute_button_macro)


def execute_preset_old(preset_number):
    if utilities.config.get_value('presets/preset_{}_enabled'.format(preset_number),
                                  default_value=False, cast_as='boolean') is True:

        preset_name = utilities.config.get_value('presets/preset_{}_name'.format(preset_number),
                                  default_value='Un-named', cast_as='string')

        DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                   'Preset starting execution..', 'Info')

        preset_index = 0
        while preset_index < 50:   # We don't want this loop to run away - 50 steps should be enough
            preset_index += 1

            current_step_enabled = utilities.config.get_value(
                'presets/preset_{}_steps/{}_enabled'.format(preset_number, preset_index),
                default_value=False, cast_as='boolean')


            current_step_data = utilities.config.get_value(
                'presets/preset_{}_steps/{}_data'.format(preset_number, preset_index),
                default_value='None', cast_as='string')

            if ((current_step_enabled is False) and (current_step_data == 'None')):
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Step #{} is not present, so we are done. Execution completed!'.
                           format(preset_index), 'Info')

                break

            elif current_step_enabled is False:
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Skipping step #{} as it is disabled: [{}]'.
                           format(preset_index, current_step_data), 'Debug')
                continue

            # If we get here then we've got valid preset data, AND we're set as enabled. Let's execute!
            else:
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Execute step #{}'.format(preset_index), 'Debug')

                execute_command(current_step_data)

        #FIXME - we really should convert this to a system state
        interface.mainscreen.lblNextPreset.SetText(preset_name)
#end function (execute_preset_old)

def execute_preset(preset_number, stage = 'prepare'):
    if utilities.config.get_value('presets/{}/enabled'.format(preset_number),
                                  default_value=False, cast_as='boolean') is True:

        preset_name = utilities.config.get_value('presets/{}/name'.format(preset_number),
                                  default_value='Un-named', cast_as='string')

        if stage == 'prepare':
            DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                       'Preset preparation stage starting..', 'Info')

        elif stage == 'activate':
            DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                       'Preset activation stage starting..', 'Info')

        else:
            DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                       'Cannot trigger preset. Unknown stage specified!', 'Error')

            return False


        preset_index = 0
        while preset_index < 50:   # We don't want this loop to run away - 50 steps should be enough
            preset_index += 1

            current_step_enabled = utilities.config.get_value(
                'presets/{}/{}/{}/enabled'.format(preset_number, stage, preset_index),
                default_value=False, cast_as='boolean')

            current_step_type = utilities.config.get_value(
                'presets/{}/{}/{}/type'.format(preset_number, stage, preset_index),
                default_value='None', cast_as='string')

            # This means we don't have enough data for a valid step, so we'll discontinue
            if current_step_enabled is False and current_step_type == 'None':
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Step #{} is not present, so we are done. Execution completed!'.
                           format(preset_index), 'Info')

                break

            # This means we probably have enough to continue, but we're disabled we'll just skip to the next preset #
            elif current_step_enabled is False:
                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Skipping step #{} as it is disabled'.format(preset_index), 'Info')

                continue

            # If we get here, we're going to [attempt] to pull in the rest of the data for this preset #,
            # then validate it one-by-one so we can provide good error messages.
            elif current_step_type.lower() == 'device':

                current_step_device = utilities.config.get_value('presets/{}/{}/{}/device'.
                                                                 format(preset_number, stage, preset_index),
                                                                 default_value='None', cast_as='string')

                current_step_command = utilities.config.get_value('presets/{}/{}/{}/command'.
                                                                  format(preset_number, stage, preset_index),
                                                                  default_value='None', cast_as='string')

                current_step_value = utilities.config.get_value('presets/{}/{}/{}/value'.
                                                                format(preset_number, stage, preset_index),
                                                                default_value='None', cast_as='string')

                current_step_qualifier_key = utilities.config.get_value('presets/{}/{}/{}/qualifier_key'.
                                                                        format(preset_number, stage, preset_index),
                                                                        default_value='None', cast_as='string')

                current_step_qualifier_value = utilities.config.get_value('presets/{}/{}/{}/qualifier_value'.
                                                                          format(preset_number, stage, preset_index),
                                                                          default_value='None', cast_as='string')

                current_step_qualifier_value_type = utilities.config.get_value('presets/{}/{}/{}/qualifier_value_type'.
                                                                               format(preset_number, stage, preset_index),
                                                                               default_value='None', cast_as='string')

                # Now let's validate all of our data, and fail gracefully with descriptive error messages along the way
                # If we make it to the bottom if this if/elif struction, then we'll be ready to use all of these
                # variables as they have been sufficiently validated.

                # Check if the device exists in our device_objects dictionary
                if current_step_device == 'None' or current_step_device not in devices.device_objects:
                    DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                               'Skipping step #{} as it specifies an invalid device name: [{}]'.
                               format(preset_index, current_step_device), 'Error')

                    continue

                # Check if the command is in the driver's "Commands" dictionary
                elif current_step_command == 'None' or \
                    current_step_command not in devices.device_objects[current_step_device].Commands:

                    DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                               'Skipping step #{} as it specifies an invalid command for the driver: [{}]'.
                               format(preset_index, current_step_command), 'Error')

                    continue

                # Some commands accept a "None" value, so make sure it's the actual Python NoneType value
                if current_step_value == 'None':
                    current_step_value = None

                # Check if we have qualifiers, and a qualifier value
                # Check if our qualifier value is intended to be casted as an integer or a string
                # Finally, check to see if the data provided can successfully be casted as an integer
                if current_step_qualifier_key != 'None' and current_step_qualifier_value != 'None':
                    if current_step_qualifier_value_type.lower() in ['int', 'integer']:
                            if not current_step_qualifier_value.isdigit():
                                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                                           'Skipping step #{} as it specifies an invalid qualifier value [{}] \
                                           (called for integer but non-integer data was found)'.
                                           format(preset_index, current_step_qualifier_value), 'Error')

                                continue

                            # We'll cast our qualifier value as an integer
                            else:
                                qualifier = {current_step_qualifier_key: int(current_step_qualifier_value)}

                    # We'll cast our qualifier value as a string
                    else:
                        qualifier = {current_step_qualifier_key: current_step_qualifier_value}

                # Our qualifier is "None" (which is valid)
                else:
                    qualifier = None

                DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                           'Executing the following information: [{}] [{}] [{}] [{}]'.
                           format(preset_index, current_step_device, current_step_command, current_step_value,
                                  qualifier), 'Debug')

                try:
                    devices.device_objects[current_step_device].Set(current_step_command, current_step_value, qualifier)

                except:
                    DebugPrint('execute_preset/{}/{}'.format(preset_number, preset_name),
                               'An unknown error occurred executing the following driver command: [{}] [{}] [{}] [{}]'.
                               format(current_step_device, current_step_command, current_step_value, qualifier), 'Error')

        # end while loop

        # Update our system state of "NextPreset" so we can keep our UI in sync
        devices.system_states.Set('NextPreset', preset_number, None)

#end function (execute_preset)

