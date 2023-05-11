import discord
from discord.ext import commands
import openai
import aiohttp
from config.config import key
import asyncio
from dotenv import load_dotenv
load_dotenv()
openai.api_key = key
async def gpt_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


class Chat_gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gpt(self,ctx,*,prompt: str):
        async with ctx.typing():
            await asyncio.sleep(2)
        response = await gpt_response(prompt)
        await ctx.send(response)

    @discord.slash_command(name="chat_gpt_turbo")
    async def gpt(self,ctx,*,prompt: str):
        response = await gpt_response(prompt)
        await ctx.respond(response)
    

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Chat_gpt(bot)) # add the cog to the bot
