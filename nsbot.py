import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

EXTENSIONS = ("cogs.installing northstar", "cogs.installation channel", "cogs.global replies", "cogs.user replies", "cogs.help with northstar", "cogs.installing mods with northstar",)
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    intents=INTENTS,
    command_prefix="$"
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
    for extension in EXTENSIONS:
        await bot.load_extension(extension)

def load_users():
    with open("noreplyusers.json", 'r') as f:
        users = json.load(f)
    return users
    
def save_users(users):
    with open('noreplyusers.json', 'w') as f:
        json.dump(users, f, indent=4)
        
log_data = {}

client = aclient()


global replies
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

# Slash command to update commands
@bot.hybrid_command(name='sync', description='Owner only')
async def sync(ctx):
    if ctx.author.id == 502519988423229460:
        await bot.tree.sync()
        print('Commands synced successfully!')
        await ctx.send('Commands synced successfully!')
    else:
        await ctx.send("You don't have permission to use this command!", ephemeral=True)

# Commands to automatically reply to users if key phrases are said. 
# This code is doodoo fucking garbage I pray to god H0L0 can fix it
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

            elif any(x in message.content.lower() for x in ["how do i fix", "help with Northsrtar", "somebody help", "anybody help", "how fix", "how to fix", "vtol error", "viper error", "flightcore error"]):
                    await message.channel.send(reference=message, embed=help, view=view)
                    print(f"Help embed reply sent")

            elif any(x in message.content.lower() for x in ["help installing mods", "help getting mods"]):
                    await message.channel.send(reference=message, embed=installmods, view=view)
                    print(f"Installing mods embed reply sent")
load_dotenv()
bot.run(os.getenv("TOKEN"))
