from app import globalConf

menu = {
    1: globalConf.config()
}
print("""
Menu
1)Global
2)Interface
3)Dynamic Routing
4)Ping Test
""")

response = input("Select a menu option")
