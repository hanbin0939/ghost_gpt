import discord
from discord.ext import commands

class user(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self,bot,member):
        channel = bot.get_channel(1083242633310261298) # Where ID is your welcome channel's ID
        guild = bot.get_guild(1069174895893827604)
        role = guild.get_role(1072660369274843257)
        await member.add_roles(role)
        embed = discord.Embed(title="welcome",description='만나서 반가워요!! XD',color=0x1700ff)
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(f'{member.mention} 님 {member.guild.name} 서버에 오신것을 환영합니다!!!',embed=embed)

    @discord.slash_command(aliases=['추방'])
    @commands.is_owner()
    async def kick_user(self, ctx, nickname: discord.Member):
        await nickname.kick()
        await ctx.respond(f"{nickname} 님이 추방되었습니다.")

    @discord.slash_command(aliases=['차단'])
    @commands.is_owner()
    async def ban_user(self, ctx, nickname: discord.Member):
        await nickname.ban()
        await ctx.respond(f"{nickname} 님이 차단되었습니다.")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(user(bot))