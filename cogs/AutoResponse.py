import datetime
import discord
from discord.ext import commands
import util.JsonHandler, util.MasterStatus
from cogs.GlobalReplies import replycheck
import re
import asyncio

responseEmbed = discord.Embed(title="Automatic bot response", description="", color=0x5D3FD3)

# Embed for automatically replying to potential questions about installing mods for Northstar
installmods = discord.Embed(description="I noticed that you may have asked for help installing mods. You can do this automatically or manually.", color=0x5D3FD3)
installmods.add_field(name="Automatic mod installation", value="Simply use a mod manager and navigate to the mods browser to automatically find and install mods.")
installmods.add_field(name="Manual mod installation", value="See the image sent below for help installing mods manually. If it's hard to read, click into it, and hit `Open in browser`, then follow the image guide.")

# Embed for automatically replying to potential mentions of "Authentication Failed", meant to be enabled when the Master Server Northstar is run on is down
msdownembed = discord.Embed(title="I noticed you may have mentioned the error \"Authentication Failed\".", description="Currently, the master server Northstar's server browser operates on is down. This means that currently you can't connect and aren't alone in having the error. Please wait for the master server to come back up and continue to check [the annoucements channel](https://discord.com/channels/920776187884732556/920780605132800080) for more updates.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

config = util.JsonHandler.load_json("config.json")
        
class AutoResponse(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        self.last_time = datetime.datetime.utcfromtimestamp(0)
        self.last_channel = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        users = util.JsonHandler.load_users()
        neverusers = util.JsonHandler.load_neverusers()
        enabledchannels = util.JsonHandler.load_channels()
        time_diff = (datetime.datetime.utcnow() - self.last_time).total_seconds()
        
        text_image_map = {
            "bike": "https://cdn.discordapp.com/attachments/924051841631805461/1128540732358131753/image.png",
            "plane": "https://media.discordapp.net/attachments/924051841631805461/1130649908593049640/plen.png",
            "car": "https://media.discordapp.net/attachments/924051841631805461/1130649908869861397/spec.png",
            "walk": "https://media.discordapp.net/attachments/924051841631805461/1130649909159264316/walk.png",
            "unicycle": "https://media.discordapp.net/attachments/942505193893945394/1130916070455259247/image.png",
            "titan": "https://media.discordapp.net/attachments/942505193893945394/1130915423802630166/image.png",
            "tank": "https://media.discordapp.net/attachments/942505193893945394/1130926682321191012/IMG_1307.png"
        }
        
        


        if not (time_diff > config["cooldowntime"] or message.channel.id != self.last_channel):
            self.last_channel = message.channel.id            
            print(f"Tried to send message while on cooldown! Didn't send message!")
            return
        else:
            if replycheck() == True:
                if str(message.author.id) in users:
                        return
                    
                if str(message.author.id) in neverusers:
                        return
                
                if str(message.channel.id) in enabledchannels or str(message.channel.name).startswith("ticket"):
                        # Should stop all bot messages
                        if message.author.bot:
                            return
                            
                        elif self.bot.user.mentioned_in(message):
                            image_match = next((key for key in text_image_map if re.search(key, message.content.lower())))
                            
                            if image_match:
                                await message.channel.send(text_image_map[image_match], reference=message)
                                print(f"Sent a {image_match}")
                            else:
                                print("No matching keyword was found")     

                        elif re.search("player.*account", message.content.lower()):
                            responseEmbed.add_field(name="Couldn't find player account error", value="Please read the [wiki section for this issue](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#playeraccount) to solve the error.")

                        elif re.search("Failed.creating.log.file", message.content.lower()):
                            responseEmbed.add_field(name="Default EA path issues", value="If you have the game installed on EA, please follow the [wiki section](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#cannot-write-log-file-when-using-northstar-on-ea-app) for solving this issue.")

                        elif re.search("controller.not.working", message.content.lower()) or re.search("can.i.use.controller.*northstar", message.content.lower()):
                            responseEmbed.add_field(name="Controller not working", value="Try following the [controller not working](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#controller) wiki section for multiple ways you can fix a controller not working on Northstar.")
                            
                        elif re.search("authentication.*failed", message.content.lower()) or re.search("cant.*join", message.content.lower()):
                            if util.MasterStatus.IsMasterDown() == True:
                                await message.channel.send(reference=message, embed=msdownembed)
                            else:
                                return

                        elif re.search("how|help", message.content.lower()) and re.search("install.northstar", message.content.lower()):
                            if re.search("uninstall", message.content.lower()):
                                responseEmbed.add_field(name="Uninstalling Northstar", value="Note that if you're wanting to play vanilla, you can simply launch the vanilla game on Steam (remove the `-northstar` launch arg if you added it).\n\nIf you still want to delete Northstar however, deleting `NorthstarLauncher.exe`, `Northstar.dll`, and the `R2Northstar` folder from the `titanfall2` directory should be enough.\n\nIf you want to clear absolutely everything, you can also delete `r2ds.bat` and `LEGAL.txt` from the `titanfall2` directory, and delete the `bin` folder in the `titanfall2 directory`, then verify the game's files to restore the vanilla files found in the bin folder.")
                            else:
                                responseEmbed.add_field(name="Installing Northstar", value="Please read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430) for ways to install Northstar.")
                    
                        # note: rewrite this later
                        elif re.search("help|how", message.content.lower()) and re.search("titanfall|northstar", message.content.lower()) and re.search("install.*mods", message.content.lower()):
                            await message.channel.send(reference=message, embed=installmods)
                            await message.channel.send("https://cdn.discordapp.com/attachments/942391932137668618/1069362595192127578/instruction_bruh.png")
                            print(f"Northstar mods installing embed reply sent")

                        if len(responseEmbed.fields) > 0:
                            await message.channel.typing()
                            await asyncio.sleep(3)
                            await message.channel.send(reference=message, embed=responseEmbed)
                            responseEmbed.clear_fields()

                if message.channel.id == 937922165163065384:

                        # Note: this is actually really gross. discord's api doesn't like when you try to add multiple emojis at once (say, from a list)
                        # and will instead place them in the incorrect order regardless of sleep time or order you place them in the list :P

                        await message.add_reaction("🔴")
                        await asyncio.sleep(1)

                        await message.add_reaction("🟠")
                        await asyncio.sleep(1)

                        await message.add_reaction("🟢")
                        await asyncio.sleep(1)
                            
                self.last_time = datetime.datetime.utcnow()
            self.last_channel = message.channel.id

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoResponse(bot))
