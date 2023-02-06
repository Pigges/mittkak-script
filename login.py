from base64 import b64encode
from getpass import getpass
from fetch import fetch
import sys, json

def login():
    credentials = getCredentials()

    try:
        f = open('data.json', 'r')
        profile = json.loads(f.readlines()).get('profile')
    except:    
        profile = json.loads(fetch('get', 'login', credentials))

        # Exit if failed to log in
        if profile.get('status') == 401:
            print("Invalid credentials, try again by rerunning this script.")
            sys.exit()
    
    return credentials, profile


def getCredentials():
    # If this is successful, it means that credentials are saved and we can skip asking for credentials
    try:
        f = open('.credentials', 'r')
        credentials = f.readline()
        f.close()
    except:
        print('Login to Mitt Käk!\n--------------------')
        credentials = askCredentials()

    return credentials


def askCredentials():
    mail = validInput(input, 'Email: ', 'email', '@.')
    password = validInput(getpass, 'Password: ', 'password')

    userPass = (mail + ':' + password).encode()

    return b64encode(userPass).decode()

def validInput(method, text, name, constrains=''):
    """Make sure the input are valid.

    Arguments:
    method -- method to be used (input or getpass)
    text -- the input text
    name -- the word it will use when input is invalid
    constrains -- characters needed to be in the input in order for it to be valid
    """
    while True:
        answer = method(text)

        # Check that the input contains the asked constrains
        valid = True
        for i in constrains:
            if not i in answer:
                valid = False

        if valid:
            return answer
        else:
            print("Invalid", name)