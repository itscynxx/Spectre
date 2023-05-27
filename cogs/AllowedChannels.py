import discord
import os
import util.JsonHandler
from discord.ext import commands

log_data = {}

class AllowedChannels(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Enables automatic replies for the current channel. Owner only.")
    async def allowchannel(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            data = util.JsonHandler.load_channels()
            log_data[str(ctx.channel.id)] = []
            log_data[str(ctx.channel.id)] = True
            util.JsonHandler.save_channels(log_data)
            await ctx.send("Successfully enabled automatic replies in this channel!", ephemeral=True)

    @commands.hybrid_command(description="Disables automatic replies for the current channel. Owner only.")
    async def blockchannel(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            data = util.JsonHandler.load_channels()

            for key in data:
                if str(ctx.channel.id) in data:
                    del data[str(ctx.channel.id)]
                    await ctx.send("Successfully disabled automatic replies in this channel!", ephemeral=True)
                    break
        
            util.JsonHandler.save_channels(data)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AllowedChannels(bot))