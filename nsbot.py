import discord
from discord import app_commands
from discord.ext import commands
import json

EXTENSIONS = ("extensions.test")
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    intents=INTENTS,
    command_prefix=""
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

def load_users():
    with open("noreplyusers.json", 'r') as f:
        users = json.load(f)
    return users
    
def save_users(users):
    with open('noreplyusers.json', 'w') as f:
        json.dump(users, f, indent=4)
        
log_data = {}


client = aclient()

tree = discord.app_commands.CommandTree(client)

replies = True

class SimpleView(discord.ui.View):
    
    @discord.ui.button(label="Disable automatic bot replies", style=discord.ButtonStyle.red)
    async def disable(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('noreplyusers.json', 'r') as f:
            data = json.load(f)
            log_data[str(interaction.user.id)] = {}
            log_data[str(interaction.user.id)] = 1
            save_users(log_data)
            await interaction.response.send_message("Successfully disabled automatic replies!", ephemeral=True)
        
        with open("noreplyusers.json", "w") as f:
            json.dump(data, f)
            
    @discord.ui.button(label="Enable automatic bot replies", style=discord.ButtonStyle.success)
    async def enable(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('noreplyusers.json', 'r') as f:
            data = json.load(f)
            for key in data:
                if str(interaction.user.id) in data:
                    del data[str(interaction.user.id)]
                    await interaction.response.send_message("Successfully enabled automatic replies!", ephemeral=True)
                    break
            
        with open("noreplyusers.json", "w") as f:
            json.dump(data, f)

# Embed for automatically replying to potential questions about help for Northstar
help = discord.Embed(description="I noticed that you may have asked for help. Please open a ticket in the [help channel](https://discordapp.com/channels/920776187884732556/922663326994018366/1101924175343517827).\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)

# Embed for automatically replying to potential questions about installing mods for Northstar
installmods = discord.Embed(description="I noticed that you may have asked for help installing mods. You can do this automatically or manually.", color=0x5D3FD3)
installmods.add_field(name="Automatic mod installation", value="Simply use a mod manager and navigate to the mods browser to automatically find and install mods.")
installmods.add_field(name="Manual mod installation", value="When downloading a `.zip` folder for a mod from Thunderstore, you first want to unzip/extract it. Then, go into the extracted folder, go into the `mods` folder, and there will be a folder with a name similar to the mod. Move that folder to `Titanfall2\R2Northstar\mods` and your mod will be installed.\n\nIf I'm being accidentally triggered or annoying, please ping @cooldudepugs#4318")

# Embed for automatically replying to potential questions about installing Northstar
installing = discord.Embed(description="I noticed that you may have asked for help installing Northstar. Please read the [installation channel](https://discordapp.com/channels/920776187884732556/922662496588943430) for ways to install Northstar.\n\nIf I'm being accidentally triggered or annoying, please disable replies with the button below or ping @cooldudepugs#4318", color=0x5D3FD3)

# Embeds for the installation channel - Help mention
helpembed = discord.Embed(title="Having issues with Northstar?", color=0xfff9ac)
helpembed.add_field(name="Troubleshooting issues with Northstar or installing Northstar", value="Check out the [FAQ](https://r2northstar.gitbook.io/r2northstar-wiki/faq) and [troubleshooting](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting) pages of the wiki for your error\n\nIf you can\'t find your error, feel free to open a ticket in the [help channel](https://discordapp.com/channels/920776187884732556/922663326994018366/1101924175343517827) by reading the embedded message and clicking the button to open a ticket")

# Embeds for the installation channel - Manual
manual = discord.Embed(title="Manual Installation", description="Note: Does not automatically update. You will have to do this every time Northstar has an update, and install mods and mod dependencies yourself\n", color=0xff6969)
manual.add_field(name="\u200b", value="Download the newest `.zip` from the [releases page](https://github.com/R2Northstar/Northstar/releases/latest)\n\nFollow the [Manual installation guide](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/manual-installation)")

# Embeds for the installation channel - Automatic
installation = discord.Embed(title="Automatic Installation for Northstar (recommended)", description="Automatic updates and mod installation are also parts of mod managers", color=0x69ff69)
installation.add_field(name="FlightCore", value="Simple, easy to use mod manager and Northstar installer.\n Works on Windows and Linux, and is actively updated. Most stable mod manager.\n\n [Download (Windows)](https://r2northstartools.github.io/FlightCore/index.html?win-setup)\n\n [Guide to setting up FlightCore](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/northstar-installers/flightcore-guide)", inline=True)
installation.add_field(name="VTOL", value="Advanced, feature rich mod manager and Northstar installer.\n Works on Windows, and is actively updated.\n\n [Download (Windows)](https://github.com/BigSpice/VTOL/releases/latest/download/VTOL_Installer.msi)\n\n [Guide to setting up VTOL](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/northstar-installers/vtol-guide)", inline=True)
installation.add_field(name="Viper", value="Simple, easy to use mod manager and Northstar installer.\n Works on Windows and Linux, and recieves bug fix updates.\n\n [Download (Windows)](https://0negal.github.io/viper/index.html?win-setup)\n\n [Guide to setting up Viper](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/northstar-installers/viper-guide)", inline=True)

# Embeds about the reply status of the bot
replieson = discord.Embed(title="Automatic bot replies set to ***ON***", color=0x287e29)
repliesoff = discord.Embed(title="Automatic bot replies set to ***OFF***", color=0xDC143C)
replystatusenabled = discord.Embed(title="Automatic bot replies are currently enabled", color=0x6495ED)
replystatusdisabled = discord.Embed(title="Automatic bot replies are currently disabled", color=0x6495ED)


# Stops replies across all servers
@bot.hybrid_command(name="stop", description="Globally disables Spectre replying to messages")
async def stop(ctx):
    if ctx.author.id == 502519988423229460:
        global replies
        replies = False
        await ctx.send(embed=repliesoff)
        print(f"Automatic bot replies are disabled")
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Starts replies across all servers
@bot.hybrid_command(name="start", description="Globally enables Spectre replying to messages")
async def start(ctx):
    if ctx.author.id == 502519988423229460:
        global replies
        replies = True
        await ctx.send(embed=replieson)
        print(f"Automatic bot replies are enabled")
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Displays the current status of replies across all servers
@bot.hybrid_command(name="replystatus", description="Displays if bot replies are on or off")
async def replystatus(ctx):
    if replies == True:
        await ctx.send(embed=replystatusenabled)
    elif replies == False:
        await ctx.send(embed=replystatusdisabled)

# Slash command to send the embeds for the installation channel
@bot.hybrid_command(name="installation", description="Installation information for Northstar")
async def installation(ctx):       
    if ctx.author.id == 502519988423229460:

        await ctx.send(embed=helpembed)
        await ctx.send(embed=manual)
        await ctx.send(embed=installation)

# Slash command to update commands
@bot.hybrid_command(name='sync', description='Owner only')
async def sync():
    if ctx.author.id == 502519988423229460:
        await tree.sync()
        print('Command tree synced.')
        await ctx.sened('Commands synced successfully!')
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Slash command to disable replies to one user
@bot.hybrid_commands(name='disablereplies', description='Disables replies for the user who uses the command')
async def disablereplies(ctx):
    log_data[str(ctx.author.id)] = {}
    log_data[str(ctx.author.id)] = False
    save_users(log_data)
    await ctx.send("Successfully disabled me automatically replying to your messages!", ephemeral=True)
    
    with open("noreplyusers.json", "w") as f:
        json.dump(data, f)
        
# Slash command to enable replies to one user
@bot.hybrid_command(name='enablereplies', description='Enables replies for the user who uses the command')
async def enablereplies(ctx):
    with open('noreplyusers.json', 'r') as f:
        data = json.load(f)
        for key in data:
            if str(ctx.author.id) in data:
                del data[str(ctx.author.id)]
                await ctx.send("Successfully enabled me automatically replying to your messages!", ephemeral=True)
                break
            
    with open("noreplyusers.json", "w") as f:
        json.dump(data, f)
    
# Commands to automatically reply to users if key phrases are said. 
@bot.event
async def on_message(message):
    with open('noreplyusers.json', 'r') as f:
        data = json.load(f)
        
        view = SimpleView()
        
        
        if replies == True:
            if message.author == client.user:
                print(f"Stopped my stupid ass from making an infinite message loop :3")
                return
            
            # Disable automatic replies in Northstar while I continue to write code
            if message.guild.id == 920776187884732556:
                return
        
            if str(message.author.id) in data:
                if str(message.author.id) == False:
                    return

            elif any(x in message.content.lower() for x in ["installing northstar", "install northstar", "get northstar", "download northstar", "downloading northstar"]):
                await message.channel.send(reference=message, embed=installing, view=view)
                print(f"Installing Northstar embed reply sent")

            elif any(x in message.content.lower() for x in ["how do i fix", "help with Northsrtar", "somebody help", "anybody help", "how fix", "how to fix", "vtol error", "viper error", "flightcore error"]):
                    await message.channel.send(reference=message, embed=help, view=view)
                    print(f"Help embed reply sent")

            elif any(x in message.content.lower() for x in ["help installing mods", "help getting mods"]):
                    await message.channel.send(reference=message, embed=installmods, view=view)
                    print(f"Installing mods embed reply sent")

bot.run('no token for you')
