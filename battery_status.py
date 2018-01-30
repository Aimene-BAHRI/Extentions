#!/usr/bin/env python3

import subprocess
import time


def read_status_percentage():
    command = "upower -i $(upower -e | grep BAT) | grep --color=never -E percentage|xargs|cut -d' ' -f2|sed s/%//"
    get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    return get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")

def read_status_AC():
    command = "upower -i $(upower -e | grep BAT) | grep --color=never -E state|xargs|cut -d' ' -f2|sed s/%//"
    get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    return get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")

def take_action():
    " the commands to run if charged over 90% or below 20% or 10% in case of danger."
    state_danger = "notify-send 'charged less then 10%. Please save your work!' ""PC is about to shutdown"
    while True:
        charge = int(read_status_percentage())
        state = read_status_AC()
        print charge
        if charge >= 90 and 'charging' == state:
            charge_above = "notify-send -u critical 'charged over 90%. Please unplug your AC adapter!' "" Charging:{} ".format(
                charge)
            subprocess.Popen(["/bin/bash", "-c", charge_above])
        elif 20 >= charge >= 10 and 'discharging' == state:
            charge_below = "notify-send 'charged below 20%. Please plug your AC adapter!' "" Charging:{} ".format(
                charge)
            subprocess.Popen(["/bin/bash", "-c", charge_below])
        elif charge < 10:
            subprocess.Popen(["/bin/bash", "-c", state_danger])
            time.sleep(60)
            # TODO: FOR EXAMPLE ADD SUSPEND COMMAND-LINE TO SAVE YOUR WORK
            ".........................."

        else:
            " No need for notifications during the interval (gap) [20-90]"
            " Make your favorable loop notifications timing in time.sleep() function 10 second for example"
        time.sleep(10)

take_action()
