# Domoticz TP-Link TAPO P100 Integration - README TODO
This library adds memory based serial communication, between software components, to an Arduino device.
___
Author: RandomOutcome | Status: Pre-Release
___

### Local non-IO based loopback library implementing SoftwareSerial interface

[![GitHub release](https://img.shields.io/github/v/release/RandomOutcome/LoopbackSerial?display_name=tag)](https://github.com/RandomOutcome/LoopbackSerial/releases/latest) [![License](https://img.shields.io/github/license/RandomOutcome/LoopbackSerial.svg?maxAge=3600)](LICENSE) [![Issues](https://img.shields.io/github/issues/RandomOutcome/LoopbackSerial.svg?maxage=3600)](ISSUES)

This Domoticz plugin allows control of TP-Link Tapo P100 WiFi controlled plugs from within Domoticz, each plug is configured as a separate hardware unit and can be controlled independently.   

### Limitations:

- The plugin has only tested with P100 plugs, other Tapo devices may work as well. 
- The plugin only supports On & Off functionallity and basic monitoring of the device's relay status.
- P100 plugs must be configured first via the Tapo app, once configured the username, password and IP address assigned to each plug are used to configure the devices into Domoticz.
- Depends upon the Python module plugp100.
- Requires Python versions 3.8 and above.

### Features
-   Provides basic on/off relay control for Tapo P100 plugs (may work on other models)local loopback communication, memory based, stream based upon the SoftwareSerial class interface
-   Each plug is configured as a separate Domoticz hardware instance

### Installation

**Plugin:**

    Download the plugin's zip from from Github.
    Copy the downloaded zip file to the directory where Domoticz is installed
    Unzip the downlaoded zip file.
    The plugin wil be installed into [Domoticz Dir]/plugsin/Domotiz-Tapo

    A helper Python model p100.py will also be created in folder when the dowloaded file is unzipped. This file needs to be moved into a folder on the executable path of your Domoticz installation, for example into [Domoticz Dir]/.local/bin on Linux.
   
**Supporting Installation Requirements:** 

    Requires [@petretiandrea](https://github.com/petretiandrea) port of the [plugp100](https://github.com/petretiandrea/plugp100) Python module to be installed, follow the instruction in the link to install. 
    [@petretiandrea](https://github.com/petretiandrea) version of plugp100 required Python v3.10 or above to be installed to work. 
    
    If using Python v3.8 or v3.9, the backported version of [plugip](https://github.com/RandomOutcome/plugp100-3.9) can be used instead, follow the instruction in the link to install.  
    
    Python version prior to 3.8 are not supported. 
    
## Domoticz Configuration:
To-Do

