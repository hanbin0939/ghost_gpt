import discord
from discord.ext import commands
from discord import ui, Interaction

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        if ctx.channel.name == 'verification-channel':  # 추가된 라인
            view = VerifyView(ctx.guild)
            await ctx.send("Click the button below to verify yourself!", view=view)


class VerifyButton(ui.Button['VerifyView']):
    def __init__(self):
        super().__init__(label="Verify", style=discord.ButtonStyle.green)

    async def callback(self, interaction: Interaction):
        if interaction.channel.name == 'verification-channel':  # 추가된 라인
            guild = interaction.guild
            member = guild.get_member(interaction.user.id)
            role = discord.utils.get(guild.roles, name="Verified")
            if role is not None:
                await member.add_roles(role)
                await interaction.response.send_message("You have been verified!", ephemeral=True)


class VerifyView(ui.View):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        self.add_item(VerifyButton())

def setup(bot):
    bot.add_cog(VerificationCog(bot))
