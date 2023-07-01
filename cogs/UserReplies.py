import discord
import util.JsonHandler
from discord.ext import commands


class UserReplies(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot

    # Slash command to disable replies for the user
    @commands.hybrid_command(description='Toggles replies for the user who uses the command')
    async def togglereplies(self, ctx):
        data = util.JsonHandler.load_users()

        if str(ctx.author.id) in data:
            del data[str(ctx.author.id)]
            await ctx.send("Succesfully enabled me automatically replying to your messages!", ephemeral=True)
            
        else:    
            data[str(ctx.author.id)] = f"{ctx.author.display_name}"
            await ctx.send("Successfully disabled me automatically replying to your messages!", ephemeral=True)
            
        util.JsonHandler.save_users(data)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserReplies(bot))
