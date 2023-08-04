import discord
from discord.ext import commands
from color_ansi import Color
import traceback
import openai
import aiohttp
from config.config import *
import asyncio
from dotenv import load_dotenv
load_dotenv()
openai.api_key = key

def code_respose(prompt):
    completion = openai.Completion.create(
        model="code-davinci-003",
        prompt=prompt,
        max_tokens=8000,
        temperature=0.7
    )
    return completion.choices[0].message.content

def gpt_3_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return completion.choices[0].message.content

async def gpt_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt }
        ]
    )
    return completion.choices[0].message.content

modlist = [759072684461391893]

def ListCheck():
    async def IsInList(ctx):
        member=ctx.message.author.id
        return member in modlist
    return commands.check(IsInList)

class Chat_gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Color.GREEN + "[open-ai]-Ready"+Color.RESET)

    @discord.slash_command(description="talk with GPT-4 : )")
    #@ListCheck()
    async def gpt_4(self,ctx,*,prompt: str):
        await ctx.defer()
        await asyncio.sleep(60)
        response = await gpt_response(prompt)
        await ctx.respond(response)

    @commands.command(description="talk with GPT-4 : )")
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
                await ctx.reply(output)

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if message.author.bot or message.content.startswith('$gpt'):
            return
            
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        prompt = user_message
        
        print(username + " said " + user_message.lower() + " in " + channel)

        if message.channel.name == 'chat-gpt':
            async with message.channel.typing():
                await asyncio.sleep(3)
            respond = await gpt_response(prompt)
            await message.channel.send(respond)
        
        if message.channel.name == "code-davinci-003":
            async with message.channel.typing():
                await asyncio.sleep(3)
            respond_c = await code_respose(prompt)
            await message.channel.send(respond_c)

    @gpt.error
    async def error_gpt(self, ctx,error):
        await ctx.reply(error)

    @commands.Cog.listener("on_error")
    async def on_error(self,event, *args, **kwargs):
        exc_info = traceback.format_exc()
        print(Color.RED+ Color.BOLD+f"[ERROR] {event} - {args} - {kwargs}"+ Color.RESET +Color.RESET)
        print(Color.RED+f"{exc_info}"+Color.RESET)

def setup(bot): 
    bot.add_cog(Chat_gpt(bot))