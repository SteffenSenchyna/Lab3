from app import globalConf



menu = {
    "1": globalConf.config
}
print("""
Menu
1)Global
2)Interface
3)Dynamic Routing
4)Ping Test
""")


while True:
    response = input("Select a menu option:")
    if response in menu.keys():
        functionCall = menu[response]
        functionCall()
    else:
        print("Please Select a Correct Menu Option")

