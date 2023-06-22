import discord
import util.JsonHandler
from discord.ext import commands


replies = True

# Embeds about global enabling/denying automatic replies for the bot
replieson = discord.Embed(title="Automatic bot replies set to ***ON***", color=0x287e29)
repliesoff = discord.Embed(title="Automatic bot replies set to ***OFF***", color=0xDC143C)

# Embeds about the reply status of the bot
replystatusenabled = discord.Embed(title="Automatic bot replies are currently enabled", color=0x6495ED)
replystatusdisabled = discord.Embed(title="Automatic bot replies are currently disabled", color=0xDC143C)

# Embeds for showing if users have their replies off or I've removed their ability to toggle replies while showing the global status of replies
replystatusenabledUserTogglesDisabled = discord.Embed(title="Automatic bot replies are currently enabled", description="_But_ the user of this command has their ability to control their automatic replies disabled", color=0x6495ED)
replystatusenabledUserRepliesDisabled = discord.Embed(title="Automatic bot replies are currently enabled", description="_But_ the user of this command has automatic replies disabled", color=0x6495ED)


def replycheck():
    return replies

class GlobalReplies(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
    
    # Disables replies across all servers
    @commands.hybrid_command(description="Globally disables Spectre replying to messages. Allowed users only.")
    async def globaldisable(self, ctx):
        allowed_users = util.JsonHandler.load_allowed_users()

        if str(ctx.author.id) in allowed_users:
            global replies
            replies = False
            await ctx.send(embed=repliesoff)
            print(f"Automatic bot replies are disabled")
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)

    # Enables replies across all servers
    @commands.hybrid_command(description="Globally enables Spectre replying to messages. Allowed users only.")
    async def globalenable(self, ctx):
        allowed_users = util.JsonHandler.load_allowed_users()

        if str(ctx.author.id) in allowed_users:
            global replies
            replies = True
            await ctx.send(embed=replieson)
            print(f"Automatic bot replies are enabled")
        else:
            await ctx.send("You don't have permission to use this command!", ephemeral=True)

    # Displays the current status of replies across all servers
    @commands.hybrid_command(description="Displays if bot replies are on or off")
    async def replystatus(self, ctx):
        users = util.JsonHandler.load_users()
        neverusers = util.JsonHandler.load_neverusers()

        if replies == True:
            if str(ctx.author.id) in neverusers:
                await ctx.send(embed=replystatusenabledUserTogglesDisabled)
            elif str(ctx.author.id) in users:
                await ctx.send(embed=replystatusenabledUserRepliesDisabled)
            else:
                await ctx.send(embed=replystatusenabled)
        elif replies == False:
            await ctx.send(embed=replystatusdisabled)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GlobalReplies(bot))
