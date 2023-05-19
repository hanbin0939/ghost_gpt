import discord
from discord import Option
from discord.ext import commands
import asyncio

class message(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if "hello" in message.content:
            await message.channel.send(f"{message.author.mention}nice to meet you let's talk")
'''
        if not message.guild: return # DM Message
        if message.author.guild_permissions.manage_guild:

            if message.content.startswith("!청소 "):
                purge_number = message.content.replace("!청소 ", "")
                check_purge_number = purge_number.isdigit()

            if check_purge_number == True:
                await message.channel.purge(limit=int(purge_number) + 1)
                await message.channel.send(f"**{purge_number}개**의 메시지를 삭제했습니다.")
                await asyncio.sleep(5)

            else:
                await message.channel.send("올바른 값을 입력해주세요.")
'''
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(message(bot))

