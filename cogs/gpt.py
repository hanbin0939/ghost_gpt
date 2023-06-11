import discord
from discord.ext import commands
import openai
import aiohttp
from config.config import *
import asyncio
from dotenv import load_dotenv
load_dotenv()
openai.api_key = key
async def gpt_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt }
        ]
    )
    return completion.choices[0].message.content

modlist = [759072684461391893]

def ListCheck():
    async def IsInList(ctx):
        member = ctx.message.author.id
        return member in modlist
    return commands.check(IsInList)

class Chat_gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    #@ListCheck()
    async def gpt(self,ctx,*,prompt: str):
        async with ctx.typing():
            await asyncio.sleep(2)
        response = await gpt_response(prompt)
        await ctx.send(response)

    @commands.command(help="ask a chat-gpt")
    async def gpt_d3(self, ctx:commands.Context, *,prompt:str):
        async with ctx.typing():
            await asyncio.sleep(2)
        async with aiohttp.ClientSession() as session:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=4000,
                temperature=0.7,
                )
            headers = {"Authorization" : f"banner{key}"}
            async with session.post("https://api.openai.com/v1/completions", json=response , headers=headers) as resp:
                output = response["choices"][0]["text"]
                embed = discord.Embed(title="chat GPT's response" , description=output,color=0xe6caff)
                print(output)
                await ctx.reply(embed=embed)

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if message.author.bot:
            return
            
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        prompt = user_message
        
        print(username + " said " + user_message.lower() + " in " + channel)

        if message.channel.name == 'beta-ai':
            async with message.channel.typing():
                await asyncio.sleep(3)
            respond = await gpt_response(prompt)
            await message.channel.send(respond)

    @gpt.error
    async def error_gpt(self, ctx,error):
        await ctx.reply(error)
        await ctx.reply("봇의 접근 권한이 없습니다!")

def setup(bot): 
    bot.add_cog(Chat_gpt(bot))