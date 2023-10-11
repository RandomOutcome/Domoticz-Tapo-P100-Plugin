# TP-Link Tapo Plugin
#
# Author: 593304
#
"""
<plugin key="TapoPlugin" name="TP-Link Tapo Plugin" author="999999" version="0.1" externallink="">
    <description>
        <h2>TP-Link Tapo Plugin</h2><br/>
        <p>The plugin will connect to a Tapo device with the given IP address, username(e-mail address) and password.</p>
        <p>Before using this plugin, you have to install the<a href="https://github.com/petretiandrea/plugp100" style="margin-left: 5px">PlugP100 module</a></p>
        <br />
        <br />
    </description>
    <params>
        <param field="Mode1" label="Username" width="250px" required="true"/>
        <param field="Password" label="Password" width="250px" required="true" password="true"/>
        <param field="Address" label="IP address" width="250px" required="true"/>
        <param field="Mode2" label="Debug" width="50px">
            <options>
                <option label="on" value="on"/>
                <option label="Off" value="off" default="off"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

import os
import subprocess
import json

# Simple heartbeat with a 10 secs interval
class Heartbeat():
    def __init__(self):
        self.callback = None
        self.interval = 10

    def setHeartbeat(self, callback):
        Domoticz.Heartbeat(self.interval)
        Domoticz.Log("Heartbeat interval is " + str(self.interval) + ".")
        self.callback = callback
            
    def beatHeartbeat(self):
        self.callback()


class TapoPlugin:
    def __init__(self):
        self.unit = None
        self.deviceInfo = None
        self.lastState = None
        self.username = None
        self.password = None
        self.ip = None
        return

    def tapo_on(self):
        env = os.environ.copy()
        env["TAPO_USERNAME"] = self.username
        env["TAPO_PASSWORD"] = self.password
        env["TAPO_DEVICEIP"] = self.ip
        cmd=['p100.py', 'on']
        result = subprocess.run(cmd, env=env)

    def tapo_off(self):
        env = os.environ.copy()
        env["TAPO_USERNAME"] = self.username
        env["TAPO_PASSWORD"] = self.password
        env["TAPO_DEVICEIP"] = self.ip
        cmd=['p100.py', 'off']
        result = subprocess.run(cmd, env=env)

    def tapo_info(self):
        env = os.environ.copy()
        env["TAPO_USERNAME"] = self.username
        env["TAPO_PASSWORD"] = self.password
        env["TAPO_DEVICEIP"] = self.ip
        cmd=['p100.py', 'info']
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        self.deviceInfo=json.loads(result.stdout)

    def onStart(self):
        Domoticz.Log("onStart called")
        
        # Setting up debug mode
        if (Parameters["Mode2"] != "off"):
            Domoticz.Debugging(1)
            Domoticz.Debug("Debug mode enabled")

        self.ip = Parameters["Address"]
        self.username = Parameters["Mode1"]
        self.password = Parameters["Password"]

        # Setting up heartbeat
        self.heartbeat = Heartbeat()
        self.heartbeat.setHeartbeat(self.update)

        Domoticz.Debug("Tapo object created with IP: " + self.ip)

        # Getting last state to get device type
        self.update(False)

        # Creating device
        self.unit = 1
        if self.unit not in Devices:
            typeName = "Selector Switch"
            switchType = 0
            
            Domoticz.Device(
                Name = self.lastState["PlugDeviceState"]["info"]["DeviceInfo"]["friendly_name"],
                Unit = self.unit,
                TypeName = typeName, 
                Switchtype = switchType,
                Image = 9,
                Options = {}).Create()

        self.update()

        DumpConfigToLog()

        return

    def onStop(self):
        Domoticz.Log("onStop called")
        return

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called; connection: %s, status: %s, description: %s" % (str(Connection), str(Status), str(Description)))
        return

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called; connection: %s, data: %s" % (str(Connection), str(Data)))
        return

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        if Unit != self.unit:
            Domoticz.Error("Unknown device with unit: " + str(Unit))
            return

        commandValue = 1 if Command == "On" else 0
        if self.lastState["PlugDeviceState"]["device_on"] == commandValue:
            Domoticz.Log("Command and last state is the same, nothing to do")
            return
        
        if Command == "On":
            self.tapo_on()
        else:
            self.tapo_off()

        self.update()

        return

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)
        return

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")
        return

    def onHeartbeat(self):
        self.heartbeat.beatHeartbeat()
        return

    def update(self, updateDomoticz = True):
        self.tapo_info()
        if "error_code" in self.deviceInfo.keys():
            self.lastState = None
            Domoticz.Error("Cannot get last state from device error code: " + str(self.deviceInfo["error_code"]))
        else:
            self.lastState=self.deviceInfo
            Domoticz.Debug(self.lastState)

        # Update device
        if self.unit not in Devices or not updateDomoticz:
            return

        powerState = self.lastState["PlugDeviceState"]["device_on"]
        powerStateValue = 1 if powerState else 0
        powerStateStr = "On" if powerState else "Off"
        if (Devices[self.unit].nValue != powerStateValue) or (Devices[self.unit].sValue != powerStateStr):
            Domoticz.Debug("Updating %s (%d, %s)" % (Devices[self.unit].Name, powerStateValue, powerStateStr))
            Devices[self.unit].Update(nValue = powerStateValue, sValue = powerStateStr)

        return

global _plugin
_plugin = TapoPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
