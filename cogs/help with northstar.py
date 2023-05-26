import discord
import os
from discord.ext import commands

replies = True

# Embed for automatically replying to potential questions about help for Northstar
help = discord.Embed(description="I noticed that you may have asked for help. Please open a ticket in the [help channel](https://discordapp.com/channels/920776187884732556/922663326994018366/1101924175343517827).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)

class NorthstarHelp(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NorthstarHelp(bot))