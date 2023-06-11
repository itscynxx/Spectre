import discord
from discord import utils
from discord.ext import commands
import util.JsonHandler

ticket = discord.Embed(title="**Please go to the [Northstar Wiki FAQ](https://r2northstar.gitbook.io/r2northstar-wiki/faq) and use `Ctrl + F` to search for the error you're experiencing before opening a ticket", description=", as most common errors can be found there without needing to wait for a response for someone.")
ticket.add_field(name="Everyone involved in helping does it entirely for fun or out of passion, with no monetary gain, so please don't expect an immediate response.\n", value="Clicking the buttons below this message will open a ticket.\n(Public = People volunteering can see your ticket)\n(Staff-only = Only Northstar staff can see your ticket)")

INTENTS = discord.Intents.default()
INTENTS.message_content = True

config = util.JsonHandler.load_json("config.json")

bot = commands.Bot(
    intents=INTENTS,
    command_prefix=config["prefix"],
    owner_id=config["admin"]
)

class TicketButtons(discord.ui.View):    

    @discord.ui.button(label="Open a public ticket!", style=discord.ButtonStyle.success)
    async def openTicket(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = util.JsonHandler.load_ticketuser()
        ticket = utils.get(interaction.guild.text_channels, name= f"ticket-{interaction.user.display_name}")
        if str(interaction.user.id) in data:
            await interaction.response.send_message(f"You already have a ticket open! Check your ticket!", ephemeral=True)

        else: 
            
            category = discord.utils.get(interaction.guild.categories, id=1111762231454072964)        
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
            ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.display_name}", category=category, overwrites=overwrites, reason = f"Ticket for {interaction.user}")
            data[str(interaction.user.id)] = "Open"
            util.JsonHandler.save_ticketuser(data)
            await interaction.response.send_message(f"I've opened a ticket for you at {ticket_channel.mention}!", ephemeral=True)
    
    @discord.ui.button(label="Open a staff-only ticket!", style=discord.ButtonStyle.red)
    async def openStaffTicket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_ticket = discord.utils.get(interaction.guild.text_channels, name= f"ticket-{interaction.user.display_name}")
        category = discord.utils.get(interaction.guild.categories, id=1111762231454072964)        
        overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }
        staff_ticket_channel = await interaction.guild.create_text_channel(name=f"staff-ticket-{interaction.user.display_name}", category=category, overwrites=overwrites)

        if ticket is not None: 
            print(f"mfw")
            await interaction.response.send_message(f"You already have a ticket open! Check {staff_ticket_channel.mention}!", ephemeral=True)
        else: 
            await interaction.response.send_message(f"I've opened a ticket for you at {staff_ticket_channel.mention}!", ephemeral=True)
    
class CloseRequestButtons(discord.ui.View):

    @discord.ui.button(label="Close", style=discord.ButtonStyle.success)
    async def CloseRequestButtonClose(self, interaction: discord.Interaction, button: discord.ui.button):
        data = util.JsonHandler.load_ticketuser
        data2 = util.JsonHandler.load_ticket
        if str(interaction.channel.id) in data:
            if str(interaction.user.id) in data:
                await interaction.channel.delete()

    @discord.ui.button(label="Deny close request", style=discord.ButtonStyle.red)
    async def CloseRequestButtonKeepOpen(self, interaction: discord.Interaction, button: discord.ui.button):
        data = util.JsonHandler.load_ticketuser
        if str(interaction.user.id) in data:
            await interaction.response.send_message(f"{interaction.user.display_name} has denied the close request!")



class TicketEmbed(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(description="Command for testing tickets")
    async def ticket(self, ctx):
        view = TicketButtons()
        await ctx.send(embed=ticket, view=view)
    
    @commands.hybrid_command(description="Request to close the current ticket!")
    async def closerequest(self, ctx):
        requestcloseembed = discord.Embed(title=f"This ticket has been requested to be closed by {ctx.author.display_name}", description="Would you like to accept?")
        view = CloseRequestButtons()

        await ctx.send(embed=requestcloseembed, view=view)

    @commands.hybrid_command(description="Closes the current ticket")
    async def close(self, ctx):

        transcript_channel = self.bot.get_channel(1100869266921771061) 
        await transcript_channel.send(f"Closed #{ctx.channel.name}")       
        await ctx.channel.delete() 

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicketEmbed(bot))