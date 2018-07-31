import discord
from discord.ext import commands

class Ranks():

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ranks(self, ctx):
		"View all assignable ranks in the server"
		if ctx.guild.id not in self.bot.db.ranks:
			await ctx.send("This server has no ranks")
		elif ranks[ctx.guild.id].count_documents() == 0:
			await ctx.send("This server has no ranks")
		else:
			ranks = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
			rank_list = []
			async for rank in ranks.find({"_id": ctx.guild.id}):
				rank.append(rank)

			await ctx.send(", ".join(rank_list))

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def add_rank(self, ctx, *, rank: str):
		"Add an assignable rank to the server"
		ranks = self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		role = discord.utils.find(lambda m: rank.lower() in m.name.lower(), ctx.guild.roles)
		if ctx.guild.id not in ranks:
			await self.bot.db.ranks.insert_one({"_id": ctx.guild.id})
		if role:
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$set": {str(role.name): str(role.name)}})
			await ctx.send(f"Added {role.name} as a rank")
		elif rank in ranks:
			await ctx.send("That rank already exists")
		else:
			await ctx.guild.create_role(name=rank)
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$set": {str(role.name): str(role.name)}})
			await ctx.send(f"I created and added {rank} as a rank")

def setup(bot):
	bot.add_cog(Ranks(bot))

