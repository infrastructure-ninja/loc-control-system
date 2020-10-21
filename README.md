# Control System for LoC Lutheran

## Design Features

### Configuration File
Nearly every detail of the control system is intended to be read out of a JSON file and can be updated, re-uploaded via sftp and be re-read without restarting the control processor or interrupting the running program.

Many portions of the UI will reconfigure itself based on settings in the file, such as which cameras are enabled, and which presets are currently built inside the system. There are more than a handful of buttons that do not have hard-coded functions, but are configured using the configuration file and the same preset primitives available (like showing a UI popup). 

### Presets (Scenes)
The preset engine is one of the most powerful aspects of the system design. Anything that can be accomplished with "commands/values/qualifiers" in the Extron GlobalScripter driver module can immediately be brought to bear inside a system preset.

Presets have two components: a **prepare** phase, and an **activate** phase. A primary design principle of the entire system is that the user should always be able to see/build what they're going to do on the *preview* monitor, before being able to "take" it to *program*.

Therefore, activating a preset in the "prepare" phase should ***never*** make changes to anyone on-air on the program bus, the audio channels going out to air, etc..

It is subsequently the job of the "activate" phase to move that over to the program bus, and do whatever things are called for during this intentional transition.

There are currently three supported primitives for a preset step:

 - delay
 - device
 - ui

Work is still in progress to develop additional preset primitives - including one that will allow a preset to know that performing this step of a preset is not 'safe' (if a camera is on-air for example).

#### Example 1 - Set the "MLEPresetSource" to "HDMI 2" on the "carbonite" device
          "1": {
            "enabled": true,
            "type": "device",
            "device": "carbonite",
            "command": "MLEPresetSource",
            "value": "HDMI 2",
            "qualifier_key": "None",
            "qualifier_value": "None",
            "qualifier_value_type": ""
          }

#### Example 2 - Set the "InputMute" to "On" on the "soundboard" device for channel "5"
          "1": {
            "enabled": true,
            "type": "device",
            "device": "soundboard",
            "command": "InputMute",
            "value": "On",
            "qualifier_key": "Channel",
            "qualifier_value": "5",
            "qualifier_value_type": "string"
          },

#### Example 3 - Delay for 2 seconds before continuing with preset stage execution
         "4": {
            "enabled": true,
            "type": "delay",
            "seconds": "2"
          },


## Devices Used
 - Extron DMP 128 Plus
 - Extron DXP 88 HD Plus
 - Extron IPL T Pro S6
 - Extron SMD 101
 - Extron SMP 351
 - Extron TLI 101 Pro
 - Ross Video Carbonite Black Solo 109 Frame
 - Yamaha TF5 sound console
