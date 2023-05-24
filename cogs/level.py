import discord
from discord.ext import commands
import aiosqlite
import asyncio
import random
from easy_pil import*


class Level(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        print("LEVEL SYSTEM ACTIVE")
        setattr(self.bot,"db",await aiosqlite.connect("level.db"))
        await asyncio.sleep(1)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute('''CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER, name INTEGER)''')

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if message.author.bot:
            return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp, level FROM levels WHERE user =? AND guild =? AND name =?",(str(author.id),str(guild.id),author.name))
            result = await cursor.fetchone()
            if not result:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild, name) VALUES (?, ?, ?, ?, ?)", (0, 0, str(author.id), str(guild.id),author.name))
                xp = 0
                level = 1
            else:
                xp = result[0]
                level = result[1]
            if level <4:
                xp += random.randint(1, 4) * 4

            else:
                xp += random.randint(1, 3) * 3

        
            if xp >= 100:
                level += 1
                xp = 0
                await message.channel.send(f"{author.mention} 님이 **{level}** 이 되었습니다!!")

            await cursor.execute("UPDATE levels SET xp = ?, level = ? WHERE user = ? AND guild = ? AND name = ?",(xp, level, str(author.id), str(guild.id),author.name))
        await self.bot.db.commit()

    @commands.command()
    async def my_level(self,ctx,member: discord.Member = None):
        if member is None:
            member = ctx.author
            profile_picture = await load_image_async(str(member.avatar.url))
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(member.id,ctx.guild.id))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(member.id,ctx.guild.id))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id))
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0
            user_data = {
                "name" : f"{member.name}#{member.discriminator}",
                "xp" : xp,
                "level" : level,
                "next_level_xp" : 100,
                "percentage": xp,
            }

            background = Editor(Canvas((900,300),color="#141414"))
            profile_picture = await load_image_async(str(member.avatar.url))
            profile = Editor(profile_picture).resize((150,150)).circle_image()

            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=20)

            card_right_shape = [(600,0), (750, 300), (900, 300), (900,0)]

            background.polygon(card_right_shape,color="#FFFFFF")
            background.paste(profile, (30,30))

            background.rectangle((30,220),width=650,height=40,color="#FFFFFF",radius=20)
            background.bar((30,220),max_width=650, height=40, percentage=user_data["percentage"],color="#282828",radius=20,)
            background.text((200,40), user_data["name"], font= poppins, color="#FFFFFF")

            background.rectangle((200,100),width=350,height=2, fill="#FFFFFF")
            background.text(
                (200,130),
                f"level - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level_xp']}",
                font=poppins_small,
                color="#FFFFFF"
                )

            file = discord.File(fp=background.image_bytes,filename="levelcard.png")
            await ctx.reply(file=file)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Level(bot))