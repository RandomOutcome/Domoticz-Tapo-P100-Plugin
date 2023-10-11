#!/usr/bin/python3.9
import os, sys
import asyncio
import json
from typing import Any, Dict, List

from plugp100.api.plug_device import PlugDevice
from plugp100.api.tapo_client import TapoClient
from plugp100.common.credentials import AuthCredential

credentials = None
client = None
plug = None
deviceInfo = None
loop = None
username = None
password = None
ip = None
output = None

async def async_tapo_login():
    global credentials, client, plug
    credentials = AuthCredential(username, password)
    client = TapoClient(credentials, ip)
    await client.initialize()
    plug = PlugDevice(client)

async def async_tapo_logout():
    global client
    await client.close()

async def async_tapo_on():
    global plug
    await plug.on()

async def async_tapo_off():
    global plug
    await plug.off()

async def async_tapo_info():
    global plug, deviceInfo
    deviceInfo = await plug.get_state()

def tapo_login():
    global loop
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_tapo_login())
    loop.run_until_complete(asyncio.sleep(0.1))

def tapo_logout():
    global loop
    loop.run_until_complete(async_tapo_logout())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()

def tapo_on():
    global loop
    tapo_login()
    loop.run_until_complete(async_tapo_on())
    loop.run_until_complete(asyncio.sleep(0.1))
    tapo_logout()

def tapo_off():
    global loop
    tapo_login()
    loop.run_until_complete(async_tapo_off())
    loop.run_until_complete(asyncio.sleep(0.1))
    tapo_logout()

def tapo_info():
    global loop
    tapo_login()
    loop.run_until_complete(async_tapo_info())
    loop.run_until_complete(asyncio.sleep(0.1))
    tapo_logout()


def unwrap_object(any_object, level=0):
    output = ""

    object_type = type(any_object)

    if str(object_type) == "<class 'plugp100.common.functional.tri.Success'>":
        output+='{"Success": '

        sub_object=any_object.__dict__
        output+=unwrap_object(sub_object, level+1)

        output+='}'

        return output

    elif str(object_type) == "<class 'plugp100.responses.device_state.PlugDeviceState'>":
        output+='{"PlugDeviceState": '

        sub_object=any_object.__dict__
        output+=unwrap_object(sub_object, level+1)

        output+='}'

        return output

    elif str(object_type) == "<class 'plugp100.responses.device_state.DeviceInfo'>":
        output+='{"DeviceInfo": '

        sub_object=any_object.__dict__
        output+=unwrap_object(sub_object, level+1)

        output+='}'

        return output

    elif str(object_type) == "<class 'tuple'>":
        output+='{' 

        try:
            items = any_object.items()
        except (AttributeError, TypeError):
            output+=unwrap_object(any_object, level+1)
            pass
        else: 
            item_count = len(items)
            count = 0
            for item in items: 
                output+=unwrap_object(item, level+1)
                count+=1
                if ( count < item_count ):
                    output+=', '

        output+='}'

        return output

    elif str(object_type) == "<class 'dict'>":
        #output+='{' 

        ok = True
        try:
            items = any_object.items()
        except (AttributeError, TypeError):
            output+=unwrap_object(any_object, level+1)
            ok = False
            pass

        if ok:
            output+='{'
            keys_count = len(items)
            key_count = 0
            for key, values in items: 
                #output+='{"' + key + '": '
                output+='"' + key + '": '

                output+=unwrap_object(values, level+1)
                
                #ok = True
                #try:
                #    values_count = len(values)
                #except (AttributeError, TypeError):
                #    print("DICT KEY ERROR")
                #    output+=unwrap_object(values, level+1)
                #    ok = False
                #    pass

                #if ok:
                #    print(key, values)
                #    value_count = 0
                #    for value in values:
                #        output+=unwrap_object(value, level+1)
                #        value_count+=1
                #        if ( value_count < values_count ):
                #            output+=', '

                key_count+=1
                if ( key_count < keys_count ):
                    output+=', '

                #output+='}'
            output+='}'

        #output+='}'

        return output

    elif str(object_type) == "<class 'str'>":
        return '"'+any_object+'"'

    elif str(object_type) == "<class 'bool'>":
        if any_object:
            return "1"
        else:
            return "0"

    elif str(object_type) == "<type 'NoneType'>":
        return '"None"'

    else:
        return '"'+str(any_object)+'"'
   

if __name__ == "__main__":
    if len(sys.argv) == 5:
        username = sys.argv[2]
        password = sys.argv[3]
        ip       = sys.argv[4]

        if sys.argv[1].lower() == "info":
            tapo_info()
            if deviceInfo.is_failure():
                print(deviceInfo)
            else:
                result=unwrap_object(deviceInfo)
                print(json.dumps(json.loads(result)["Success"]["value"]))

        elif sys.argv[1].lower() == "on":
            tapo_on()

        elif sys.argv[1].lower() == "off":
            tapo_off()

        else:
            print('{"error_code": -1}')

    elif len(sys.argv) == 2:
        username = os.environ.get('TAPO_USERNAME', None)
        password = os.environ.get('TAPO_PASSWORD', None)
        ip       = os.environ.get('TAPO_DEVICEIP', None)

        if username is None or password is None or ip is None:
            print('{"error_code": -2}')

        elif sys.argv[1].lower() == "info":
            tapo_info()
            if deviceInfo.is_failure():
                print(deviceInfo)
            else:
                result=unwrap_object(deviceInfo)
                print(json.dumps(json.loads(result)["Success"]["value"]))

        elif sys.argv[1].lower() == "on":
            tapo_on()

        elif sys.argv[1].lower() == "off":
            tapo_off()

        else:
            print('{"error_code": -1}')

    else:
        print('{"error_code": -2}')

else:
    print('{"error_code": -3}')
