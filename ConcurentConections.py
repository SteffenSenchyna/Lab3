# A python script that pulls info from network devices cocurrently
# D. Hague
# 2022-11-14


from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import time
nr = InitNornir(config_file="C:\\Lab03\\Lib\\site-packages\\nornir\\plugins\\inventory\\config.yaml")

def main():
    # print(nr.inventory.hosts)
    # print(nr.inventory.groups)
    result = nr.run(
        task=netmiko_send_command,
        # Consider using show arp or another command that doen't need privaleged access to run
        command_string="show run"
    )

    print_result(result)

start = time.time()
main()
end = time.time()
totalTime = end - start
print("===================================")
print("Execution time = " + str(totalTime) + " seconds")
print("===================================")
