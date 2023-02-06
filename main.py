from login import login
from menu import menuHandler

def main():
    print("""\n
--------------------
| Mitt Käk! script |
| by Pigges        |
--------------------\n\n""")

    credentials, profile = login()

    menuHandler(credentials, profile)


main()