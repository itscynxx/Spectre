import discord
import os
from discord.ext import commands

replies = True

# Embeds about global enabling/denying automatic replies for the bot
replieson = discord.Embed(title="Automatic bot replies set to ***ON***", color=0x287e29)
repliesoff = discord.Embed(title="Automatic bot replies set to ***OFF***", color=0xDC143C)

# Embeds about the reply status of the bot
replystatusenabled = discord.Embed(title="Automatic bot replies are currently enabled", color=0x6495ED)
replystatusdisabled = discord.Embed(title="Automatic bot replies are currently disabled", color=0x6495ED)


def replycheck():
    return replies

class GlobalReplies(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
    
    # Stops replies across all servers
    @commands.hybrid_command(description="Globally disables Spectre replying to messages")
    async def stop(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            global replies
            replies = False
            await ctx.send(embed=repliesoff)
            print(f"Automatic bot replies are disabled")
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)

    # Starts replies across all servers
    @commands.hybrid_command(description="Globally enables Spectre replying to messages")
    async def start(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            global replies
            replies = True
            await ctx.send(embed=replieson)
            print(f"Automatic bot replies are enabled")
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)

    # Displays the current status of replies across all servers
    @commands.hybrid_command(description="Displays if bot replies are on or off")
    async def replystatus(self, ctx):
        if replies == True:
            await ctx.send(embed=replystatusenabled)
        elif replies == False:
            await ctx.send(embed=replystatusdisabled)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GlobalReplies(bot))

    