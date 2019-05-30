import discord
from discord.ext import commands
import asyncio

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user, *, reason=None):
		mod_log = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		try:
			await user.kick(reason=reason)
		except discord.Forbidden():
			await ctx.send("I don't have the proper permissios to kick this member")
		await ctx.send(f"**{user} was kicked**")
		if mod_log["mod_log"]:
			channel = self.bot.get_channel(mod_log["mod_log"])
			embed = discord.Embed(title="Member kicked!", color=discord.Color.red(), description=f"{user} was kicked by {ctx.author}")
			embed.add_field(name="Reason", value=reason)
			embed.set_image(url=user.avatar_url)
			await channel.send(embed=embed)

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user, *, reason=None):
		mod_log = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		try:
			await user.ban(reason=reason)
		except discord.Forbidden():
			await ctx.send("I don't have the proper permissions to ban this member")
		await ctx.send(f"**{user} was banned**")
		if mod_log["mod_log"]:
			channel = self.bot.get_channel(mod_log["mod_log"])
			embed = discord.Embed(title="Member banned!", color=discord.Color.red(), description=f"{user} was banned by {ctx.author}")
			embed.add_field(name="Reason", value=reason)
			embed.set_image(url=user.avatar_url)
			await channel.send(embed=embed)

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def warn(self, ctx, user, *, reason):
		mod_log = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		warns = await self.bot.db.warns.find_one({"_id": user.id})
		if not warns:
			await self.bot.db.warns.insert_one({"_id": user.id})
			warns = [reason]
		else:
			warns = warns["warnings"]
			warns.append(reason)

		await self.bot.db.warns.update_one({"_id": user.id}, {"$set": {"warnings": warns}})
		await ctx.send(f"{user} was warned for {reason}")
		if mod_log["mod_log"]:
			channel = self.bot.get_channel(mod_log["mod_log"])
			embed = discord.Embed(title="Member warned!", color=discord.Color.red(), description=f"{user} was warned by {ctx.author}")
			embed.add_field(name="Warning #", value=len(warns))
			embed.add_field(name="Reason", value=reason)
			embed.set_image(url=user.avatar_url)
			await channel.send(embed=embed)

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def warnings(self, ctx, user):
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		warns = await self.bot.db.warns.find_one({"_id": user.id})
		if not warns:
			await ctx.send("This user has no warnings :D")
		else:
			embed = discord.Embed(title=f"{user}'s warnings", color=discord.Color.red(), description=", ".join(warns["warnings"]))
			embed.add_field(name="Total Warnings", value=len(warns["warnings"]))
			embed.set_image(url=user.avatar_url)
			await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def remove_warn(self, ctx, user, *, warning):
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		warns = await self.bot.db.warns.find_one({"_id": user.id})
		if not warns:
			await ctx.send("This user has no warnings to remove")
		else:
			warns = warns["warnings"]
			if warning in warns:
				warns.remove(warning)
				await self.bot.db.warns.update_one({"_id": user.id}, {"$set": {"warnings": warns}})
				await ctx.send(f"Succesfully removed the warning from {user}")
			else:
				await ctx.send("That user has never been warned for that")

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, num: int):
		try:
			await ctx.message.delete()
			await ctx.channel.purge(limit=num)
			resp = await ctx.send(f"Succesfully deleted {num} messages.")
			await asyncio.sleep(5)
			await resp.delete()
		except discord.Forbidden():
			await ctx.send("I don't have the proper permissions to delete messages.")

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def mute(self, ctx, user, time, *, reason):
		mod_log = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		try:
			await ctx.send(f'{user} has been muted')
			if mod_log["mod_log"]:
					channel = self.bot.get_channel(mod_log["mod_log"])
					embed = discord.Embed(title="Member muted!", color=discord.Color.red(), description=f"{user} was muted by {ctx.author}")
					embed.add_field(name="Length", value=time)
					embed.add_field(name="Reason", value=reason)
					embed.set_image(url=user.avatar_url)
					await channel.send(embed=embed)
			for channel in ctx.guild.channels:
				overwrite = discord.PermissionOverwrite()
				overwrite.send_messages = False
				await channel.set_permissions(user, overwrite=overwrite)
			if str(time) != "infinite":
				time = int(time) * 60
				await asyncio.sleep(time)
				await ctx.invoke(self.bot.get_command("unmute"), user=str(user.id), reason="Time Expired")
		except discord.Forbidden:
			await ctx.send("I don't have the proper permissions to delete this user.")

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def unmute(self, ctx, user, *, reason):
		mod_log = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		try:
			for channel in ctx.guild.channels:
				await channel.set_permissions(user, overwrite=None)
			await ctx.send(f'{user} has been unmuted')
		except discord.Forbidden:
			await ctx.send("I don't have the proper permissions to delete this user.")
		if mod_log["mod_log"]:
			channel = self.bot.get_channel(mod_log["mod_log"])
			embed = discord.Embed(title="Member unmuted!", color=discord.Color.red(), description=f"{user} was unmuted")
			embed.add_field(name="Reason", value=reason)
			embed.set_image(url=user.avatar_url)
			await channel.send(embed=embed)








def setup(bot):
	bot.add_cog(Mod(bot))