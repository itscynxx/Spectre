import datetime
import discord
from discord.ext import commands
import util.JsonHandler
from cogs.GlobalReplies import replycheck


# Embed for automatically replying to potential questions about installing Northstar
installing = discord.Embed(description="I noticed that you may have asked for help installing Northstar. Please read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430) for ways to install Northstar.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for automatically replying to potential questions about help for Northstar
help = discord.Embed(description="I noticed that you may have asked for help. Please open a ticket in the [help channel](https://discordapp.com/channels/920776187884732556/922663326994018366/1101924175343517827).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for automatically replying to potential questions about installing mods for Northstar
installmods = discord.Embed(description="I noticed that you may have asked for help installing mods. You can do this automatically or manually.", color=0x5D3FD3)
installmods.add_field(name="Automatic mod installation", value="Simply use a mod manager and navigate to the mods browser to automatically find and install mods.")
installmods.add_field(name="Manual mod installation", value="See the image sent below for help installing mods manually. If it's hard to read, click into it, and hit `Open in browser`, then follow the image guide.")
installmods.add_field(name="\u200b", value="If I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", inline=False)

# Embed for automatically replying to mentions of "Couldn't find player account"
playeraccount = discord.Embed(description="I noticed that you may have asked for help regarding the \"Couldn't find player account\" error. Please read the [wiki section for this issue](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#player-not-found-invalid-master-server-token) to solve the error. \n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

# Embed for automatically replying to mentions of "What is Northstar?"
northstarInfo = discord.Embed(title="I noticed you may have asked a question about what Northstar is.", description="Northstar is a mod loader for Titanfall 2 with a focus on community server hosting and support for modding to replace models, sounds, textures, or even add new gamemodes. To install, you can check and read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs")

# Embed for automatically replying to potential questions of script compilation errors- either temporary entirely or temporary version for the ModSettings merge into Northstar 1.15.0
compError = discord.Embed(title="I noticed you may have asked for help regarding \"Script Compilation Error\" issues.", description="This error generally means that something has gone wrong with one of your mods and either\n1. You\'re missing a dependency for a mod you\'ve installed (note: if you're using a mod manager, that should auto install them for you) or\n2. A mod you have is conflicting with another mod you have installed.", color=0x5D3FD3)
compError.add_field(name="Recently, ModSettings has been merged into Northstar. This means it\'s a part of normal Northstar, and having the mod version of it from now on will cause issues.", value="This will probably cause a lot of this specific issue for the next little while, so make sure to remove it if you haven\'t already\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#")

# Embed for automatically replying to potential mentions of "Authentication Failed", meant to be enabled when the Master Server Northstar is run on is down
msdownembed = discord.Embed(title="I noticed you may have mentioned the error \"Authentication Failed\".", description="Currently, the master server Northstar's server browser operates on is down. This means that currently you can't connect and aren't alone in having the error. Please wait for the master server to come back up and continue to check [the annoucements channel](https://discord.com/channels/920776187884732556/920780605132800080) for more updates.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs", color=0x5D3FD3)

responses = {  
    "install":         ["installing northstar", "install northstar", "get northstar", "download northstar", "downloading northstar"],
    "help":            ["how do i fix", "help with Northsrtar", "somebody help", "anybody help", "how fix", "how to fix", "vtol error", "viper error", "flightcore error"],
    "installmods":     ["help installing mods", "help getting mods"],
    "playeraccount":   ["couldnt find player account", "couldn't find player account", "player account not found"],
    "whatisNorthstar": ["what is northstar", "what's northstar"],
    "ScriptCompError": ["script compilation error", "compilation error", "compile error"],
    "msdown":          ["authentication failed", "cant join", "can't join"]
}

config = util.JsonHandler.load_json("config.json")

class ToggleRepliesButton(discord.ui.View):
    @discord.ui.button(label="Toggle automatic bot replies", style=discord.ButtonStyle.success)
    async def disable(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = util.JsonHandler.load_users()

        if str(interaction.user.id) in data:
            for key in data:
                del data[str(interaction.user.id)]
                await interaction.response.send_message("Successfully enabled automatic replies!", ephemeral=True)
                break
        else:
            data[str(interaction.user.id)] = "off"
            await interaction.response.send_message("Successfully disabled automatic replies!", ephemeral=True)

        util.JsonHandler.save_users(data)

msdown = False

def EnabledCheck():
    return msdown
        
class AutoResponse(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        self.last_time = datetime.datetime.utcfromtimestamp(0)
        self.last_channel = 0


    @commands.hybrid_command(description="Display what phrases trigger Spectre's auto reply. Allowed users only.")
    async def autoreplytriggers(self, ctx):
        allowed_users = util.JsonHandler.load_allowed_users()

        triggers = discord.Embed(title="Phrases that trigger Spectre's auto reply:")
        triggers.add_field(name="Installation help", value='"installing northstar", "install northstar", "get northstar", "download northstar", "downloading northstar"\n', inline=False)
        triggers.add_field(name="", value="\u200b", inline=False)
        triggers.add_field(name="General help", value='"how do i fix", "help with Northsrtar", "somebody help", "anybody help", "how fix", "how to fix", "vtol error", "viper error", "flightcore error"\n', inline=False)
        triggers.add_field(name="", value="\u200b", inline=False)
        triggers.add_field(name="Mod installing help", value='"help installing mods", "help getting mods"\n', inline=False)
        triggers.add_field(name="", value="\u200b", inline=False)
        triggers.add_field(name="Player account not found help", value='"couldnt find player account", "couldn\'t find player account", "player account not found"\n', inline=False)
        triggers.add_field(name="", value="\u200b", inline=False)
        triggers.add_field(name="What is Northstar messages", value='"what is northstar", "what\'s northstar"\n', inline=False)
        triggers.add_field(name="", value="\u200b", inline=False)
        triggers.add_field(name="Script compilation errors (Note: This is mostly likely temporary, or at the very least will change soon especially as the Mod Settings mention will most likely only stay for a week or two)", value='"script compilation error", "compilation error", "compile error"\n', inline=False)
        triggers.add_field(name="", value="\u200b", inline=False)
        triggers.add_field(name="Master server down messages (Note: This auto reply must be enabled by using `/enablemsdownmessage` and should only be enabled when MS is actually down!)", value='"authentication failed", "cant join"\n', inline=False)

        if str(ctx.author.id) in allowed_users:
            await ctx.send(embed=triggers, ephemeral=True)
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)
            
    @commands.hybrid_command(description="Enables the message for the master server being down. Allowed users only.")
    async def msdownmessageon(self, ctx):
        allowed_users = util.JsonHandler.load_allowed_users()

        if str(ctx.author.id) in allowed_users:
            global msdown
            msdown = True
            await ctx.send("Enabled the message for cases where master server is down!")
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)
            
    @commands.hybrid_command(description="Disables the message for the master server being down. Allowed users only.")
    async def msdownmessageoff(self, ctx):
        allowed_users = util.JsonHandler.load_allowed_users()

        if str(ctx.author.id) in allowed_users:
            global msdown
            msdown = False
            await ctx.send("Disabled the message for cases where the master server is down!")
        else:
            await ctx.send("You don't have permission to use this command", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        view = SimpleView()
        users = util.JsonHandler.load_users()
        neverusers = util.JsonHandler.load_neverusers()
        enabledchannels = util.JsonHandler.load_channels()
        time_diff = (datetime.datetime.utcnow() - self.last_time).total_seconds()


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
                
                        elif any(x in message.content.lower() for x in responses["whatisNorthstar"]):
                            await message.channel.send(reference=message, embed=northstarInfo, view=view)
                            print(f"Northstar info embed reply sent")

                        elif any(x in message.content.lower() for x in responses["msdown"]):
                            if EnabledCheck() == True:
                                await message.channel.send(reference=message, embed=msdownembed, view=view)
                            else:
                                return

                        elif any(x in message.content.lower() for x in responses["install"]):
                            await message.channel.send(reference=message, embed=installing, view=view)
                            print(f"Installing Northstar embed reply sent")

                        elif any(x in message.content.lower() for x in responses["ScriptCompError"]):
                            await message.channel.send(reference=message, embed=compError, view=view)
                            print(f"Comp Error embed reply sent")

                        elif any(x in message.content.lower() for x in responses["help"]):
                            await message.channel.send(reference=message, embed=help, view=view)
                            print(f"Northstar help embed reply sent")
                    
                        elif any(x in message.content.lower() for x in responses["installmods"]):
                            await message.channel.send(reference=message, embed=installmods, view=view)
                            await message.channel.send("https://cdn.discordapp.com/attachments/942391932137668618/1069362595192127578/instruction_bruh.png")
                            print(f"Northstar mods installing embed reply sent")
                            
                        elif any(x in message.content.lower() for x in responses["playeraccount"]):
                            await message.channel.send(reference=message, embed=playeraccount, view=view)
                            print(f"Couldn\'t find player account embed reply sent")
                            
                self.last_time = datetime.datetime.utcnow()
            self.last_channel = message.channel.id

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoResponse(bot))
