import discord
import os
from discord.ext import commands

replies = True

class UserReplies(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    # Slash command to disable replies to one user
    @commands.hybrid_command(name='disablereplies', description='Disables replies for the user who uses the command')
    async def disablereplies(self, ctx):
        with open('noreplyusers.json', 'r') as f:
            data = json.load(f)
            log_data[str(ctx.author.id)] = {}
            log_data[str(ctx.author.id)] = False
            save_users(log_data)
            await ctx.send("Successfully disabled me automatically replying to your messages!", ephemeral=True)
    
        with open("noreplyusers.json", "w") as f:
            data = json.load(f)
            json.dump(data, f)
        
    # Slash command to enable replies to one user
    @commands.hybrid_command(name='enablereplies', description='Enables replies for the user who uses the command')
    async def enablereplies(self, ctx):
        with open('noreplyusers.json', 'r') as f:
            data = json.load(f)
            for key in data:
                if str(ctx.author.id) in data:
                    del data[str(ctx.author.id)]
                    await ctx.send("Successfully enabled me automatically replying to your messages!", ephemeral=True)
                    break
            
        with open("noreplyusers.json", "w") as f:
            data = json.load(f)
            json.dump(data, f)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserReplies(bot))