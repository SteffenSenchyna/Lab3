from app import globalConfig
globalConfig = globalConfig.globalconfiguration()

def globalConfigCall():
    globalConfig.directoryCheck()
    globalConfig.loadDirectories()
    globalConfig.deployCMDS()



menu = {
    "1": globalConfig.config
}

print("""
Menu
1)Global
2)Interface
3)Dynamic Routing
4)Ping Test
""")

response = input("Select a menu option")
print("test")

while True:
    response = input("Select a menu option:")
    if response in menu.keys():
        functionCall = menu[response]
        functionCall()
    elif response == "5":
        break
    else:
        print("Please Select a Correct Menu Option")

