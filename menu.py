from fetch import fetch
import json, sys

states = [
    'menu',
    'ordersCurrent',
    'exit'
]

options = [
    "Current Orders",
    "Exit"
]

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

def menuHandler(credentials, profile):
    menu = Menu(credentials, profile)
    while True:
        menu.__getattribute__(states[menu.state])()

class Menu:
    def __init__(self, credentials, profile) -> None:
        self.credentials = credentials
        self.profile = profile

        self.offline = False
        self.state = 0

        # Check wether the program should run in offline mode
        if not fetch('get', 'login', credentials):
            print("Running in Offline mode.\nCan't fetch any new data.")
            self.offline = True

        print(f"\n\nWelcome, {profile.get('name')} to Mitt Käk! script!")
        
    
    def menu(self):
        while True:
            try:
                print("\nMain Menu\n----------")

                for i in range(len(options)):
                    print(f"{i+1}. {options[i]}")

                print("----------")

                answer = int(input(f"Choose [1-{len(options)}]: "))

                if answer < 0 or answer > len(options):
                    print("\nInvalid number!")
                    continue

                self.state = answer
                break
            except:
                print("\nInvalid input!")

    def ordersCurrent(self):
        # If the user is Offline, check if we have data saved, otherwise return to main menu
        if (self.offline):
            try:
                f = open('data.json', 'r')
                orders = json.loads(f.readlines()).get('orders')
            except:
                print("You are Offline and this data isn't saved.\nWhen you are connected again,\nyou can rerun this script.")
                self.state = 0
                return
        else:
            # The user is Online, get latest data from servers
            orders = json.loads(fetch('get', 'orders/current', self.credentials))

        # If we continue, we have orders
        print("\n\nYour Orders:\n")
        ordersLoop('Current Week', orders.get('current'))
        ordersLoop('Next Week', orders.get('next'))

        input("Enter to CONTINUE: ")

        self.state = 0

    def exit(self):
        print("Goodbye!")
        sys.exit()

def ordersLoop(name, orders):
    if not orders:
        return

    print(name + '\n----------')
    for day in days:
        print(day.capitalize() + ': ', end='')
        if orders.get(day):
            print(orders[day]['dish']['name'])
        else:
            print('None')
    print('----------\n')