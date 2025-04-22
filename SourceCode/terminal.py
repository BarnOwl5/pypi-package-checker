import os,time,getpass
import datetime

class User :
    def __init__(self) :
        self.username = getpass.getuser()
        self.timeline = time.strftime("%y/%m/%d")

    def intro(self) :
        global select
        print("        Welcome,",self.username,"\n        Today's Date :",self.timeline)
        print("\n        [1] Check a single package\n        [2] Check packages from a list (.json only)\n        [3] Show help & usage guide\n        [0] Exit")

        select = input("\n        Enter your choice [?] : ")

    def check_single_package():
        pass

    def check_package_list():
        pass

    def show_help():
        pass

while True :
    stool = User()
    stool.intro()

    if select == '1': stool.check_single_package
    elif select == '2': stool.check_package_list
    elif select == '3': stool.show_help
    else : break