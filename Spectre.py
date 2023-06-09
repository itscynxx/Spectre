import discord
import os
import util.JsonHandler
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


COGS = ("cogs.AutoResponse", "cogs.GlobalReplies", "cogs.UserReplies", "cogs.InstallChannelEmbed", "cogs.AllowedChannels")
INTENTS = discord.Intents.default()
INTENTS.message_content = True

config = util.JsonHandler.load_json("config.json")

# Config docs
# {
#     "admin": <admin id>,
#     "cooldowntime": <cooldown seconds>, 
#     "noreplylist": <name of list.json>,
#     "neverreplylist": <name of neverreplylist.json>
#     "allowedchannels": <name of list.json>
# }

bot = commands.Bot(
    intents=INTENTS,
    command_prefix=config["prefix"],
    owner_id=config["admin"]
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

# Slash command to reload cogs
@bot.hybrid_command(name='reload', description='Owner only')
async def reload(ctx):
    if ctx.author.id == bot.owner_id:
        for cog in COGS:
            await bot.reload_extension(cog)
        print('Reloaded cogs successfully!')
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Disable a user's automatic replies if they're being naughty :D
@bot.hybrid_command(description="Disables reply toggling for selected user. Owner only.")
@app_commands.describe(user = "The user to disable reply toggling for")
async def disablereplytoggle(ctx, user: discord.Member):
    if ctx.author.id == bot.owner_id:
        data = util.JsonHandler.load_neverusers()
        data[str(user.id)] = "off"
        # This isn't very efficient but it works (I think)!
        util.JsonHandler.save_neverusers(data)
        await ctx.send(f"Successfully disabled reply toggling for {user}", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Enables giving users control over automatic responses for them again
@bot.hybrid_command(description="Enables reply toggling for selected user. Owner only.")
@app_commands.describe(user = "The user to enable reply toggling for")
async def enablereplytoggle(ctx, user: discord.Member):
    if ctx.author.id == bot.owner_id:
        data = util.JsonHandler.load_neverusers() 

        if str(user.id) in data:
            del data[str(user.id)]

        util.JsonHandler.save_neverusers(data) 
        await ctx.send(f"Successfully enabled reply toggling for {user}", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

load_dotenv()
util.JsonHandler.init_json()
bot.run(os.getenv("TOKEN"))
