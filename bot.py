import discord
from discord.ext import commands
import time
import os

#got the Token this way because Python was being stupid and wouldn't import another file and I was too lazy to figure it out XD
bot = commands.Bot(command_prefix="~")
cogs = {"test"}

@bot.event
async def on_ready():
	print('------------------------------------')
	print('THE BOT IS ONLINE')
	print('------------------------------------')
	print("Name: {}".format(bot.user.name))
	print('Author: The Programming Discord :D')
	print("ID: {}".format(bot.user.id))
	print('DV: {}'.format(discord.__version__))

@bot.command()
async def online(ctx):
	await ctx.send("I am online :D")

@bot.command()
async def ping(ctx):
    t1 = time.perf_counter()
    message = await ctx.send("checking ping...")
    t2 = time.perf_counter()
    ping = round((t2-t1)*1000)
    await message.edit(content=f":ping_pong: Pong! `{ping}`ms")


if __name__ == "__main__":
    for extension in cogs:
        try:
            bot.load_extension(f"cogs.{extension}")
            print('Loaded: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error on load: {}\n{}'.format(extension, exc))

	
bot.run(os.environ.get("TOKEN"))
