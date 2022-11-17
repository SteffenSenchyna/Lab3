# A python script that pulls info from network devices one at a time
# D. Hague
# 2022-11-14

import time
from napalm import get_network_driver

deviceList = ["10.1.10.1", "10.1.10.2", "10.1.10.10", "10.1.10.253"]
commands = ["show run"]

def main():
    start = time.time()
    driver = get_network_driver('ios')

    for dev in deviceList:
        device = driver(
            hostname = dev,
            username = "cisco",
            password = "cisco",
            optional_args = {"secret" : "cisco"}
        )

        print("===================================")
        print("conecting ...")
        print("===================================")
        device.open()
        res = device.cli(commands)
        with open("config"+dev+".txt", "w") as f:
            f.write(res["show run"])

        print(res["show run"])
    end = time.time()
    totalTime = end - start
    print("===================================")
    print("Execution time = " + str(totalTime) + " seconds")
    print("===================================")
    

main()
