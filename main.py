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


