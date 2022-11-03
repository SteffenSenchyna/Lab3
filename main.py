from app import globalConf
globalConfig = globalConf.globalconfiguration()

def globalConfigCall():
    globalConfig.directoryCheck()
    globalConfig.loadDirectories()
    globalConfig.deployCMDS()

menu = {
    "1": globalConfigCall
}

print("""
Menu
1)Global
2)Interface
3)Dynamic Routing
4)Ping Test
""")
response = input("Please Select a Menu Option: ")
while True:
    if response in menu.keys():
        functionCall = menu[response]
        functionCall()
    else:
        print("Please Select a Listed Menu Option")

