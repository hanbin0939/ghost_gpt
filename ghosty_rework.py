import discord
from dotenv import load_dotenv
from discord.commands import Option
from discord.ext import commands
from config.config import *
import asyncio
import aiohttp
import openai

load_dotenv()

bot = commands.Bot(command_prefix='$',intents=discord.Intents.all(),owner_ids=[759072684461391893])  # 봇의 접두사 설정
bot.remove_command("help")
# cogs 폴더의 절대 경로 얻기
# Pycharm에서 바로 상대 경로를 사용하면 오류가 발생하기 때문에 따로 절대경로를 얻어야한다.
cogs_path = 'cogs'
cogs_list = [
    'gpt',
    'user',
    "msg"
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():  # 봇 준비 시 1회 동작하는 부분
    # 봇 이름 하단에 나오는 상태 메시지 설정
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Alpha testing"))
    print("Bot is ready")

#rework soon...
@bot.slash_command(guild_ids = [1069174895893827604])
async def dev_role(ctx):
    guild = bot.get_guild(1069174895893827604)
    role = guild.get_role(1104911269766631584)
    user = ctx.author
    await user.add_roles(role)
    await ctx.respond("you got a **DEV** role.")
    
#rework soon....
@bot.command(name="text-davinci-003",guild_ids=[1069174895893827604],help="ask a chat-gpt")
async def ask_gpt(ctx:commands.Context, *,prompt:str):
    async with ctx.typing():
        await asyncio.sleep(2)
    async with aiohttp.ClientSession() as session:
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=3000,
                temperature=0.7,
                )

        headers = {"Authorization" : f"banner{key}"}
        async with session.post("https://api.openai.com/v1/completions", json=response , headers=headers) as resp:
            output = response["choices"][0]["text"]
            embed = discord.Embed(title="chat GPT's response" , description=output,color=0xe6caff)
            print(output)
            await ctx.reply(embed=embed)

@bot.command(name="help",help="show this commands")
async def help(ctx):
    embed = discord.Embed(title="help")
    file = discord.File("Ghosts_insignia_CoDG.png",filename="image.png")
    embed.set_author(name="command list",icon_url="attachment://image.png")
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="$help",value="Shows this message",inline=False)
    embed.add_field(name="$gpt",value="ask a Chat-Gpt (model = gpt-3.5-turbo)",inline=False)
    embed.add_field(name="$text-davinci-003",value=" Ask text-davinci-003 (Chat-gpt3)",inline=False)
    embed.add_field(name="$generate",value="Ghosty 가 당신이 원하는 이미지를 그려줍니다!\n(model = Dall-E)",inline=False)
    embed.add_field(name="/dev_role",value="you can get develoer community acess room.",inline=False)
    embed.add_field(name="/chat_gpt_turbo",value="Slash command gpt3.5",inline=False)
    await ctx.reply(embed=embed,file=file)

bot.run(token)