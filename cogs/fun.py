import discord
from discord.ext import commands
import aiohttp

class Fun():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def floof(ctx):
		async with self.bot.session.get('https://randomfox.ca/floof/') as resp:
			json = await resp.json()
		embed = discord.Embed(title="Floof!", color=discord.Color.blue())
		embed.set_image(url=json["image"])
		await ctx.send(embed=embed)

	@commands.command()
	async def cat(ctx):
		async with self.bot.session.get("https://catapi.glitch.me/random") as resp:
			json = await resp.json()
		embed = discord.Embed(title="Kitty!", color=discord.Color.blue())
		embed.set_image(url=json["url"])
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Fun(bot))
