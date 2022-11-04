from netmiko import ConnectHandler
import subprocess
import pathlib
import sys
import os
import json
import ipaddress
import re
from netaddr import *

class intconfiguration():
    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
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
        while True:
            print("Input quit to exit the script builder")
            ipAddress = self.validateIP("Enter an IP address: ")
            if ipAddress == "quit":
                break
            while True:
                interfaces = 0
                print(f"Input quit to exit the interface script for {ipAddress}")
                int = self.validateInt(f"Enter interface on {ipAddress}: ")
                if int =="quit":
                    break
                self.intIP = self.validateIP("Enter an interface IP address: ")
                intSubnet = self.validateSubnet("Enter a subnet (X.X.X.X): ")                 
                fullAddress = "ip address " + self.intIP + " " + intSubnet
                self.interfaceCMDS.append({
                    "IP": ipAddress,
                    "CMDS": [
                        int,
                        fullAddress
                    ]
                    })
                interfaces += 1
                print(f"{ipAddress} has {interfaces} interfaces configured")

    def displayCMDS(self):
        print(self.interfaceCMDS)


           
    def menu(self):
        menu = {
        "1": self.buildScript,
        "2": self.displayCMDS,
        "3": "3",
        "4": "4",
        "5": "5"
        }



        while True:
            print("""
            Menu
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
            else:
                print("Please Select a Correct Menu Option")

obj = intconfiguration()
obj.menu()