import discord
import asyncio
from dotenv import load_dotenv
from discord.commands import Option
from discord.ext import commands
from config.config import *

load_dotenv()

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all(), owner_ids=[
                   759072684461391893])  # 봇의 접두사 설정
bot.remove_command("help")
# cogs 폴더의 절대 경로 얻기
# Pycharm에서 바로 상대 경로를 사용하면 오류가 발생하기 때문에 따로 절대경로를 얻어야한다.
cogs_path = 'cogs'
cogs_list = [
    'gpt',
    'user',
    "msg",
    "dall_e",
    "level",
    "ticket"
]


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(
            label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


@bot.slash_command()
async def modal_slash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="Modal via Slash Command")
    await ctx.send_modal(modal)


@bot.event
async def on_ready():  # 봇 준비 시 1회 동작하는 부분
    # 봇 이름 하단에 나오는 상태 메시지 설정
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Ghost_gpt"))
    print("Bot is ready")


@bot.slash_command(guild_ids=[1069174895893827604])
async def beta_testing(ctx):
    guild = bot.get_guild(1069174895893827604)
    role = guild.get_role(1088477030661763183)
    user = ctx.author
    await user.add_roles(role)
    await ctx.respond("베타 태스팅에 조인하셧습니다!")
@bot.command(name="help")
async def help(ctx):
    file = discord.File("Ghosts_insignia_CoDG.png", filename="image.png")
    embed = discord.Embed(title="Command list")
    embed.set_author(name="Ghosty", icon_url="attachment://image.png")
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="$help",value="Show this message")
    embed.add_field(name="$gpt",value="Ask a Chat GPT (gpt-3.5-turbo-16k)")
    embed.add_field(name="$gpt_d3",value="ask a Chat GPT (text-davinci-003)")
    embed.add_field(name="$generate",value="Draw a topic")
    embed.add_field(name="$level",value="See your LEVEL")
    embed.add_field(name="$level_madness",value="Madness Combat LEVEL")
    embed.add_field(name="$join",value="Join a voice chat")
    embed.add_field(name="$leave",value="Leave a voice chat")
    await ctx.reply(embed=embed, file=file)

@bot.slash_command()
async def help(ctx):
    await ctx.defer()
    await asyncio.sleep(3)
    file = discord.File("Ghosts_insignia_CoDG.png", filename="image.png")
    embed = discord.Embed(title="Command list")
    embed.set_author(name="Ghosty", icon_url="attachment://image.png")
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="$help",value="Show this message")
    embed.add_field(name="$gpt",value="Ask a Chat GPT (gpt-3.5-turbo-16k)")
    embed.add_field(name="$gpt_d3",value="ask a Chat GPT (text-davinci-003)")
    embed.add_field(name="$generate",value="Draw a topic")
    embed.add_field(name="$level",value="See your LEVEL")
    embed.add_field(name="$level_madness",value="Madness Combat LEVEL")
    embed.add_field(name="$join",value="Join a voice chat")
    embed.add_field(name="$leave",value="Leave a voice chat")
    await ctx.reply(embed=embed, file=file)
bot.run(token_beta)
