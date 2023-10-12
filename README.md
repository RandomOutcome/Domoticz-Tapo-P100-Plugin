# Domoticz TP-Link TAPO P100 Integration
This plugin provides basic control of TP-Link Tapo P100 devices, with firmware from 2023 onwards, from Domoticz.
___
Author: RandomOutcome | Status: Pre-Release
___

### Domoticz plugin for Tapo P100 control, for Tapo devices with firmware upgrade in 2023 that changed the device communication protocol breaking earlier plugins

[![GitHub release](https://img.shields.io/github/v/release/RandomOutcome/Domoticz-Tapo-P100-Plugin?display_name=tag)](https://github.com/RandomOutcome/Domoticz-Tapo-P100-Plugin/releases/latest) [![License](https://img.shields.io/github/license/RandomOutcome/Domoticz-Tapo-P100-Plugin.svg?maxAge=3600)](LICENSE) [![Issues](https://img.shields.io/github/issues/RandomOutcome/Domoticz-Tapo-P100-Plugin.svg?maxage=3600)](ISSUES)

This Domoticz plugin allows control of TP-Link Tapo P100 WiFi controlled plugs from within Domoticz, each plug is configured as a separate hardware unit and can be controlled independently.   
The plugin is based on the [Domoticz-Tapo plugin](https://github.com/593304/Domoticz-Tapo), which has stopped working due to a change in firmware cloud upated rolled out to the plugs.  

### Limitations:

- The plugin has only been tested with P100 plugs, although other Tapo devices may work as well.
- Only works on Tapo devices that had their firmware upgrade from late 2022 till 2023
- The plugin only supports On & Off functionallity and basic monitoring of the device's relay status.
- P100 plugs must be configured first via the Tapo app, once configured the username, password and IP address assigned to each plug are used to configure the plug
  devices into Domoticz.
- Depends upon the Python library plugp100.
- Requires Python versions 3.8 and above.

### Features
- Provides basic on/off relay control for Tapo P100 plugs (may work on other models)
- Each plug is configured as a separate Domoticz hardware instance
- Can co-reside with other Domoticz Tapo plugin modules

### Installation

**Plugin:**
- Download the plugin's zip from from Github.
- Copy the downloaded zip file to the directory where Domoticz is installed
- Unzip the downlaoded zip file.
- The plugin wil be installed into **[Domoticz Dir]**/plugins/Domoticz-Tapo
- If co-installing with other Tapo plugins ensure the directory doesn't clash prior to unzipping. If clashes would oocur unzip elsewhere and rename the plugins/Domoticz-Tapo
  directory and manually copy the directory plugins directory and p100.py file into the **[Domoticz Dir]** folder.
- A helper Python model p100.py will also be created in folder when the dowloaded file is unzipped. This file needs to be moved into a folder on the executable path of your
  Domoticz installation, for example **[Domoticz Dir]**/.local/bin on Linux.

- Restart Domoticz.
   
**Python Library Module Requirements:** 

  Requires [@petretiandrea](https://github.com/petretiandrea) port of the [plugp100](https://github.com/petretiandrea/plugp100) Python module to be installed, follow the 
  instruction in the link to install. [@petretiandrea](https://github.com/petretiandrea) version of plugp100 requires Python v3.10 or above to be installed to work. 
    
  If using Python v3.8 or v3.9, the backported version of [plugp100](https://github.com/RandomOutcome/plugp100-3.9) can be used instead, follow the instructions in the link to 
  install.  
    
  Python versions prior to 3.8 are not supported. 
    
## Domoticz Configuration:

**Adding P100 Plugs:** 

To add a Tapo plug device in Domoticz, select Hardware from the mention scroll down to the configuration form.
Enter a Name for the device's function, e.g. Lounge Rear Right Light, select the type "TP-Link Tapo Plugin" from the type dropdown.
Select any logging details you wish to record via the tick boxes.
Set Data Timeout to disabled.
Set the Username (Tapo email address), Password and devices IP address as configured in the Tapo App when you setup the plug.
Set Debug to off (unless having issues 

Click Add.

![Domoticz Plugin](images/P100-plugin-config.png?raw=true "Domoticz Plugin Config")

If changing details highlight the Hardware device in the list you wish to change, modify the details as required in the same form as above, then click Update.
To remove a device, highlight the Hardware device to remove and click Delete.

**Usage:** 

The configured plug device should now appear in the Switches panel and can be controlled from here by clicing on the devices icon.  
You can also:
- View the log of the device usages.
- Setup timers to automatically control the device.
- Edit the device's Domoticz settings and icon.
- Setup notifications to be sent when using the device.

![Domoticz Usage](images/P100-Switch.png?raw=true "Domoticz P100 Switch")

## Plugin Implementation Details:

The plugin uses a losely coupled implementation to control P100 (and potentially other Tapo) devices. The *plugin.py* module provides the interface to Domoticz to
request *On/Off* actions and request plug status. This calls a command line module *p100.py* to communicate with the plug, *p100.py* must be located in the Domoticz 
execution Path. The *p100.py* module can be used from the command line directly if wished (details below).

The loosely coupled approach has been adopted as the plugp100 library uses an asyncio approach, which causes errors if implemented directly inside a Domoticz
*plugin.py* module.

For security the username, password and ip address are passed to the *p100.py* module via the environment so the details will not be visible to system utilities.

The plugin.py module itself is based upon [593304's](https://github.com/593304/Domoticz-Tapo) plugin from the Domoticz [Plugin wiki age](https://www.domoticz.com/wiki/Plugins).

**command line usage**

  ```python p100.py [on|off|info] [username] [password] [ip]```

  Turn a plug *on* / *off* or request device status *info*rmation (json format response)

*or*

  ```python p100.py [on|off|info]```

  with enviroment variables:
  - ***TAPO_USERNAME*** for the username/email configured in the Tapo App for the device
  - ***TAPO_PASSWORD*** for the password configured in the Tapo App for the device
  - ***TAPO_DEVICEIP*** for the devices IP address

