import discord
from discord.ext import commands

class Test():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def cog_test(self, ctx):
		await ctx.send("Cog is working")

def setup(bot):
	bot.add_cog(Test(bot))