from util.JsonHandler import *


roles = load_json("roles.json")

def isModerator(ctx):
    if(ctx.guild == None): return False
    for roleID in roles['Moderator']:
        # check if any of the roles the user has is Moderator
        if(any(map(lambda x : x.id == int(roleID), ctx.author.roles)) == True):
            return True
    return False