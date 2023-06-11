import json
import os



def init_json():
    # Automatically create files for user data 

        
    if os.path.isfile(noreplylist) == False:

        new_json(noreplylist)
    if os.path.isfile(allowedchannels) == False:
        new_json(allowedchannels)
    if os.path.isfile(neverreplylist) == False:
        new_json(neverreplylist)
    
    # Automatically create files for ticket data

    if os.path.isdir(openticketlist) == False:
        new_json(openticketlist)
    if os.path.isdir(openticketusers) == False:
        new_json(openticketusers)

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
    
# Functions for saving users toggling their replies to JSON
def save_users(data):
    save_json(noreplylist, data)

def load_users():
    return load_json(noreplylist)

# Functions for saving me toggling user abilities to toggle replies to JSON
def save_neverusers(data):
    save_json(neverreplylist, data)

def load_neverusers():
    return load_json(neverreplylist)

# Functions for saving allowed channels to JSON
def save_channels(data):
    save_json(allowedchannels, data)

def load_channels():
    return load_json(allowedchannels)

# Functions for saving currently opened tickets
def save_ticket(data):
    save_json(openticketlist, data)

def load_ticket():
    return load_json(openticketlist)

def save_ticketuser(data):
    save_json(openticketusers, data)

def load_ticketuser():
    return load_json(openticketusers)

config = load_json("config.json")

# Config loading for user data
usersdata = config["usersdata"]
noreplylist = config["noreplylist"]
neverreplylist = config["neverreplylist"]
allowedchannels = config["allowedchannels"]

# Config loading for tickets data
ticketsdata = config["ticketsdata"]
openticketlist = config["openticketlist"]
openticketusers = config["openticketusers"]