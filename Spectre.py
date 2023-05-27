import discord
import os
import util.JsonHandler
from discord.ext import commands
from dotenv import load_dotenv


COGS = ("cogs.AutoResponse", "cogs.GlobalReplies", "cogs.UserReplies", "cogs.InstallChannelEmbed", "cogs.AllowedChannels")
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    intents=INTENTS,
    command_prefix="$",
    owner_id=502519988423229460
)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await bot.tree.sync
            self.synced = True
        # Very professional way to show that the bot is online :D
        print('{self.user} is a bitch ass motherfucker. Oh, and shit\'s working.')

@bot.event
async def setup_hook() -> None:
    for cog in COGS:
        await bot.load_extension(cog)

client = aclient()

# Slash command to update commands
@bot.hybrid_command(name='sync', description='Owner only')
async def sync(ctx):
    if ctx.author.id == bot.owner_id:
        await bot.tree.sync()
        print('Commands synced successfully!')
        await ctx.send('Commands synced successfully!')
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

@bot.hybrid_command(name='reload', description='Owner only')
async def reload(ctx):
    if ctx.author.id == bot.owner_id:
        for cog in COGS:
            await bot.reload_extension(cog)
        print('Reloaded cogs successfully!')
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

load_dotenv()
util.JsonHandler.init_json()
bot.run(os.getenv("TOKEN"))
