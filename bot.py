import discord
from discord.ext import commands
import json

#got the Token this way because Python was being stupid and wouldn't import another file and I was too lazy to figure it out XD
with open('config.json') as f:
	file = json.load(f)
TOKEN = file["TOKEN"]
bot = commands.Bot(command_prefix="~")

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

bot.run(TOKEN)
