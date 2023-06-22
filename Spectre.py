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
#     "allowedusers": <name of alloweduserslist.json>
# }

bot = commands.Bot(
    intents=INTENTS,
    command_prefix=config["prefix"],
    owner_id=config["admin"]
)

bot.remove_command("help")

@bot.event
async def setup_hook() -> None:
    for cog in COGS:
        await bot.load_extension(cog)

client = aclient()

# Slash command to update commands
@bot.hybrid_command(name='sync', description='Syncs the bot\'s commands. Allowed users only.')
async def sync(ctx):
    allowed_users = util.JsonHandler.load_allowed_users()

    if str(ctx.author.id) in allowed_users or ctx.author.id == bot.owner_id:
        await bot.tree.sync()
        print('Commands synced successfully!')
        await ctx.send('Commands synced successfully!')
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)



# Slash command to reload cogs
@bot.hybrid_command(name='reload', description='Reloads the bot\'s cogs. Allowed users only.')
async def reload(ctx):
    allowed_users = util.JsonHandler.load_allowed_users()

    if str(ctx.author.id) in allowed_users:
        for cog in COGS:
            await bot.reload_extension(cog)
        print('Reloaded cogs successfully!')
        await ctx.send("Reloaded cogs succesfully!", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)



# Disable a user's automatic replies if they're being naughty :D
@bot.hybrid_command(description="Disables reply toggling for selected user. Allowed users only.")
@app_commands.describe(user = "The user to disable reply toggling for")
async def disablereplytoggle(ctx, user: discord.Member):
    allowed_users = util.JsonHandler.load_allowed_users()

    if str(ctx.author.id) in allowed_users:
        data = util.JsonHandler.load_neverusers()
        data[str(user.id)] = "off"
        # This isn't very efficient but it works (I think)!
        util.JsonHandler.save_neverusers(data)
        await ctx.send(f"Successfully disabled reply toggling for {user.name}!", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Enables giving users control over automatic responses for them again
@bot.hybrid_command(description="Enables reply toggling for selected user. Allowed users only.")
@app_commands.describe(user = "The user to enable reply toggling for")
async def enablereplytoggle(ctx, user: discord.Member):
    allowed_users = util.JsonHandler.load_allowed_users()

    if str(ctx.author.id) in allowed_users:
        data = util.JsonHandler.load_neverusers() 

        if str(user.id) in data:
            del data[str(user.id)]

        util.JsonHandler.save_neverusers(data) 
        await ctx.send(f"Successfully enabled reply toggling for {user.name}!", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)



# Set the status for the bot
@bot.hybrid_command(description="Set the status of the bot. Allowed users only.")
async def setstatus(ctx, status: str):
    allowed_users = util.JsonHandler.load_allowed_users()

    if str(ctx.author.id) in allowed_users:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
        await ctx.send(f"Set bot status to `Listening to {status}`!", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)



@bot.hybrid_command(description="Add a user to the allowed users list. Owner only")
async def enablerusercommands(ctx, user: discord.Member):
    if ctx.author.id == bot.owner_id:
        allowed_users = util.JsonHandler.load_allowed_users()

        allowed_users[str(user.id)] = ""
        util.JsonHandler.save_allowed_users(allowed_users)
        await ctx.send(f"Successfully allowed {user.name} to use bot commands!", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

@bot.hybrid_command(description="Removes a user from the allowed users list. Owner only.")
@app_commands.describe(user = "The user to enable reply toggling for")
async def disableusercommands(ctx, user: discord.Member):
    if ctx.author.id == bot.owner_id:
        allowed_users = util.JsonHandler.load_allowed_users()

        if str(user.id) in allowed_users:
            del allowed_users[str(user.id)]

        util.JsonHandler.save_allowed_users(allowed_users) 
        await ctx.send(f"Successfully removed {user.name}'s ability to use bot commands!", ephemeral=True)
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

@bot.hybrid_command(description="Lists the current users with permission to use higher level bot commands. Allowed users only.")
async def permissionlist(ctx):
    allowed_users = util.JsonHandler.load_allowed_users()
    
    if str(ctx.author.id) in allowed_users:
        
        listEmbed = discord.Embed(title="Allowed users", description="These users have access to (most) of Spectre's commands!", color=0xA020F0)
        listEmbed.add_field(name="", value="\u200b")
        
        for user_id, value in allowed_users.items():
            user = await bot.fetch_user(int(user_id))
            listEmbed.add_field(name="", value=f"{user.name}", inline=False)
        
        await ctx.send(embed=listEmbed, ephemeral=True)
    
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)



@bot.hybrid_command(description="Display information for using the bot")
async def help(ctx):
    helpembed = discord.Embed(title="Spectre", description="Spectre is a bot created by Cyn (aka cooldudepugs) with major help from H0L0. Its purpose is to redirect users to get help easier when sending messages in public channels trying to get help. The list below is of commands for the bot that all users have access to.", color=0x6495ED)
    helpembed.add_field(name="disablereplies", value="Disables the bot replying to the person who used the command", inline=False)
    helpembed.add_field(name="enablereplies", value="Enables the bot replying to the person who uesd the command", inline=False)
    helpembed.add_field(name="replystatus", value="Sends an embed about if the bot has automatic replies on at all. Also shows if the user has their replies or ability to control their replies disabled.\n\nYou can view a full list of the commands on the [GitHub repo's wiki](https://github.com/CooldudePUGS/Spectre/wiki)", inline=False)
    await ctx.send(embed=helpembed)


load_dotenv()
util.JsonHandler.init_json()
bot.run(os.getenv("TOKEN"))
