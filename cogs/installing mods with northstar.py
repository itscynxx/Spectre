import discord
import os
from discord.ext import commands

replies = True

# Embed for automatically replying to potential questions about installing mods for Northstar
installmods = discord.Embed(description="I noticed that you may have asked for help installing mods. You can do this automatically or manually.", color=0x5D3FD3)
installmods.add_field(name="Automatic mod installation", value="Simply use a mod manager and navigate to the mods browser to automatically find and install mods.")
installmods.add_field(name="Manual mod installation", value="When downloading a `.zip` folder for a mod from Thunderstore, you first want to unzip/extract it. Then, go into the extracted folder, go into the `mods` folder, and there will be a folder with a name similar to the mod. Move that folder to `Titanfall2\R2Northstar\mods` and your mod will be installed.\n\nIf I'm being accidentally triggered or annoying, please ping @cooldudepugs#4318")

class ModInstallation(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModInstallation(bot))