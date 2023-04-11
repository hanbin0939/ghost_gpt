import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config.config import token ,key
load_dotenv()
openai.api_key = key
DISCORD_TOKEN = os.getenv(token)
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

async def gpt_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

@bot.command(name="gpt", help="Ask GPT-3.5 Turbo a question or send a message")
async def gpt(ctx, *, prompt: str):
    response = await gpt_response(prompt)
    await ctx.send(response)

bot.run(token)