import discord
from discord.ext import commands
from discord.commands import Option
from discord.utils import get
import datetime

class user(commands.Cog):

    new_member_role_name = "DEV Role"
    rules_message_id = 1084676435786084422

    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(1083242633310261298) # Where ID is your welcome channel's ID
        guild = self.bot.get_guild(1069174895893827604)
        role = guild.get_role(1072660369274843257)
        await member.add_roles(role)
        embed = discord.Embed(title="welcome",description='만나서 반가워요!! XD',color=0x1700ff)
        embed.set_thumbnail(url=member.avatar.url)
        await member.send(f"{member.mention} welcome to server!")
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

    @commands.command()
    async def profile(self,ctx):
        member = ctx.author
        roles = [role for role in member.roles[1:]]
        embed = discord.Embed(title=f"{ctx.author}",color=0x929292)
        embed.add_field(name="**•ID•**", value=f"{member.id}", inline=True)
        embed.add_field(name="**•Status•**", value=str(member.status).replace("dnd", "Do Not Disturb"), inline=True)
        embed.set_thumbnail(url=f"{member.avatar.url}")
        embed.add_field(name=f"**•Roles• ({len(ctx.author.roles) - 1})**", value='• '.join([role.mention for role in roles]), inline=False)
        embed.add_field(name="**•Account Created At•**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
        embed.add_field(name="**•Joined Server At•**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
        embed.set_footer(icon_url = f"{ctx.author.avatar.url}", text = f"Requested by {ctx.author}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=embed)

    @discord.slash_command()
    async def profile(self,ctx):
        member = ctx.author
        roles = [role for role in member.roles[1:]]
        embed = discord.Embed(title=f"{ctx.author}",color=0x929292)
        embed.add_field(name="**•ID•**", value=f"{member.id}", inline=True)
        embed.add_field(name="**•Status•**", value=str(member.status).replace("dnd", "Do Not Disturb"), inline=True)
        embed.set_thumbnail(url=f"{member.avatar.url}")
        embed.add_field(name=f"**•Roles• ({len(ctx.author.roles) - 1})**", value='• '.join([role.mention for role in roles]), inline=False)
        embed.add_field(name="**•Account Created At•**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
        embed.add_field(name="**•Joined Server At•**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
        embed.set_footer(icon_url = f"{ctx.author.avatar.url}", text = f"Requested by {ctx.author}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.rules_message_id == payload.message_id:
            if payload.emoji.name == "✅":
                for role in await self.bot.guilds[0].fetch_roles():
                    if role.name == self.new_member_role_name:
                        await payload.member.add_roles(role)
                        break
    
    async def setup_role(self):
        exists = False
        for role in await self.bot.guilds[0].fetch_roles():
            if role.name == self.new_member_role_name:
                exists = True
                break
        if exists:
            return 
        permissions= discord.Permissions.none()
        permissions.view_channel = True
        
        await self.bot.guilds[0].create_role(
            name=self.new_member_role_name,
            color=discord.Color.red(),
            hoist=True, 
            permissions =permissions
        )

    @commands.command()
    async def dev_role(ctx):
        message = "이모지를 눌러 칭호를 얻으세요!"
        react_message = await ctx.send(message)
        await react_message.add_reaction(emoji="✅")
    



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(user(bot))