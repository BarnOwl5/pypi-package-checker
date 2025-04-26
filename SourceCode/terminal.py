import os,time,getpass
from datetime import datetime
import time
import platform, subprocess
from package_cheker import *

def clear_screen() :
    cmd = "cls" if platform.system() == "Windows" else "clear"
    subprocess.call(cmd,shell=True)

def pause_screen() :
    cmd = "pause" if platform.system() == "Windows" else "clear"
    subprocess.call(cmd,shell=True)

class User :
    def __init__(self) :
        self.username = getpass.getuser()
        self.timeline = time.strftime("%y/%m/%d")
        self.history = [] # 결과 누적 저장
    
    def show_recent_packages(self):
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        if not os.path.exists(results_dir):
            print("[ Recent Packages ]\nEmpty.")
            return

        files = [f for f in os.listdir(results_dir) if f.endswith(".json")]
        if not files:
            print("[ Recent Packages ]\nEmpty.")
            return

        print("[Recent Packages ]\n")
        recent = sorted(files, key=lambda f: os.path.getmtime(os.path.join(results_dir, f)), reverse=True)[:3]
        for f in recent:
            path = os.path.join(results_dir, f)
            timestamp = os.path.getmtime(path)
            readable = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{f} (saved: {readable})")

    def intro(self) :
        global select
        clear_screen()
        print("Welcome,",self.username,"\nToday's Date :",self.timeline)
        
        self.show_recent_packages()
        
        print("\n[1] Check a Single Package \n[2] Package History \n[3] Show help & usage guide \n[0] Exit")

        select = input("\nEnter your choice [?] : ")

    def check_single_package(self):
        try : 
            while True :
                clear_screen()
                package_name = input("\nEnter package name (Ctrl+C cancel) : ")
                filename = run_check_flow(package_name)

                if filename : 
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        print("\n [ Result ]")
                        for key, value in data.items() :
                            print(f"{key} : {value}"+"\n")
                    pause_screen()

        except KeyboardInterrupt :
            print("\n\n[!] Cancelled by user. Returning to menu...\n")
            time.sleep(0.5)
            return

    def show_history(self):
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

        while True:
            clear_screen()
            print("\n[ Package Check History ]\n")

            if not os.path.exists(results_dir):
                print("No history found. 'results' folder does not exist.")
                input("\nPress Enter to return to menu...")
                return

            files = [f for f in os.listdir(results_dir) if f.endswith(".json")]
            if not files:
                print("Empty. No .json package records found.")
                input("\nPress Enter to return to menu...")
                return
            for f in sorted(files):
                path = os.path.join(results_dir, f)
                timestamp = os.path.getmtime(path)
                readable_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                print(f"{f}  (saved: {readable_time})")

            show_input = input("\nEnter file name to view (or press 'enter' to return): ").strip()

            # 자동 확장자, 소문자 처리
            if not show_input.endswith(".json"):
                show_input += ".json"
            filename = show_input.lower()
            path = os.path.join(results_dir, filename)

            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    print(f"\n[ {filename} ]")
                    for key, value in data.items():
                        print(f"{key} : {value}")
                    print("\n")  # 여유 줄바꿈

                except Exception as e:
                    print(f"\n[!] Error reading file '{filename}': {e}")
            else:
                return
            
            input("\nPress Enter to return to the list...")

    def show_help(self):
        help_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "help.txt")

        clear_screen()

        print("\n[ Help & Usage Guide ]\n")

        try:
            with open(help_path, "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("help.txt not found.")

        input("\nPress Enter to return to main menu...")



while True :
    stool = User()
    stool.intro()

    if select == '1': stool.check_single_package()
    elif select == '2': stool.show_history()
    elif select == '3': stool.show_help()
    else : 
        print("\nExit Tool...\n")
        time.sleep(1)
        break