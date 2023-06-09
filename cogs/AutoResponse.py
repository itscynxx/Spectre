import datetime
import discord
from discord.ext import commands
import util.JsonHandler
from cogs.GlobalReplies import replycheck

# Embed for automatically replying to potential questions about installing Northstar
installing = discord.Embed(description="I noticed that you may have asked for help installing Northstar. Please read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430) for ways to install Northstar.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)
# Embed for automatically replying to potential questions about help for Northstar
help = discord.Embed(description="I noticed that you may have asked for help. Please open a ticket in the [help channel](https://discordapp.com/channels/920776187884732556/922663326994018366/1101924175343517827).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)
# Embed for automatically replying to potential questions about installing mods for Northstar
installmods = discord.Embed(description="I noticed that you may have asked for help installing mods. You can do this automatically or manually.", color=0x5D3FD3)
installmods.add_field(name="Automatic mod installation", value="Simply use a mod manager and navigate to the mods browser to automatically find and install mods.")
installmods.add_field(name="Manual mod installation", value="See the image sent below for help installing mods manually. If it's hard to read, click into it, and hit `Open in browser`, then follow the image guide.")
installmods.add_field(name="\u200b", value="If I'm being accidentally triggered or annoying, please ping @cooldudepugs#4318", inline=False)
# Embed for automatically replying to mentions of "Couldn't find player account"
playeraccount = discord.Embed(description="I noticed that you may have asked for help regarding the \"Couldn't find player account\" error. Please read the [wiki section for this issue](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#player-not-found-invalid-master-server-token) to solve the error. \n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)

responses = {  
    "install":       ["installing northstar", "install northstar", "get northstar", "download northstar", "downloading northstar"],
    "help":          ["how do i fix", "help with Northsrtar", "somebody help", "anybody help", "how fix", "how to fix", "vtol error", "viper error", "flightcore error"],
    "installmods":   ["help installing mods", "help getting mods"],
    "playeraccount": ["couldnt find player account", "couldn't find player account", "player account not found"]
}

config = util.JsonHandler.load_json("config.json")

class SimpleView(discord.ui.View):
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

        
class AutoResponse(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        self.last_time = datetime.datetime.utcfromtimestamp(0)
        self.last_channel = 0
    
    @commands.Cog.listener()
    async def on_message(self, message):
        view = SimpleView()
        users = util.JsonHandler.load_users()
        neverusers = util.JsonHandler.load_neverusers()
        channel = util.JsonHandler.load_channels()
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
                
                if str(message.channel.id) in channel:
                        # Should stop all bot messages
                        if message.author.bot:
                            # print(f"Stopped my stupid ass from making an infinite message loop :3")
                            return
                
                        elif any(x in message.content.lower() for x in responses["install"]):
                            await message.channel.send(reference=message, embed=installing, view=view)
                            print(f"Installing Northstar embed reply sent")

                        elif any(x in message.content.lower() for x in responses["help"]):
                            await message.channel.send(reference=message, embed=help, view=view)
                            print(f"Northstar Help embed reply sent")
                    
                        elif any(x in message.content.lower() for x in responses["installmods"]):
                            await message.channel.send(reference=message, embed=installmods, view=view)
                            await message.channel.send("https://cdn.discordapp.com/attachments/942391932137668618/1069362595192127578/instruction_bruh.png")
                            print(f"Northstar mods embed reply sent")
                            
                        elif any(x in message.content.lower() for x in responses["playeraccount"]):
                            await message.channel.send(reference=message, embed=playeraccount, view=view)
                            print(f"Couldn\'t find player account embed reply sent")
                            
                self.last_time = datetime.datetime.utcnow()
            self.last_channel = message.channel.id

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoResponse(bot))
