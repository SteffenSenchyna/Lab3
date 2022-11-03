from netmiko import ConnectHandler
import subprocess
import pathlib
import sys
import os
import json

class globalconfiguration():
    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
        self.filepath_cmd = "None"
        self.filepath_ip = "None"

    def directoryCheck(self):
        #Checks to see if there is proper file structure and creates directories if needed
        self.directoryIP = str(pathlib.Path(__file__).parent.resolve())+"\IPs"
        self.directoryConfig = str(pathlib.Path(__file__).parent.resolve())+"\Configs"
        try:
            os.makedirs(self.directoryIP)
            os.makedirs(self.directoryConfig)
        except FileExistsError:
            # directory already exists
            pass       

    def loadDirectories(self):
        directoryConfig = str(self.directoryConfig)
        filelistConfig = os.listdir(directoryConfig)
        while True:
            print(filelistConfig)
            response = input("Please Select a Configuration File: ")
            if ".json" in response:
                self.filepath_cmd = str(self.directoryConfig) + "\\" + response
                break
            else:
                response = response + ".json"
            if response in filelistConfig:
                self.filepath_cmd = str(self.directoryConfig) + "\\" + response
                break
            else:
                print("Please Select a Listed File")
    
    def deployCMDS(self):
        device = {
            'device_type': 'cisco_ios',
            'host': 'ip',
            'username': '%s' % self.username,
            'password': '%s' % self.password
            }
        f = open(self.filepath_cmd)
        cmdJSON = json.load(f)
        for i in cmdJSON:
            print("Connecting to ", i["IP"])
            net_connect = ConnectHandler(**device)
            net_connect.config_mode()
            check = net_connect.check_config_mode()
            if check == True:
                outp = net_connect.send_config_set(i["cmds"])
                print("Disconnecting")
                net_connect.disconnect()
            else:
                print('Unable to enter configure terminal for ', i["IP"])
                print("Disconnecting")
                net_connect.disconnect()
        print('Commands have been deployed')




