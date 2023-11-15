import discord
from discord.ext import commands
import util.JsonHandler
from time import sleep
import requests
import shutil
import os
import datetime

errorMessages = []
issues = []
disabledMods = []
enabledMods = []

# not sure if this is needed anymore
# it isnt currently used, but id rather not get rid of it until rewrite is done
def decodetext(text, text_to_filter, text_to_filter2):
    filtered_bytes = text.replace(b'\x82', b'')
    decoded_string = filtered_bytes.decode('utf-8')
    split_v2 = str(decoded_string)
    lines_split = split_v2.splitlines()
    new_text = ""
    for i in lines_split:
        if text_to_filter in i or text_to_filter2 in i:
            new_text = new_text + i + "\n"
    return new_text

# Functions used for trying to solve actual error messages
def check_errorMessages( file ):
    with open(file, "r") as fileread:
        lines = fileread.readlines()
        print("Errors:\n") 
        for line in lines:
            if "[error]" in line:
                errorMessages.append(line.split("[error]")[1].lstrip())

        for error in errorMessages:
            print(error)


# This checks the errors we put in the list earlier for ones that I manually add
# Note: clean this up when I don't have a life again
# additionally, add checks for if mods are disabled. this way, instead of "disable or install", i can recommend exactly disable OR install
global hudRevamp
global ckcallback
def check_errors():
    print("Error matches:\n")
    hudRevamp = False
    ckcallback = False
    for error in errorMessages:
        if "COMPILE ERROR expected \",\", found identifier \"inputParams\"" in error or "COMPILE ERROR expected \",\", found identifier \"Streakperams\"" in error:
            for mod in enabledMods:
                if "HUD Revamp" in mod:
                    hudRevamp = True
                if "ClientKillCallback" in mod:
                    ckcallback = True
            
            # this is very gross
            # also needs an update
            # basically this needs to check:
            # do they have ckcb (Client Kill CallBack)?
            # if they do, do they have hud revamp?
            # if they do, do they have hud announcer or ckcb hud revamp patch?
            # if they do have the patch, it isnt an issue
            # if they dont have the patch, respond that they need it due to mod conflicts
            # if they dont have client kill callback, reply that the error is because they need it

            # currently, the patch is not checked for
            if ckcallback == True:
                if hudRevamp == True:
                    hudRevamp = False
                    ckcallback = False
                    return "HudRevampClientKillCallback"
            else:
                return "MissingClientKillCallback"
        
                
        if "COMPILE ERROR Undefined variable \"Progression_GetPreference\"" in error:
            for mod in enabledMods:
                if "VanillaPlus" in mod:
                    return "VanillaPlusClientInstalled"
                
        if "COMPILE ERROR Undefined variable \"ModSettings_AddDropDown\"" in error:
            # This function is from NegativBild, no reason to do checking for mods
            return "MissingNegativBild"
        
        if "COMPILE ERROR Undefined variable \"ModSettings_AddModTitle\"" in error:
            for mod in disabledMods:
                if "VanillaPlus" in mod:
                    return "VanillaPlusDisabled"
                

# Functions used for getting a list of mods from a log
def check_mods( file ):
    with open(file, "r") as fileread:
        lines = fileread.readlines()

        for line in lines:
            if "loaded successfully" in line.lower():
                if "disabled" in line.lower():
                    # why did i call this fullLine?
                    fullLine = line.split("[info]")[1].strip().replace("'", "")
                    disabledMods.append(fullLine.split("loaded")[0])

                else:
                    fullLine = line.split("[info]")[1].strip().replace("'", "")
                    enabledMods.append(fullLine.split("loaded")[0])

        if len(disabledMods) > 0:
            print("Disabled mods:\n")
            for mod in disabledMods:
                print(mod + "\n")

        if len(enabledMods) > 0:
            print("Enabled mods:\n")
            for mod in enabledMods:
                print(mod + "\n")


# this function checks the files date by reading the first line
# note: this can break if the log is older than the update that adds the date to logs
# maybe check version first, and if it's a valid version then check this?

# this also has no real function currently, and has no actual reply
# this is because i want to get this file uploded to the loggingrewrite branch tonight
def check_filedate( file ):
    with open(file, "r") as fileread:
        lines = fileread.readlines()
        for line in lines:
            logDate = line.split("[")[1].split("]")[0]
            break

    nowDate = datetime.today().strftime('%Y-%m-%d') 

    if logDate < nowDate:
        print("Found an older log")

# This checks if Northstar is in the "log" (which as of now is just any message.txt in the Discord)\
# If it is, rename it for log checking. If it isn't, print a frowny face to console
def check_for_log(file):
    shouldRename = False
    with open(file, "r") as fileread:
        lines = fileread.readlines()

        for line in lines:
            if "Northstar" in line:
                shouldRename = True
            else:
                break

        if shouldRename == True:
            os.rename(file, "Logs/nslogunparsed.txt")
        else:
            print("Spoiler, that wasn't a log :(")

# this function returns the current version of Northstar
# it is currently unused, but will eventually be
# this way, Spectre will tell the user to update

