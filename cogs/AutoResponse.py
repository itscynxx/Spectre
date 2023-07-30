import datetime
import discord
from discord.ext import commands
import util.JsonHandler
from cogs.GlobalReplies import replycheck
import re


# Embed for automatically replying to potential questions about installing Northstar
installing = discord.Embed(description="I noticed that you may have asked for help installing Northstar. Please read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430) for ways to install Northstar.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for automatically replying to potential questions about help for Northstar
help = discord.Embed(description="I noticed that you may have asked for help. Please open a ticket in the [help channel](https://discordapp.com/channels/920776187884732556/922663326994018366/1101924175343517827).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for automatically replying to potential questions about a controller not working
controller = discord.Embed(description="I noticed you may have asked for help regarding a controller not working.", color=0x5D3FD3)
controller.add_field(name="\u200b", value="Try following the [controller not working](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#controller) wiki section for multiple ways you can fix a controller not working on Northstar.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs")

# Embed for automatically replying to potential questions about installing mods for Northstar
installmods = discord.Embed(description="I noticed that you may have asked for help installing mods. You can do this automatically or manually.", color=0x5D3FD3)
installmods.add_field(name="Automatic mod installation", value="Simply use a mod manager and navigate to the mods browser to automatically find and install mods.")
installmods.add_field(name="Manual mod installation", value="See the image sent below for help installing mods manually. If it's hard to read, click into it, and hit `Open in browser`, then follow the image guide.")
installmods.add_field(name="\u200b", value="If I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", inline=False)

# Embed for automatically replying to mentions of "Couldn't find player account"
playeraccount = discord.Embed(description="I noticed that you may have asked for help regarding the \"Couldn't find player account\" error. Please read the [wiki section for this issue](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#playeraccount) to solve the error.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for automatically replying to mentions of "What is Northstar?"
northstarInfo = discord.Embed(title="I noticed you may have asked a question about what Northstar is.", description="Northstar is a mod loader for Titanfall 2 with a focus on community server hosting and support for modding to replace models, sounds, textures, or even add new gamemodes. To install, you can check and read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs")

# Embed for automatically replying to potential mentions of "Authentication Failed", meant to be enabled when the Master Server Northstar is run on is down
msdownembed = discord.Embed(title="I noticed you may have mentioned the error \"Authentication Failed\".", description="Currently, the master server Northstar's server browser operates on is down. This means that currently you can't connect and aren't alone in having the error. Please wait for the master server to come back up and continue to check [the annoucements channel](https://discord.com/channels/920776187884732556/920780605132800080) for more updates.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for letting users know the fastify error response doesn't matter if they aren't hosting a server
fastifyError = discord.Embed(title='I noticed you may have mentioned the "NO GAMESERVER RESPONSE"/"got fastify error response" error message while asking for help.', description="This error only applies if you are trying to host a server, in which case your ports likely aren't forwarded properly. If you aren't trying to host a server, your actual error is something else happening. Please look for other mentions of issues, or send a log.", color=0x5D3FD3)
fastifyError.add_field(name="\u200b", value="If I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", inline=False)

# Embed for default EA stuff
ea = discord.Embed(title="I noticed you may have asked for help regarding the \"Couldn't write log file!\" error.", description="If you have the game installed on EA, please follow the [wiki section](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#cannot-write-log-file-when-using-northstar-on-ea-app) for solving this issue.", color=0x5D3FD3)
ea.add_field(name="\u200b", value="If I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", inline=False)

config = util.JsonHandler.load_json("config.json")

msdown = False

def EnabledCheck():
    return msdown
        
class AutoResponse(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        self.last_time = datetime.datetime.utcfromtimestamp(0)
        self.last_channel = 0


    @commands.hybrid_command(description="Enables the message for the master server being down. Allowed users only.")
    async def togglemsdownreply(self, ctx):
        allowed_users = util.JsonHandler.load_allowed_users()

        if str(ctx.author.id) in allowed_users:
            global msdown
            
            if msdown == False:
                msdown = True
                await ctx.send("Enabled the message for cases where master server is down!")
                
            elif msdown == True:
                msdown = False
                await ctx.send("Disabled the message for cases where the master server is down!")
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)
            
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
        
        regex_embed_map = {
            "player.*account": playeraccount,
            "Failed creating log file": ea,
            "controller not working": controller,
            "can.i.use.controller.*northstar": controller,
            "authentication.*failed": msdownembed,
            "cant.*join": msdownembed,
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
                
                if str(message.channel.id) in enabledchannels:
                        # Should stop all bot messages
                        if message.author.bot:
                            return
                            
                        elif self.bot.user.mentioned_in(message):
                            image_match = next((key for key in text_image_map if re.search(key, message.content.lower())))
                            
                            if image_match:
                                await message.channel.send(text_image_map[image_match])
                                print(f"Sent a {image_match}")
                            else:
                                print("No matching keyword was found")
                                
                        elif re.search("how|help", message.content.lower()) and re.search("install.northstar", message.content.lower()):
                            await message.channel.send(reference=message, embed=installing)
                            print(f"Installing Northstar embed reply sent")
        
                        elif re.search("help|how", message.content.lower()) and re.search("titanfall|northstar", message.content.lower()) and re.search("install.*mods", message.content.lower()):
                            await message.channel.send(reference=message, embed=installmods)
                            await message.channel.send("https://cdn.discordapp.com/attachments/942391932137668618/1069362595192127578/instruction_bruh.png")
                            print(f"Northstar mods installing embed reply sent")
                            
                        else:
                            message_match = next((key for key in regex_embed_map if re.search(key, message.content.lower())))
                            if EnabledCheck() == True and message_match:
                                await message.channel.send(reference=message, embed=regex_embed_map[message_match])
                            else:
                                return
                                
                            
                            
                self.last_time = datetime.datetime.utcnow()
            self.last_channel = message.channel.id

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoResponse(bot))
