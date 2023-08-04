import discord
import aiohttp
from discord.ext import commands
from craiyon import Craiyon
from PIL import Image
from io import BytesIO
import time

class Dall_E(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="generate")
    async def genetate(self,ctx,*,prompt:str):
        ETA = int(time.time() + 60)
        msg = await ctx.send(f"이 그림을만드는데 시간이 걸립니다 ETA : <t:{ETA}:R>")
        async with aiohttp.request("POST","https://api.craiyon.com/v3",json={"prompt":prompt})as resp:
            r = await resp.json()
            generator = Craiyon()
            result = generator.generate(prompt)
            image = result.images
            for i in image:
                image = BytesIO(base64.decodebytes(i.encode("utf-8")))
                return await msg.edit(file = discord.File(image,"generatedImage.png"))
        

def setup(bot):
    bot.add_cog(Dall_E(bot))