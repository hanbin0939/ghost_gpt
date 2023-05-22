import discord
from discord.ext import commands
import aiosqlite
import random
from easy_pil import*


class Level(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        print("Ready")
        setattr(self.bot,"db",await aiosqlite.connect("level.db"))
        #await asyncio.sleep(1)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute('''CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)''')

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if message.author.bot:
            return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp, level FROM levels WHERE user =? AND guild =?",(str(author.id),str(guild.id),))
            result = await cursor.fetchone()
            if not result:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, str(author.id), str(guild.id)))
                xp = 0
                level = 0
            else:
                xp = result[0]
                level = result[1]
            if level < 5:
                xp += random.randint(1,4) * 4
            else:
                rand = random.randint(1,(level//4))
                if rand == 1:
                    xp += random.randint(1,4) * 2

        
            if xp >= 100:
                level += 1
                xp = 0
                await message.channel.send(f"{author.mention} 님이 **{level}** 이 되었습니다!!")

            await cursor.execute("UPDATE levels SET xp = ?, level = ? WHERE user = ? AND guild = ?",(xp, level, str(author.id), str(guild.id)))
        await self.bot.db.commit()

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Level(bot))