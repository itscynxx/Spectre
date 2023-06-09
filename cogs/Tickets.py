import discord
from discord.ext import commands

ticket = discord.Embed(title="**Please go to the [Northstar Wiki FAQ](https://r2northstar.gitbook.io/r2northstar-wiki/faq) and use `Ctrl + F` to search for the error you're experiencing before opening a ticket", description=", as most common errors can be found there without needing to wait for a response for someone.")
ticket.add_field(name="Everyone involved in helping does it entirely for fun or out of passion, with no monetary gain, so please don't expect an immediate response.\n", value="Clicking the buttons below this message will open a ticket.\n(Public = People volunteering can see your ticket)\n(Staff-only = Only Northstar staff can see your ticket)")

class TicketButtons(discord.ui.View):    

    @discord.ui.button(label="Open a public ticket!", style=discord.ButtonStyle.success)
    async def openTicket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticketname = "ticket-" + str(interaction.user.display_name)
        category = discord.utils.get(interaction.guild.categories, id=1111762231454072964)
        await interaction.guild.create_text_channel(name=ticketname, category=category)
        await interaction.followup("Successfully created your ticket!")
    
    @discord.ui.button(label="Open a staff-only ticket!", style=discord.ButtonStyle.red)
    async def openStaffTicket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staffticketname = "staff-ticket-" + str(interaction.user.display_name)
        category = discord.utils.get(interaction.guild.categories, id=1111762231454072964)
        await interaction.guild.create_text_channel(name=staffticketname, category=category)
        await interaction.reply("Successfully created a staff only ticket!")

class TicketEmbed(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(description="Command for testing tickets")
    async def ticket(self, ctx):
        view = TicketButtons()
        await ctx.send(embed=ticket, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicketEmbed(bot))