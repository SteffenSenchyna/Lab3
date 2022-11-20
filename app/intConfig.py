from netmiko import ConnectHandler
import subprocess
import pathlib
import sys
import os
import json
import ipaddress
import re
from netaddr import *
import pprint

class intconfiguration():
    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
        self.secret = ""
        self.filepath_cmd = "None"
        self.filepath_ip = "None"
        self.interfaceCMDS = []
        self.intIP = ""

    def validatedInput(self, prompt):
        valid_input = False
        while True:
            value = input(prompt)
            #Error handling
            if len(value) == 0:
                print("Please enter the field")
            if value == "quit":
                break
            if value != "":
                break
        return value

    def validateInt(self, prompt):
        valid_input = False
        intf_pattern = "^[lLgGeEfF]\S+[0-9]/?[0-9]*"
        regex = re.compile(intf_pattern)
        while True:
            value = input(prompt)
            #Error handling
            if len(value) == 0:
                print("Please enter the field")
            if value == "quit":
                break
            if value != "":
                if re.fullmatch(regex, value):
                    break
                else:
                    print("That does not seem to be a valid interface")  
        return value

    def validateIP(self, prompt):
        while True:
            value = input(prompt)
            #Error handling
            if len(value) == 0:
                print("Please enter the field")
            if value == "quit":
                break
            if value != "":
                try:
                    ipaddress.ip_address(value)
                    break
                except Exception as e:
                    print(e)     
        return value

    def validateSubnet(self, prompt):
        while True:
            value = input(prompt)
            #Error handling
            if len(value) == 0:
                print("Please enter the field")
            if value == "quit":
                break
            if value != "":
                try:
                    netCheck = self.intIP + "/" + value
                    #Using the netaddr library for subnet validation
                    subnetCheck = IPNetwork(netCheck)
                    netmask = subnetCheck.netmask
                    print(netmask)
                    break
                except Exception as e:
                    print(e)     
        return netmask

    def buildScript(self):
        #This function builds the config file in the format of files located in the app/Configs Folder
        #Works in a layered format, user inputs an ip then can enter a as many interfaces as they want until they input quit
        self.username = self.validatedInput("Enter username: ")
        self.password = self.validatedInput("Enter password: ")
        self.secret = self.validatedInput("Enter secret: ")
        counter = 0
        while True:
            print("Input quit to exit the script builder")
            ipAddress = self.validateIP("Enter an IP address: ")
            if ipAddress == "quit":
                break
            self.interfaceCMDS.append({
                    "IP": ipAddress,
                    "CMDS": []
                    })
            interfaces = 0
            while True:
                print(f"Input quit to exit the interface script for {ipAddress}")
                int = self.validateInt(f"Enter interface on {ipAddress}: ")
                if int =="quit":
                    break
                self.intIP = self.validateIP("Enter an interface IP address: ")
                intSubnet = self.validateSubnet("Enter a subnet: ")
                fullInt = "int " + str(int)                 
                fullAddress = "ip address " + str(self.intIP) + " " + str(intSubnet)
                self.interfaceCMDS[counter]["CMDS"].append(fullInt)
                self.interfaceCMDS[counter]["CMDS"].append(fullAddress)
                self.interfaceCMDS[counter]["CMDS"].append("no shutdown")
                interfaces += 1
            print(f"{ipAddress} has {interfaces} interfaces configured")
            counter += 1

    def displayCMDS(self):
        #Displays commands 
        print(self.interfaceCMDS)
        
    def deployCMDS(self):
        #Deploys commands build from the script building function
        if not self.interfaceCMDS:
            print("Please build a script to deploy")
        else: 
            try:
                for i in self.interfaceCMDS:
                    device = {
                    'device_type': 'cisco_ios',
                    'host': i['IP'],
                    'username': self.username,
                    'password': self.password,
                    'secret': self.secret
                    }
                    print("Connecting to ", i["IP"])
                    net_connect = ConnectHandler(**device)
                    net_connect.enable()
                    net_connect.config_mode()
                    check = net_connect.check_config_mode()
                    if check == True:
                        #Bulk Deploy of commands from the build script
                        output = net_connect.send_config_set(i["CMDS"])
                        print("Deploying commands")
                        print("Disconnecting")
                        net_connect.disconnect()
                    else:
                        print('Unable to enter configure terminal for ', i["IP"])
                        print("Disconnecting")
                        net_connect.disconnect()
                print('Commands have been deployed')
            except Exception as e:
                print(e)    
    
    def eraseCMDS(self):
        self.interfaceCMDS = []
        
    

           
    def menu(self):
        menu = {
        "1": self.buildScript,
        "2": self.displayCMDS,
        "3": self.deployCMDS,
        "4": self.eraseCMDS,
        }



        while True:
            print("""
Interface Menu
1)Build Interface Script
2)Show Interface Script 
3)Deploy Interface Script
4)Erase Interface Script
5)Exit
            """)
            response = input("Select a menu option: ")
            if response in menu.keys():
                functionCall = menu[response]
                functionCall()
            elif response == "5":
                break
            else:
                print("Please Select a Correct Menu Option")

