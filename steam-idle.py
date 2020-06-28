import os
import platform
import time
import sys
from ctypes import CDLL

def get_steam_api():
    if platform.architecture()[0].startswith('32bit'):
        print('Loading Linux 32bit library')
        return CDLL('./libsteam_api_32.so')
    elif platform.architecture()[0].startswith('64bit'):
        print('Loading Linux 64bit library')
        return CDLL('./libsteam_api_64.so')
    else:
        print('Linux architecture not supported')
        sys.exit()

def get_processes():
    return [(int(p), c) for p, c in [x.rstrip('\n').split(' ', 1) for x in os.popen('ps h -eo pid:1,command')]]

def is_ffxiv_running():
    processes = get_processes()
    process_list = ["ffxivboot.exe", "XIVLauncher.exe", "ffxiv_dx11.exe"]

    for process in processes:
        for allowed_process in process_list:
            if allowed_process in process[1]:
                return True

    return False


def wait_for_ffxiv():
    while not is_ffxiv_running():
        time.sleep(1)
        pass
    
if __name__ == '__main__':
    print("Steam integration running. Waiting for FFXIV...")
    wait_for_ffxiv() # Wait for FFXIV to launch
    
    # Start Steam API
    print("Found FFXIV. Starting Steam API...")
    os.environ["SteamAppId"] = "39210"
    get_steam_api().SteamAPI_Init()

    while is_ffxiv_running():
        time.sleep(1)
        pass
    
    print("FFXIV exited. Bye bye")
    sys.exit()
