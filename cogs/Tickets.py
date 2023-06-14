import discord
from discord import utils
from discord.ext import commands
import util.JsonHandler
import os
import datetime
import time

ticketembed = discord.Embed(title="Open a ticket!", description="Please go to the [Northstar Wiki FAQ](https://r2northstar.gitbook.io/r2northstar-wiki/faq) and use `Ctrl + F` to search for the error you're experiencing before opening a ticket as most common errors can be found there without needing to wait for a response for someone.\n", color=0x6495ED)
ticketembed.add_field(name="Everyone involved in helping does it entirely for fun or out of passion, with no monetary gain, so please don't expect an immediate response.\n", value="Clicking the buttons below this message will open a ticket.\n(public = People volunteering can see your ticket)\n(staff-only = Only Northstar staff can see your ticket)")

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
        data = util.JsonHandler.load_ticketusers()
        ticket = utils.get(interaction.guild.text_channels, name= f"ticket-{interaction.user.display_name}")
        
        if str(interaction.user.id) in data:
            await interaction.response.send_message(f"You already have a ticket open! Check {ticket.mention}!", ephemeral=True)

        else: 
            
            category = discord.utils.get(interaction.guild.categories, id=1111762231454072964)        
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
            ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.display_name}", category=category, overwrites=overwrites, reason = f"Ticket for {interaction.user}")
            data[str(interaction.user.id)] = (f"ticket-{interaction.user.display_name}")
            util.JsonHandler.save_ticketusers(data)
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
        def __init__(self, bot :commands.Bot) -> None:
            self.bot = bot

        @discord.ui.button(label="Close", style=discord.ButtonStyle.success)
        async def CloseRequestButtonClose(self, interaction: discord.Interaction, button: discord.ui.button):

            data = util.JsonHandler.load_ticketusers()
            transcripts = self.bot.get_channel(config["transcripts_channel"])
            transcriptsClosedEmbed = discord.Embed(title="Newly closed ticket!", description=f"The newest closed ticket was #{interaction.channel.name}")

            if str(interaction.user.id) in data:
            
                if os.path.isdir("ticket-logs") == False:
                    os.mkdir("ticket-logs")     
                util.JsonHandler.new_json(f"ticket-logs/log-{interaction.channel.name}.json")

                await transcripts.send(embed=transcriptsClosedEmbed) 
                await transcripts.send(file=discord.File(f"tickets-logs/log-{interaction.channel.name},json"))

                await interaction.channel.delete()

            else:
                await interaction.response.send_message("You aren't able to accept a close request for someone else!", ephemeral=True)
        

        @discord.ui.button(label="Deny close request", style=discord.ButtonStyle.red)
        async def CloseRequestButtonKeepOpen(self, interaction: discord.Interaction, button: discord.ui.button):

            data = util.JsonHandler.load_ticketusers()
        
            if str(interaction.user.id) in data:
                deniedEmbed = discord.Embed(title="Close request denied!", description=f"{interaction.user.display_name} has denied the close request!", color=0xff6969)
                await interaction.response.edit_message(embed=deniedEmbed, view=None)
        
            else:
                await interaction.response.send_message("You aren't able to deny a close request for someone else!", ephemeral=True)



class TicketEmbed(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        super().__init__()
        self.bot = bot
    
    
    @commands.hybrid_command(description="Command for testing tickets")
    async def ticket(self, ctx):
        view = TicketButtons()
        await ctx.send(embed=ticketembed, view=view)
    
    @commands.hybrid_command(description="Request to close the current ticket!")
    async def closerequest(self, ctx):
        requestcloseembed = discord.Embed(title=f"This ticket has been requested to be closed by {ctx.author.display_name}", description="Would you like to accept?", color=0x69ff69)

        view = CloseRequestButtons(self.bot)

        await ctx.send(embed=requestcloseembed, view=view)

    @commands.hybrid_command(description="Closes the current ticket")
    async def close(self, interaction: discord.Interaction, reason: str) -> None:
        transcripts = self.bot.get_channel(config["transcripts_channel"])
        channel = interaction.channel

        channel_created_at = channel.created_at 
        closed_at = datetime.datetime.now().timestamp()


        transcriptsClosedEmbed = discord.Embed(title=f"Ticket closed! - {channel.name}", description="", color=0xA020F0)
        transcriptsClosedEmbed.add_field(name="Opened at:", value=f"<t:{int(channel_created_at.timestamp())}>", inline=True)
        transcriptsClosedEmbed.add_field(name="Closed by:", value=f"{interaction.author.display_name}", inline=True)
        transcriptsClosedEmbed.add_field(name="Closed at:", value=f"<t:{int(closed_at)}>", inline=True)
        transcriptsClosedEmbed.add_field(name="Reason:", value=f"{reason}")


        if os.path.isdir("ticket-logs") == False:
            os.mkdir("ticket-logs")
        log_path = (f"ticket-logs/log-{channel.name}.txt")
        
        messages = []
        async for message in interaction.channel.history(limit=None):
            messages.append(message)
        messages.reverse() 

        with open(log_path, "a", encoding="utf8") as f:
            for message in messages:

                timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                author = message.author.name.replace(',', '')
                content = message.content.replace(',', '')

                f.write(f'{timestamp}. {author}, {content}\n')

        await transcripts.send(embed=transcriptsClosedEmbed)
        await transcripts.send(file=discord.File(log_path))

        os.remove(path=log_path)
        await interaction.channel.delete()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicketEmbed(bot))  
