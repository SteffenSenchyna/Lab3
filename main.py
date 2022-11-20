from app import globalConfig, intConfig, routeConfig, ping
globalConfig = globalConfig.globalconfiguration()
intConfig = intConfig.intconfiguration()
routeConfig = routeConfig.routeconfiguration()

def globalConfigCall():
    globalConfig.directoryCheck()
    globalConfig.loadDirectories()
    globalConfig.deployCMDS()

def intConfigCall():
    intConfig.menu()

def routeConfigCall():
    routeConfig.menu()

def pingCall():
    ping.main()

menu = {
    "1": globalConfigCall,
    "2": intConfigCall,
    "3": routeConfigCall,
    "4": pingCall
}



while True:
    print("""
Menu
1)Global
2)Interface
3)Dynamic Routing
4)Ping Test
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

