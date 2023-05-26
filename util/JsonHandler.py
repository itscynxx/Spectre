import json
import os

noreplylist = "noreplyusers.json"

def init_json():
    if os.path.isfile(noreplylist) == False:
        new_json(noreplylist)

def new_json(name):
    fp = open(name, "w")
    fp.write("{}")
    fp.close()

def load_users():
    with open("noreplyusers.json", 'r') as f:
        users = json.load(f)
    return users
    
def save_users(data):
    with open('noreplyusers.json', 'w') as f:
        json.dump(data, f, indent=4)
    