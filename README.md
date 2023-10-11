# Domoticz TP-Link TAPO P100 Integration - README Work In Progress
This pliugin provides basic control of TP-Link Tapo P100 devices, with firmware from 2023 onwards, from Domoticz.
___
Author: RandomOutcome | Status: Pre-Release
___

### Domoticz plugin for Tapo P100 control, for Tapo devices with firmware upgrade in 2023 that changed the device communication protocol breaking earlier plugins

[![GitHub release](https://img.shields.io/github/v/release/RandomOutcome/Domoticz-Tapo-P100-Plugin?display_name=tag)](https://github.com/RandomOutcome/Domoticz-Tapo-P100-Plugin/releases/latest) [![License](https://img.shields.io/github/license/RandomOutcome/Domoticz-Tapo-P100-Plugin.svg?maxAge=3600)](LICENSE) [![Issues](https://img.shields.io/github/issues/RandomOutcome/Domoticz-Tapo-P100-Plugin.svg?maxage=3600)](ISSUES)

This Domoticz plugin allows control of TP-Link Tapo P100 WiFi controlled plugs from within Domoticz, each plug is configured as a separate hardware unit and can be controlled independently.   

### Limitations:

- The plugin has only been tested with P100 plugs, although other Tapo devices may work as well.
- Only works on Tapo devices that had their firmware upgrade from late 2022 till 2023
- The plugin only supports On & Off functionallity and basic monitoring of the device's relay status.
- P100 plugs must be configured first via the Tapo app, once configured the username, password and IP address assigned to each plug are used to configure the plug
  devices into Domoticz.
- Depends upon the Python module plugp100.
- Requires Python versions 3.8 and above.

### Features
- Provides basic on/off relay control for Tapo P100 plugs (may work on other models)
- Each plug is configured as a separate Domoticz hardware instance
- Can co-reside with other Domoticz Tapo plugin modules

### Installation

**Plugin:**
- Download the plugin's zip from from Github.
- Copy the downloaded zip file to the directory where Domoticz is installe
- Unzip the downlaoded zip file.
- The plugin wil be installed into **[Domoticz Dir]**/plugsin/Domoticz-Tapo
- If co-installing with other Tapo plugins ensure the directory doesn't clash prior to unzipping, if clashes unzip elsewhere and rename the plugins/Domoticz-Tapo directory
  and manually copy the directory plugins directory and p100.py file into the **[Domoticz Dir]** folder.

- A helper Python model p100.py will also be created in folder when the dowloaded file is unzipped. This file needs to be moved into a folder on the executable path of your
  Domoticz installation, for example into **[Domoticz Dir]**/.local/bin on Linux.

- Restart domoticz.
   
**Supporting Installation Requirements:** 

  Requires [@petretiandrea](https://github.com/petretiandrea) port of the [plugp100](https://github.com/petretiandrea/plugp100) Python module to be installed, follow the 
  instruction in the link to install. [@petretiandrea](https://github.com/petretiandrea) version of plugp100 required Python v3.10 or above to be installed to work. 
    
  If using Python v3.8 or v3.9, the backported version of [plugp100](https://github.com/RandomOutcome/plugp100-3.9) can be used instead, follow the instructions in the link to 
  install.  
    
  Python version prior to 3.8 are not supported. 
    
## Domoticz Configuration:

**Adding P100 Plugs:** 

(https://github.com/RandomOutcome/Domoticz-Tapo-P100-Plugin/images/P100-plugin-config.png)
  
    
## Plugin Implementation Details:
  To-Do

