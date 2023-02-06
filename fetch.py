from base64 import b64decode
import sys, requests

def fetch(method, endpoint, auth):

    try:
        data = getattr(requests, method)('https://mittkak.nu/v1/' + endpoint, headers={"Authorization": "Basic %s" % auth}).text
    except:
        print(f"An unexpected error ocurred while trying to fetch '${endpoint}'.")
        data = {}

    return data