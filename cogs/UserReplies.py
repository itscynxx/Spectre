import discord
import os
import util.JsonHandler
from discord.ext import commands

log_data = {}

class UserReplies(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    # Slash command to disable replies to one user
    @commands.hybrid_command(name='disablereplies', description='Disables replies for the user who uses the command')
    async def disablereplies(self, ctx):
        data = util.JsonHandler.load_users()
        log_data[str(ctx.author.id)] = {}
        log_data[str(ctx.author.id)] = False
        util.JsonHandler.save_users(log_data)
        await ctx.send("Successfully disabled me automatically replying to your messages!", ephemeral=True)

    # Slash command to enable replies to one user
    @commands.hybrid_command(name='enablereplies', description='Enables replies for the user who uses the command')
    async def enablereplies(self, ctx):
        data = util.JsonHandler.load_users()

        for key in data:
            if str(ctx.author.id) in data:
                del data[str(ctx.author.id)]
                await ctx.send("Successfully enabled me automatically replying to your messages!", ephemeral=True)
                break
        
        util.JsonHandler.save_users(data)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserReplies(bot))