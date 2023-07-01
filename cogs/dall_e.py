import discord
from discord.ext import commands
from discord.commands import Option
import openai
import asyncio
from dotenv import load_dotenv
load_dotenv()

class dall_E(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def generate(self,  ctx,  *, prompt):
        response = openai.Image.create(
            prompt=prompt,
            n=2,
            max_tokens=512,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await ctx.reply(image_url)

    @generate.error
    async def error(self,ctx,error):
        await ctx.reply(error)

    @discord.slash_command()
    async def generate_command(self,  ctx,  *, prompt, size:Option(str,"사이즈를 고르시오.", choices=["256x256", "512x512", "1024x1024"] )):
        #await ctx.respond("이미지가 나올때까지 시간이걸립니다...")
        try:
            await ctx.defer()
            await asyncio.sleep(30)
            response = openai.Image.create(
                prompt = prompt,
                n=2,
                size = size
            )
            image_url = response['data'][0]['url']
            await ctx.respond(image_url)
            await ctx.send(f"\n{ctx.author.mention} 님 주문하신 {prompt} 그림 {size} 로 나오셧습니다~~")
        except discord.NotFound:
            print("Interaction이 이미 만료되었거나 존재하지 않습니다.")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(dall_E(bot))