# note: do this in an if statement and not a switch statement
# this should be appended to an embed if another issue also exists
def versionCheck():
    try:
        gh_api_response = requests.get("https://api.github.com/repos/R2Northstar/Northstar/releases/latest")
        if gh_api_response.status_code == 200:
                gh_data = gh_api_response.json()
        else:
            print(f"Error code when retrieving GitHub API: {gh_api_response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"GitHub API request failed: {err}")
        return None
    
    ns_current_version = gh_data["name"][1:] # This gets the version as the raw version number without the "v". So '1.7.3' vs 'v1.7.3'
    return ns_current_version

problem = discord.Embed(title="Problems I found in your log:", description="", color=0x5D3FD3)
# a currently unused embed for dming me when a log is sent
dmLog = discord.Embed(title="Somebody sent a log!", description="", color=0x5D3FD3)
# a currently unused embed for telling someone to send a new log
oldLog = discord.Embed(title="It looks like the log you've sent is older! Please send the newest one.", description="Windows puts the newest logs at the bottom of the logs folder due to how they're named.", color=0x5D3FD3) 
        
class LogReading(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        # when a ticket channel is created, have Spectre "type" for a bit, then ask for logs
        if str(channel.name).startswith("ticket"):
            await channel.typing()
            sleep(3)
            await channel.send("I'm a bot automatically replying to the ticket being opened. If you're having an issue with the Northstar client itself, please send a log so that I can try to automatically read it, or a human can read it better. You can do this by going to `Titanfall2/R2Northstar/logs` and sending the furthest down `nslog` file there.\n\nIf I don't automatically respond, please wait for a human to assist. If you're getting an error MESSAGE in game, you could also try typing that out here, or sending a screenshot of the error, as I automatically reply to some of those as well.")

    @commands.Cog.listener()
    async def on_message(self, message):

        allowed_channels = util.JsonHandler.load_channels()
        if message.author.bot:
            return
        
        else:    
            if str(message.channel.id) in allowed_channels or str(message.channel.name).startswith("ticket"):
                if message.attachments:
                    filename = message.attachments[0].filename  
                    shouldRespond = False
                    if 'nslog' in filename and filename.endswith('.txt'):     
                        if os.path.exists("Logs") == False:
                            os.mkdir("Logs")
                            
                        await message.attachments[0].save("Logs/nslogunparsed.txt")

                    # sometimes people copy paste the log into Discord which results in the log being called `message.txt` on Discord
                    # check_for_log checks that Northstar is in the file, and checks it at as a log if it is
                    if 'message' in filename and filename.endswith('.txt'):
                        if os.path.exists("Logs") == False:
                            os.mkdir("Logs")

                        await message.attachments[0].save("Logs/nslogcheckvalid.txt")
                        check_for_log("Logs/nslogcheckvalid.txt")

                    if os.path.exists("Logs"):

                        enabledMods.clear()
                        disabledMods.clear()
                        errorMessages.clear()

                        check_mods("Logs/nslogunparsed.txt")
                        
                        check_errorMessages("Logs/nslogunparsed.txt")

                        # ngl this is a little gross
                        match check_errors():
                            case "HudRevampClientKillCallback":
                                shouldRespond = True
                                problem.add_field(name="HUD Revamp Client Kill Callback conflict", value="HUD Revamp and Client Kill Callback currently conflict.\n\nYou can fix this temporarily by installing the [ClientKillCallback HUDRevamp Compatability patch](https://northstar.thunderstore.io/package/Capt_Diqhedd/ClientKillCallback_HUDRevamp_Compatibility_Patch/), or by disabling/uninstalling HUD Revamp")
                                print("Found a HUD Revamp Client Kill Callback conflict!")

                            case "VanillaPlusAndClientInstalled":
                                shouldRespond = True
                                problem.add_field(name="Northstar.Client installed on VanillaPlus", value="I noticed that you have Northstar.Client installed while using VanillaPlus! As of 2.0, this is no longer required.\n\nYou should follow the [instructions from the mod page](https://northstar.thunderstore.io/package/NanohmProtogen/VanillaPlus/) for steps on how to install VanillaPlus properly")
                                print("Found Northstar.Client installed with VanillaPlus!")

                            case "VanillaPlusDisabled":
                                shouldRespond = True
                                problem.add_field(name="VanillaPlus disabled", value="I noticed that you had an issue with VanillaPlus, but that it is disabled.\n\nDeleting `enablemods.json` from `Titanfall2/R2Titanfall` (assuming you followed one of the install guides) will forcibly enable ALL mods, which will fix the issue with VanillaPlus loading, but might re-introduce errors you solved if you disabled other mods")
                                print("Found disabled VanillaPlus error")

                            case "RemoveLockedMultiplayer":
                                shouldRespond = True
                                problem.add_field(name="Remove Locked Multiplayer", value="Remove Locked Multiplayer relied on a function in Northstar that is no longer present. Please disable/delete the mod")

                            case "MissingNegativBild":
                                shouldRespond = True
                                problem.add_field(name="Missing Dependency: NegativBild", value="It looks like you're having an issue with NegativBild (a dependency for mods like Provoxin RGB) where it isn't loading.\n\nEnable it if it's disabled, otherwise install it from [Thunderstore](https://northstar.thunderstore.io/package/odds/Negativbild/), or from a mod manager")
                                print("Found a missing dependency: NegativBild!")

                            case "MissingClientKillCallback":
                                shouldRespond = True
                                problem.add_field(name="Missing Dependency: ClientKillCallback", value="It looks like you're having an issue with ClientKillCallback (a dependency for mods like Champions 2023 vandal and KraberPrimrose) where it isn't loading.\n\nEnable it if it's disabled, otherwise install it from [Thunderstore](https://northstar.thunderstore.io/package/S2Mods/ClientKillCallback/), or from a mod manager")
                                print("Found a missing dependency: ClientKillCallback")

                            case _:
                                print("I couldn't find any matching errors!")
                                shouldRespond = False

                        if shouldRespond == True: 
                            await message.channel.typing()
                            sleep(5)
                            await message.channel.send(embed=problem, reference=message)
                            problem.clear_fields()
                    
                        shutil.rmtree("Logs")
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LogReading(bot))