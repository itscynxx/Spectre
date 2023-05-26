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
installmods.add_field(name="Manual mod installation", value="When downloading a `.zip` folder for a mod from Thunderstore, you first want to unzip/extract it. Then, go into the extracted folder, go into the `mods` folder, and there will be a folder with a name similar to the mod. Move that folder to `Titanfall2\R2Northstar\mods` and your mod will be installed.\n\nIf I'm being accidentally triggered or annoying, please ping @cooldudepugs#4318")

responses = {  
    "install":     ["installing northstar", "install northstar", "get northstar", "download northstar", "downloading northstar"],
    "help":        ["how do i fix", "help with Northsrtar", "somebody help", "anybody help", "how fix", "how to fix", "vtol error", "viper error", "flightcore error"],
    "installmods": ["help installing mods", "help getting mods"]
}
log_data = {}


class SimpleView(discord.ui.View):
    @discord.ui.button(label="Disable automatic bot replies", style=discord.ButtonStyle.red)
    async def disable(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_data[str(interaction.user.id)] = {}
        log_data[str(interaction.user.id)] = 1
        util.JsonHandler.save_users(log_data)
        await interaction.response.send_message("Successfully disabled automatic replies!", ephemeral=True)
        util.JsonHandler.save_users(log_data)
            
    @discord.ui.button(label="Enable automatic bot replies", style=discord.ButtonStyle.success)
    async def enable(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = util.JsonHandler.load_users()
        for key in data:
            if str(interaction.user.id) in data:
                del data[str(interaction.user.id)]
                await interaction.response.send_message("Successfully enabled automatic replies!", ephemeral=True)
                break
        util.JsonHandler.save_users(data)


class AutoResponse(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        view = SimpleView()
        data = util.JsonHandler.load_users()

        if replycheck() == True:
            if str(message.author.id) in data:
                if str(message.author.id) == False:
                    return
            # Should stop all bot messages
            if message.author.bot:
                print(f"Stopped my stupid ass from making an infinite message loop :3")
                return
            
            elif any(x in message.content.lower() for x in responses["install"]):
                await message.channel.send(reference=message, embed=installing, view=view)
                print(f"Installing Northstar embed reply sent")

            elif any(x in message.content.lower() for x in responses["help"]):
                await message.channel.send(reference=message, embed=help, view=view)
                print(f"Northstar Help embed reply sent")
            
            elif any(x in message.content.lower() for x in responses["installmods"]):
                await message.channel.send(reference=message, embed=installmods, view=view)
                print(f"Northstar mods embed reply sent")
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoResponse(bot))