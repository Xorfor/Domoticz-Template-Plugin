#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Basic Python Plugin Example
    Author: Xorfor

"""

"""
<plugin key="xfr_template" name="Domoticz Python Plugin Example" author="Xorfor" version="2.0.0">
    <params>
        <!--
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="80"/>
        -->
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz


class BasePlugin:

    ########################################################################################
    """
        Constants

        The onHeartbeat method is called every 10 seconds.
            self.__HEARTBEATS2MIN is the number of heartbeats per minute. By using
            self.__HEARTBEATS2MIN * self.__MINUTES you can specify the frequency in
            minutes of updating your devices in the onHeartbeat method.
    """

    __HEARTBEATS2MIN = 6
    __MINUTES = 1

    """
        Constants which can be used to create the devices. Look at onStart where 
        the devices are created.
            self.__UNUSED, the user has to add this devices manually
            self.__USED, the device will be directly available
    """
    __UNUSED = 0
    __USED = 1

    """
        Device Unit numbers

        Define here your units numbers. These can be used to update your devices.
        Be sure the these have a unique number!
    """
    # Device units
    __UNIT_NR01 = 1
    __UNIT_NR02 = 2
    __UNIT_NR03 = 3
    __UNIT_NR04 = 4

    ########################################################################################
    """
        Device definitions
    
            0       1       2           3       4           5           6
            id,     name,   named type,  type,   subtype,    options,    used
    """
    __UNITS = [
        [__UNIT_NR01, "Test 1", "Text", None, None, {}, __USED],
        [__UNIT_NR02, "Test 2", None, 80, 5, {}, __USED],
        [__UNIT_NR03, "Test 3", 80, 5, {}, __USED],
        [__UNIT_NR04, "Test 4", 80, 5, {}, __USED],
    ]

    ########################################################################################

    def __init__(self):
        self.__runAgain = 0

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand: {}, {}, {}, {}".format(Unit, Command, Level, Hue))

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug(
            "onConnect: {}, {}, {}".format(Connection.Name, Status, Description)
        )

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect: {}".format(Connection.Name))

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat")
        self.__runAgain -= 1
        if self.__runAgain <= 0:
            self.__runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
            # Execute your command
        else:
            Domoticz.Debug(
                "onHeartbeat - run again in {} heartbeats".format(self.__runAgain)
            )

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage: {}, {}".format(Connection.Name, Data))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug(
            "onNotification: {}, {}, {}, {}, {}, {}, {}".format(
                Name, Subject, Text, Status, Priority, Sound, ImageFile
            )
        )

    def onStart(self):
        # Debug level
        Domoticz.Debug("onStart")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)
        #
        # Validate parameters
        #
        # Check if images are in database
        if "xfr_template" not in Images:
            Domoticz.Image("xfr_template.zip").Create()
        try:
            image = Images["xfr_template"].ID
        except:
            image = 0
        Domoticz.Debug("Image created. ID: " + str(image))
        #
        # Create devices
        for unit in self.__UNITS:
            if unit[0] not in Devices:
                if unit[2] is None:
                    Domoticz.Device(
                        Unit=unit[0],
                        Name=unit[1],
                        Type=unit[3],
                        Subtype=unit[4],
                        Options=unit[5],
                        Used=unit[6],
                    ).Create()
                else:
                    Domoticz.Device(
                        Unit=unit[0],
                        Name=unit[1],
                        TypeName=unit[2],
                        Options=unit[5],
                        Used=unit[6],
                    ).Create()
        #
        # Log config
        DumpConfigToLog()
        #
        # Connection

    def onStop(self):
        Domoticz.Debug("onStop")


global _plugin
_plugin = BasePlugin()


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


################################################################################
# Generic helper functions
################################################################################
def DumpConfigToLog():
    # Show parameters
    Domoticz.Debug("Parameters count.....: " + str(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter '" + x + "'...: '" + str(Parameters[x]) + "'")
        # Show settings
        Domoticz.Debug("Settings count...: " + str(len(Settings)))
    for x in Settings:
        Domoticz.Debug("Setting '" + x + "'...: '" + str(Settings[x]) + "'")
    # Show images
    Domoticz.Debug("Image count..........: " + str(len(Images)))
    for x in Images:
        Domoticz.Debug("Image '" + x + "...': '" + str(Images[x]) + "'")
    # Show devices
    Domoticz.Debug("Device count.........: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device...............: " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device Idx...........: " + str(Devices[x].ID))
        Domoticz.Debug(
            "Device Type..........: "
            + str(Devices[x].Type)
            + " / "
            + str(Devices[x].SubType)
        )
        Domoticz.Debug("Device Name..........: '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue........: " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue........: '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device Options.......: '" + str(Devices[x].Options) + "'")
        Domoticz.Debug("Device Used..........: " + str(Devices[x].Used))
        Domoticz.Debug("Device ID............: '" + str(Devices[x].DeviceID) + "'")
        Domoticz.Debug("Device LastLevel.....: " + str(Devices[x].LastLevel))
        Domoticz.Debug("Device Image.........: " + str(Devices[x].Image))


def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    if Unit in Devices:
        if (
            Devices[Unit].nValue != nValue
            or Devices[Unit].sValue != sValue
            or Devices[Unit].TimedOut != TimedOut
            or AlwaysUpdate
        ):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Debug(
                "Update "
                + Devices[Unit].Name
                + ": "
                + str(nValue)
                + " - '"
                + str(sValue)
                + "'"
            )


def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        if Devices[Unit].Options != Options:
            Devices[Unit].Update(
                nValue=Devices[Unit].nValue,
                sValue=Devices[Unit].sValue,
                Options=Options,
            )
            Domoticz.Debug(
                "Device Options update: " + Devices[Unit].Name + " = " + str(Options)
            )


def UpdateDeviceImage(Unit, Image):
    if Unit in Devices and Image in Images:
        if Devices[Unit].Image != Images[Image].ID:
            Devices[Unit].Update(
                nValue=Devices[Unit].nValue,
                sValue=Devices[Unit].sValue,
                Image=Images[Image].ID,
            )
            Domoticz.Debug(
                "Device Image update: "
                + Devices[Unit].Name
                + " = "
                + str(Images[Image].ID)
            )


def DumpHTTPResponseToLog(httpDict):
    if isinstance(httpDict, dict):
        Domoticz.Debug("HTTP Details (" + str(len(httpDict)) + "):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                Domoticz.Debug("....'" + x + " (" + str(len(httpDict[x])) + "):")
                for y in httpDict[x]:
                    Domoticz.Debug("........'" + y + "':'" + str(httpDict[x][y]) + "'")
            else:
                Domoticz.Debug("....'" + x + "':'" + str(httpDict[x]) + "'")
