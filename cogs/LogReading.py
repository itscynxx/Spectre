import discord
from discord.ext import commands
import util.JsonHandler
from time import sleep
import requests
import os

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
   
audioList = []
modSplitList = []

problem = discord.Embed(title="Problems I found in your log:", description="", color=0x5D3FD3)
dmLog = discord.Embed(title="Somebody sent a log!", description="", color=0x5D3FD3)
oldLog = discord.Embed(title="It looks like the log you've sent is older! Please send the newest one.", description="Windows puts the newest logs at the bottom of the logs folder due to how they're named.", color=0x5D3FD3) 

class LogReading(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

            
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if str(channel.name).startswith("ticket"):
            await channel.typing()
            sleep(3)
            await channel.send("I'm a bot automatically replying to the ticket being opened. If you're having an issue with the Northstar client itself, please send a log so that I can try to automatically read it, or a human can read it better. You can do this by going to `Titanfall2/R2Northstar/logs` and sending the newset `nslog` you have. Make sure not to send an `nsdmp`, and that you send the newest one! The newest ones are near the bottom by default on windows.\n\nIf I don't automatically respond, please wait for a human to assist. If you're getting an error MESSAGE in game, you could also try typing that out here, as I automatically reply to some of those as well.")

    @commands.Cog.listener()
    async def on_message(self, message):

        global hud
        global callback
        global compileErrorClientKillCallback
        global problemFound
        global audioProblem
        global rgbError
        global frameworkError
        global modsInstalled 
        global betterServerBrowser
        global oldVersion
        hud = False
        callback = False
        compileErrorClientKillCallback = False
        problemFound = False
        audioProblem = False
        rgbError = False
        frameworkError = False
        modsInstalled = False
        betterServerBrowser = False
        oldVersion = False


        allowed_channels = util.JsonHandler.load_channels()
        if message.author.bot:
            return
        

        else:
            
            if str(message.channel.id) in allowed_channels or str(message.channel.name).startswith("ticket"):
                if message.attachments:
                    filename = message.attachments[0].filename  
                    if 'nslog' in filename and filename.endswith('.txt'): 
                        await message.attachments[0].save("Logs/nslogunparsed.txt")
                        print("Found a log!")
                        with open(r"Logs/nslogunparsed.txt", "r") as file:
                            lines = file.readlines()
                            
                   
                            for line in lines:
                                if "NorthstarLauncher version:" in line:
                                    
                                    verSplit = line.split("version:")[1]
                                    if verSplit.strip() == "0.0.0.1+dev":
                                        return
                                    elif verSplit.strip() < versionCheck():
                                        dmLog.add_field(name="", value=f"Version: {verSplit.strip()}", inline=False)
                                        problemFound = True
                                        oldVersion = True

                                # Check mods
                                if "Loading mod" in line:

                                    # Check if HUD Revamp is installed: conflicts with Client Kill callback
                                    if "HUD Revamp" in line:
                                        dmLog.add_field(name="", value="HUD Revamp: True", inline=False)
                                        print("I found HUD Revamp!")
                                        hud = True

                                    # Check if Client Kill callback is installed: conflicts with HUD Revamp
                                    if "ClientKillCallback" in line:
                                        dmLog.add_field(name="", value="Client Kill Callback: True", inline=False)
                                        print("I found Client Kill Callback!")
                                        callback = True

                                    # Check if the OLD, merged better server browser is loading. It's broken now and causes issues
                                    if "Better.Serverbrowser" in line:
                                        dmLog.add_field(name="", value="Better.Serverbrowser: True", inline=False)
                                        print("I found better server browser!")
                                        problemFound = True
                                        betterServerBrowser = True
                                
                                # Check for a compile error for missing Client Kill callback as a dependency, or when there's a conflict with it
                                if "COMPILE ERROR expected \",\", found identifier \"inputParams\"" in line:
                                    dmLog.add_field(name="", value="Client kill callback compile error: True", inline=False)
                                    print("I found a compile error!")
                                    problemFound = True
                                    compileErrorClientKillCallback = True

                                if "COMPILE ERROR Undefined variable \"ModSettings_AddDropdown\"" in line:
                                    dmLog.add_field(name="", value="Missing negativbild: True", inline=False)
                                    print("I found a person missing negativbild!")
                                    problemFound = True
                                    rgbError = True
                                
                                if "COMPILE ERROR Undefined variable \"NS_InternalLoadFile\"" in line:
                                    dmLog.add_field(name="", value="Titan Framework issue: True", inline=False)
                                    print("I found a titan framework issue >:(")
                                    problemFound = True
                                    frameworkError = True

                                # Check for audio replacements being loaded
                                # If 2 seperate mods replacing the same audio are enabled at the same time the game fucking kills itself
                                if "Finished async read of audio sample" in line:
                                    
                                    # Split the string after "R2Northstar/mods" to keep the folder name onwards
                                    a = line.split("R2Northstar/mods")[1]
                                    # Split the previous split at "audio" to cleanly format as "FolderName, audioname" 
                                    # side note: why the fuck don't we use the mod name at all literally anywhere even when registering the audio fully
                                    b = a.split("audio")
                                    # Further clean up the last split
                                    c = [item.split('\\')[1] for item in b]
                                    
                                    # Add these to the audio list for checking for errors
                                    audioList.append(c)

                        # Properly set up the list for actual checking
                        d = list(set(tuple(audio) for audio in audioList))

                        # Set up a list for checking duplicates
                        audio_duplicates_list = {}

                        for item in d:
                            # Grab the audio replacement string (e.g. "player_killed_indicator") and add it to a list to check directly for conflicts
                            audio_duplicate = item[1]

                            # If the audio override already in the list, add the mod name to the list
                            if audio_duplicate in audio_duplicates_list:
                                audio_duplicates_list[audio_duplicate].append(item[0])
                            else:
                                audio_duplicates_list[audio_duplicate] = [item[0]]                        

                        for audio_duplicate, names in audio_duplicates_list.items():
                            if len(names) > 1:
                                problemFound = True
                                print(f"Found duplicates of {audio_duplicate}: {', '.join(names)}")

                        if problemFound == True:
                            print("Found problems in the log! Replying...")   
                            await message.channel.typing()
                            sleep(5)

                            if hud == True and callback == True and compileErrorClientKillCallback == True:
                                problem.add_field(name="", value="I noticed you have both HUD Revamp and Client Kill Callback installed. Currently, these two mods create conflicts. The easiest way to solve this is to delete/disable HUD Revamp.", inline=False)

                            else:
                                
                                if compileErrorClientKillCallback:
                                    problem.add_field(name="Missing dependency!", value="One or more mods you have may require the mod [Client killcallback](https://northstar.thunderstore.io/package/S2Mods/KraberPrimrose/) to work. Please install or update the mod via a mod manager or Thunderstore.", inline=False)

                            if rgbError == True:
                                problem.add_field(name="Missing dependency!",value="One or more mods you have may require the mod [Negativbild](https://northstar.thunderstore.io/package/odds/Negativbild/) to work. Please install or update this mod via a mod manager or Thundersore")
                            
                            if frameworkError == True:
                                problem.add_field(name="Titan Framework", value="Currently, Titan Framework expects a work in progress Northstar feature to function. As such, having it installed will cause issues (temporarily, until the feature is implemented), which uninstalling it will fix. You can temporarily make it work by manually installing the mod by moving the plugins inside the `plugins` folder of the mod into `r2northstar/plugins`, however this is a TEMPORARY fix, and you'll have to undo it when Northstar gets its next update.", inline=False)

                            if betterServerBrowser == True:
                                problem.add_field(name="Better server browser", value="There are two mods called better server browser. The one called \"Better.Serverbrowser\" causes issues when installed, as it was added to Northstar a while ago. Removing it should fix that specific issue.")

                            for audio_duplicate, names in audio_duplicates_list.items():
                                if len(names) > 1:
                                    audioProblem = True
                                    problem.add_field(name="Audio replacement conflict", value=f"The following mods replace the same audio (`{audio_duplicate}`):\n {', '.join(names)}", inline=False)
                                    dmLog.add_field(name="Audio replacement conflict", value=f"The following mods replace the same audio (`{audio_duplicate}`):\n {', '.join(names)}", inline=False)


                            if oldVersion == True:
                                problem.add_field(name="Older Version", value=f"It seems that you're running an older version of Northstar. Updating may not solve your issue, but you should do it anyway. The current version is {versionCheck()}. Please update by using one of the methods in the [installation channel](https://discord.com/channels/920776187884732556/922662496588943430).", inline=False)
                                problem.add_field(name="\u200b", value="If you've already updated and are still seeing this, please check if you have a file called `northstar.dll` in `titanfall2/R2Northstar`. If you do, delete it, and try launching again.", inline=False)

                            
                            if audioProblem == True:
                                problem.add_field(name="Fixing audio replacement conflicts", value="Please remove mods until only one of these audio mods are enabled. These names aren't perfect to what they are for the mod, however they are the file names for the mod, so you can just remove the folder matching the name from `Titanfall2/R2Northstar/mods`.", inline=False)

                            problem.add_field(name="", value="Please note that I am a bot and am still heavily being worked on. There is a chance that some or all of this information is incorrect, in which case I apologize.\nIf you still encounter issues after doing this, please send another log.", inline=False)
                            await message.channel.send(embed=problem, reference=message)     
                            
                            dmme = await self.bot.fetch_user(self.bot.owner_id)
                            dmLog.add_field(name="I found an issue in the log and replied!", value=f"A link to their log can be found here: {message.jump_url}")
                            await dmme.send(embed=dmLog)
                            dmLog.clear_fields()

                            audio_duplicates_list.clear()
                            audioList.clear()
                            problem.clear_fields()
                            hud = False
                            callback = False
                            compileErrorClientKillCallback = False
                            problemFound = False
                            rgbError = False
                            frameworkError = False
                            betterServerBrowser = False
                            oldVersion = False
                            

                        elif problemFound == False:
                            dmme = await self.bot.fetch_user(self.bot.owner_id)
                            dmLog.add_field(name="I didn't find any issues!", value=f"Here's a log you could potentially train from: {message.jump_url}")
                            await dmme.send(embed=dmLog)
                            dmLog.clear_fields()

                            print("I didn't find any problems in the log!")

                        os.remove("Logs/nslogunparsed.txt")
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LogReading(bot))