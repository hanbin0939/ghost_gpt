import discord
from discord.ext import commands
from discord.utils import get

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        """
        Sends a message with a 'Create Ticket' button.
        """
        view = CreateTicketView()

        await ctx.send("Click the button to create a ticket!", view=view)

class CreateTicketView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Add a button to the View
        self.add_item(discord.ui.Button(label='Create Ticket'))

    @discord.ui.button(label='Create Ticket')
    async def create_ticket_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Handles the 'Create Ticket' button click: creates a new ticket channel.
        """
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        category = discord.utils.get(guild.categories, name='Tickets')

        # If the 'Tickets' category does not exist, create it
        if category is None:
            category = await guild.create_category('Tickets')

        # Create a new ticket channel in the 'Tickets' category
        channel = await category.create_text_channel('ticket', overwrites=overwrites)

        # Add a 'Close Ticket' button to the new channel
        view = CloseTicketView()
        await channel.send(f"New ticket created by {interaction.user.mention}! Click the button to close the ticket.", view=view(timeout=None))

        # Respond to the button click
        await interaction.response.send_message(f"Created a new ticket: {channel.mention}!")

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Add a button to the View
        self.add_item(discord.ui.Button(label='Close Ticket'))

    @discord.ui.button(label='Close Ticket')
    async def close_ticket_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Handles the 'Close Ticket' button click: deletes the ticket channel.
        """
        channel = interaction.channel

        # Delete the ticket channel
        await channel.delete()

        # Respond to the button click
        await interaction.response.send_message('The ticket was closed!')

def setup(bot):
    bot.add_cog(TicketCog(bot))
