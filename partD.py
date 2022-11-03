# Netw3100-Lab03-PartD
# Connectivity Test Module
# D. Hague
# 2022-11-03



import subprocess
import ipaddress
import socket

validMasks = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32"
]

def main():

    network = validated_input("Please enter a network address with a cidr subnet mask: ")
    
    if len(network.split("/")) > 1:
        mask = network.split("/")[1]

    goodMask = False
    if mask in validMasks:
        goodMask = True

    goodAddr = validIP(network.split("/")[0])
    print(goodAddr)

    
    while goodMask and goodAddr:
        # Tell the user what network is being scanned
        print("===========================================")
        print("Scanning the network: " + network)
        print("Please wait for scanning to finish to view results")
        print("Depending on the size of your network this might take a while")
        print("===========================================")

        # Network scanning code refrence:
        # Source: https://www.opentechguides.com/how-to/article/python/57/python-ping-subnet.html
        # By: Open Tech Guides
        # Prompt the user to input a network address
        networkAddress = network

        # Create the network
        subnet = ipaddress.ip_network(networkAddress)

        # Get all hosts on that network
        allHosts = list(subnet.hosts())

        # Configure subprocess to hide the console window
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

        # For each IP address in the subnet, 
        # run the ping command with subprocess.popen interface
        for i in range(len(allHosts)):
            output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(allHosts[i])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
            
            if "Destination host unreachable" in output.decode('utf-8'):
                print(str(allHosts[i]), "is Offline")

            elif "Request timed out" in output.decode('utf-8'):
                print(str(allHosts[i]), "is Offline")

            else:
                # let user know that specified device is online
                print(str(allHosts[i]), "is Online")
        
        goodAddr = False


def validIP(address):
    ValidIP = False

    Octets = address.split('.')
    try:
        if len(Octets) == 4:
            if int(Octets[0]) >=1 and int(Octets[0])<=255:
                if int(Octets[1]) >=0 and int(Octets[1])<=255:
                    if int(Octets[2]) >=0 and int(Octets[2])<=255:
                        if int(Octets[3]) >=0 and int(Octets[3])<=255:
                            ValidIP = True
    except Exception as error:
        print("IP Address is invalid "+str(error))
        return False
    if ValidIP:
        # print("IP Address is Valid")
        return True
    else:
        print("IP Address is not Valid")
        return False


def validated_input(prompt):
    valid_input = False
    while True:
        value = input(prompt)
        #Error handling
        if len(value) == 0:
            print("Please enter the field")
        if value == "quit":
            raise Exception("Ending Script")
        if value != "":
            break
    return value
            

main()