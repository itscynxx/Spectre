import discord
import os
from discord.ext import commands

replies = True

# Embed for automatically replying to potential questions about installing Northstar
installing = discord.Embed(description="I noticed that you may have asked for help installing Northstar. Please read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430) for ways to install Northstar.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)

class InstallingNorthstar(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if replies == True:

            # Very professional way to show that the bot won't reply to itself :D
            if message.author.id == 1108490165254619198:
                print(f"Stopped my stupid ass from making an infinite message loop :3")
                return
            
            elif any(x in message.content.lower() for x in ["installing northstar", "install northstar", "get northstar", "download northstar", "downloading northstar"]):
                await message.channel.send(reference=message, embed=installing)
                print(f"Installing Northstar embed reply sent")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InstallingNorthstar(bot))