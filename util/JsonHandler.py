import json
import os



def init_json():
    if os.path.isfile(noreplylist) == False:
        new_json(noreplylist)
    if os.path.isfile(allowedchannels) == False:
        new_json(allowedchannels)

def new_json(name):
    fp = open(name, "w")
    fp.write("{}")
    fp.close()

def save_json(file,data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data
    
def save_users(data):
    save_json(noreplylist, data)

def load_users():
    return load_json(noreplylist)

def save_channels(data):
    save_json(allowedchannels, data)

def load_channels():
    return load_json(allowedchannels)


config = load_json("config.json")
noreplylist = config["noreplylist"]
allowedchannels = config["allowedchannels"]
