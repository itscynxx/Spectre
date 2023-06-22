import discord
import util.JsonHandler
from discord.ext import commands


class UserReplies(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    # Slash command to disable replies for the user
    @commands.hybrid_command(name='disablereplies', description='Disables replies for the user who uses the command')
    async def disablereplies(self, ctx):
        data = util.JsonHandler.load_users()

        if str(ctx.author.id) in data:
            await ctx.send("You already have automatic replies disabled!", ephemeral=True)
            
        else:    
            data[str(ctx.author.id)] = f"{interaction.user.display_name}"

            util.JsonHandler.save_users(data)
            await ctx.send("Successfully disabled me automatically replying to your messages!", ephemeral=True)

    # Slash command to enable replies fore the user
    @commands.hybrid_command(name='enablereplies', description='Enables replies for the user who uses the command')
    async def enablereplies(self, ctx):
        data = util.JsonHandler.load_users()

        if str(ctx.author.id) in data:
            del data[str(ctx.author.id)]
            
            util.JsonHandler.save_users(data)
            await ctx.send("Successfully enabled me automatically replying to your messages!", ephemeral=True)
        else:
            await ctx.send("You already have automatic replies enabled!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserReplies(bot))
