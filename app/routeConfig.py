from netmiko import ConnectHandler
import ipaddress
import re
from netaddr import *
import pprint

class routeconfiguration():
    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
        self.secret = ""
        self.routeCMDS = []
        self.netIP = ""
        self.eigrpNet = ""

    def validateInput(self, prompt):
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
                    netCheck = self.netIP + "/" + value
                    #Using the netaddr library for subnet validation
                    subnetCheck = IPNetwork(netCheck)
                    netmask = subnetCheck.netmask
                    break
                except Exception as e:
                    print(e)     
        return netmask


    def validateWildcard(self, prompt):
        #Returns hostmask instead of subnet, but takes subnet mask input  
        while True:
            value = input(prompt)
            #Error handling
            if len(value) == 0:
                print("Please enter the field")
            if value == "quit":
                break
            if value != "":
                try:
                    netCheck = self.eigrpNet + "/" + value
                    #Using the netaddr library for subnet validation
                    subnetCheck = IPNetwork(netCheck)
                    hostmask = subnetCheck.hostmask
                    break
                except Exception as e:
                    print(e)   
        return hostmask

    def buildScript(self):
        #This function builds the config file in the format of files located in the app/Configs Folder
        #Works in a layered format, user inputs an ip then can enter a as many eigrp AS's and as many networks for each AS
        #The user just has to enter quit to jump back up a config layer, similiar to the cd .. command 
        self.username = self.validateInput("Enter username: ")
        self.password = self.validateInput("Enter password: ")
        self.secret = self.validateInput("Enter secret: ")
        counter = 0
        while True:
            print("Input quit to exit the script builder")
            ipAddress = self.validateIP("Enter an IP address: ")
            if ipAddress == "quit":
                break
            self.routeCMDS.append({
                    "IP": ipAddress,
                    "CMDS": []
                    })
            while True:
                networks = 0
                print(f"Input quit to exit the routing script for {ipAddress}")
                asystem = self.validateInput(f"Enter EIGRP AS for {ipAddress}: ")
                if asystem =="quit":
                    break
                fullAS = "router eigrp " + str(asystem)                 
                self.routeCMDS[counter]["CMDS"].append(fullAS)
                while True:
                    print("Input quit to stop EIGRP network input")
                    self.eigrpNet = self.validateIP("Enter network address: ")
                    if self.eigrpNet == "quit":
                        break
                    ipWildcard = self.validateWildcard("Enter a subnet: ")
                    fullNetwork = "network " + str(self.eigrpNet) + " " + str(ipWildcard)
                    self.routeCMDS[counter]["CMDS"].append(fullNetwork)
                    networks += 1
                    print(f"{ipAddress} has EIGRP AS {asystem} has {networks} networks configured")
            counter += 1

    def displayCMDS(self):
        print(self.routeCMDS)
        
    def deployCMDS(self):

        if not self.routeCMDS:
            print("Please build a script to deploy")
        else: 
            try:
                for i in self.routeCMDS:
                    device = {
                    'device_type': 'cisco_ios',
                    'host': i["IP"],
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
                        print("Deploying commands")
                        output = net_connect.send_config_set(i["CMDS"])
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
        self.routeCMDS = []
        
        

           
    def menu(self):
        menu = {
        "1": self.buildScript,
        "2": self.displayCMDS,
        "3": self.deployCMDS,
        "4": self.eraseCMDS,
        }



        while True:
            print("""
Routing Menu
1)Build Routing Script (EIGRP)
2)Show Routing Script 
3)Deploy Routing Script
4)Erase Routing Script
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
