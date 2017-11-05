#!/usr/bin/python

import avango.daemon
import os


### functions ###
    
def init_keyboard():

    _string = get_event_string(1, "Cherry GmbH")
    
    if _string is None:
        _string = get_event_string(1, "HID 046a:0011")
    
    if _string is None:
        _string = get_event_string(1, "MOSART Semi. 2.4G Keyboard Mouse")
    
    if _string is None:
        _string = get_event_string(1, "Logitech USB Keyboard")
    
    if _string is None:
        _string = get_event_string(1, "Logitech USB Keyboard")
    
    if _string is None:
        _string = get_event_string(1, "DELL Dell QuietKey Keyboard")

    if _string is not None:
        _keyboard = avango.daemon.HIDInput()
        _keyboard.station = avango.daemon.Station('gua-device-keyboard')
        _keyboard.device = _string

        _keyboard.buttons[0] = "EV_KEY::KEY_W"
        _keyboard.buttons[1] = "EV_KEY::KEY_A"
        _keyboard.buttons[2] = "EV_KEY::KEY_S"
        _keyboard.buttons[3] = "EV_KEY::KEY_D"
        _keyboard.buttons[4] = "EV_KEY::KEY_LEFT"
        _keyboard.buttons[5] = "EV_KEY::KEY_RIGHT"
        _keyboard.buttons[6] = "EV_KEY::KEY_UP"
        _keyboard.buttons[7] = "EV_KEY::KEY_DOWN"
        _keyboard.buttons[8] = "EV_KEY::KEY_Q"
        _keyboard.buttons[9] = "EV_KEY::KEY_E"
        _keyboard.buttons[10] = "EV_KEY::KEY_PAGEUP"
        _keyboard.buttons[11] = "EV_KEY::KEY_PAGEDOWN"
        _keyboard.buttons[12] = "EV_KEY::KEY_KPPLUS"
        _keyboard.buttons[13] = "EV_KEY::KEY_KPMINUS"
        _keyboard.buttons[14] = "EV_KEY::KEY_SPACE"
        _keyboard.buttons[15] = "EV_KEY::KEY_LEFTCTRL"
               

        device_list.append(_keyboard)
        print("Keyboard started at:", _string)



## Gets the event string of a given input device.
# @param STRING_NUM Integer saying which device occurence should be returned.
# @param DEVICE_NAME Name of the input device to find the event string for.
def get_event_string(STRING_NUM, DEVICE_NAME):

    # file containing all devices with additional information
    _device_file = os.popen("cat /proc/bus/input/devices").read()
    _device_file = _device_file.split("\n")
    
    DEVICE_NAME = '\"' + DEVICE_NAME + '\"'
    
    # lines in the file matching the device name
    _indices = []

    for _i, _line in enumerate(_device_file):
        if DEVICE_NAME in _line:
            _indices.append(_i)

    # if no device was found or the number is too high, return an empty string
    if len(_indices) == 0 or STRING_NUM > len(_indices):
        return None

    # else captue the event number X of one specific device and return /dev/input/eventX
    else:
        _event_string_start_index = _device_file[_indices[STRING_NUM-1]+4].find("event")
                
        return "/dev/input/" + _device_file[_indices[STRING_NUM-1]+4][_event_string_start_index:].split(" ")[0]






device_list = []

init_keyboard()

avango.daemon.run(device_list)
