import discord
from discord.ext import commands

class Ranks(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ranks(self, ctx):
		"View all assignable ranks in the server"
		ranks = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		if not ranks["ranks"]:
			await ctx.send("This server has no ranks")
		else:
			ranks = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
			rank_list = list(ranks["ranks"])
			await ctx.send(", ".join(rank_list))

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def add_rank(self, ctx, emoji_id: int, *, rank: str):
		"Add an assignable rank to the server"
		ranks = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		role = discord.utils.get(ctx.guild.roles, name=rank)
		if not ranks:
			await self.bot.db.ranks.insert_one({"_id": ctx.guild.id, "ranks": {}})
		if role:
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$set": {f"ranks.{str(role.name)}": emoji_id}})
			await ctx.send(f"I added {str(role.name)} as a rank")
		elif rank in ranks["ranks"]:
			await ctx.send("That rank already exists")
		else:
			await ctx.guild.create_role(name=rank)
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$set": {f"ranks.{rank}": emoji_id}})
			await ctx.send(f"I created and added {rank} as a rank")

	@commands.command()
	@commands.has_permissions(manage_guild=True)
	async def rank_channel(self, ctx, channel):
		"Set the channel for the rank reactions"
		ranks = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		channel = channel.replace("<", "").replace(">", "").replace("#", "")
		if not ranks:
			await self.bot.db.ranks.insert_one({"_id": ctx.guild.id, "ranks": {}, "rank_channel": int(channel)})
			await ctx.send(f"Set the rank channel to <#{channel}>")
		else:
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$set": {"rank_channel": int(channel)}}, upsert=True)
			await ctx.send(f"Set the rank channel to <#{channel}>")


	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def remove_rank(self, ctx, * , rank: str):
		ranks = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		if not ranks:
			await ctx.send('This server has no ranks')
		elif rank not in ranks["ranks"]:
			await ctx.send("That rank doesn't exist")
		elif rank in ranks["ranks"]:
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$unset": {f"ranks.{rank}": ""}})
			await ctx.send(f'I deleted {rank} from the server ranks')

	@commands.command()
	@commands.has_permissions(manage_guild=True)
	async def start_ranks(self, ctx):
		server = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		rank_channel = self.bot.get_channel(server["rank_channel"])
		ranks = server["ranks"]
		msg = ["**Self Assignable Ranks**\n", "How this works:\n", "React with the appropriate emoji to get the role, unreact to remove the role\n"]
		ids = []
		for rank in ranks:
			emoji = self.bot.get_emoji(ranks[rank])
			msg.append(f"{rank}: <:{emoji.name}:{emoji.id}>\n")
			ids.append(emoji.id)
		if not server["rank_channel"]:
			await ctx.send(f"The rank channel has not been set for this server. Please set it with {ctx.prefix}rank_channel <channel>.")
		else:
			msg = ("").join(msg)
			reactions = await rank_channel.send(msg)
			await self.bot.db.ranks.update_one({"_id": ctx.guild.id}, {"$set": {"message_id": reactions.id}})
			for id in ids:
				emoji = self.bot.get_emoji(id)
				await reactions.add_reaction(emoji)

	@commands.command()
	@commands.has_permissions(manage_guild=True)
	async def edit_ranks(self, ctx, option, emoji_id: int, *, rank: str):
		server = await self.bot.db.ranks.find_one({"_id": ctx.guild.id})
		channel = self.bot.get_channel(server["rank_channel"])
		if not server["message_id"]:
			await ctx.send("No message id was set. ~start_ranks must be ran first.")
		else:
			message_id = server["message_id"]
			message = await channel.get_message(message_id)
			emoji = self.bot.get_emoji(emoji_id)
			if option == "add":
				await ctx.invoke(self.bot.get_command('add_rank'), emoji_id=emoji_id, rank=rank)
				await message.edit(content=f"{message.content}\n{rank}: <:{emoji.name}:{emoji_id}>")
				await message.add_reaction(emoji)
			elif option == "remove":
				await ctx.invoke(self.bot.get_command("remove_rank"), rank=rank)
				await message.edit(content=message.content.replace(f"\n{rank}: <:{emoji.name}:{emoji_id}>", ""))
				for reaction in message.reactions:
					if reaction.emoji.id == emoji_id:
						async for user in reaction.users():
							await message.remove_reaction(emoji, user)
			else:
				await ctx.send("The two options for edit_ranks is add and remove")
			await ctx.send("Succesfully edited the rank message")

	
	#Events upon reactions
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		server = await self.bot.db.ranks.find_one({"_id": payload.guild_id})
		channel = self.bot.get_channel(payload.channel_id)
		if payload.channel_id == server["rank_channel"]:
			for rank in server["ranks"]:
				if server["ranks"][rank] == payload.emoji.id:
					role = discord.utils.get(channel.guild.roles, name=rank)
					await channel.guild.get_member(payload.user_id).add_roles(role, reason="selfrole")
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		server = await self.bot.db.ranks.find_one({"_id": payload.guild_id})
		channel = self.bot.get_channel(payload.channel_id)
		if payload.channel_id == server["rank_channel"]:
			for rank in server["ranks"]:
				if server["ranks"][rank] == payload.emoji.id:
					role = discord.utils.get(channel.guild.roles, name=rank)
					await channel.guild.get_member(payload.user_id).remove_roles(role, reason="selfrole")
	@commands.Cog.listener()				
	async def on_message(self, message):
		if message.content.startswith("?rank"):
			await message.channel.send("Please get your ranks from #bot-role-assignment")

		

def setup(bot):
	bot.add_cog(Ranks(bot))

