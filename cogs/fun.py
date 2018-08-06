import discord
from discord.ext import commands
import aiohttp
import random

ballans = [
    "It is certain",
	"It is decidedly so", 
   	"Without a doubt",
	"Yes definitely",
	"You may rely on it",
	"As I see it yes",
	"Most likely",
	"Outlook good",
	"Yes",
	"Signs point to yes",
	"Reply hazy try again",
	"Ask again later",
	"Better not tell you now",
	"Cannot predict now",
	"Concentrate and ask again",
	"Don't count on it",
	"My reply is no",
	"My sources say no",
	"Outlook not so good",
	"Very doubtful"
        "No"
]

class Fun():
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name= "8ball")
	async def ball(self, ctx, *, question:str):
    	#gimmie sum ballz
		await ctx.send("{}: {}".format(ctx.author.name, random.choice(ballans)))

	@commands.command()
	async def floof(self, ctx):
		async with self.bot.session.get('https://randomfox.ca/floof/') as resp:
			json = await resp.json()
		embed = discord.Embed(title="Floof!", color=discord.Color.blue())
		embed.set_image(url=json["image"])
		await ctx.send(embed=embed)

	@commands.command()
	async def cat(self, ctx):
		async with self.bot.session.get("https://catapi.glitch.me/random") as resp:
			json = await resp.json()
		embed = discord.Embed(title="Kitty!", color=discord.Color.blue())
		embed.set_image(url=json["url"])
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Fun(bot))
