import discord
from discord.ext import commands

class Config(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(manage_guild=True)
	async def config(self, ctx, option, *, text: str):
		server = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if not server:
			await self.bot.db.config.insert_one({"_id": ctx.guild.id})
		if option == "welcome_message":
			await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"welcome_message": text, "channel": True}})
			await ctx.send(f"Succesfully changed the welcome message to {text}")
		elif option == "leave_message":
			await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"leave_message": text, "channel": True}})
			await ctx.send(f"Succesfully changed the leave message to {text}")
		elif option == "welcome/leave_channel":
			text = text.replace("<", "").replace("#", "").replace(">", "")
			await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"welcome/leave_channel": int(text), "channel": True}})
			await ctx.send(f"Succesfully changed the welcome/leave channel to {text}")
		elif option == "prefix":
			if text == None:
				text = ctx.prefix
			await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": text}})
			await ctx.send(f"Succesfully changed the bot's prefix to {text}")
		elif option == "mod_log":
			text = text.lstrip("<#").strip(">")
			if self.bot.get_channel(int(text)):
				await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"mod_log": int(text)}})
				await ctx.send(f"Succesfully changed the mod log channel to <#{text}>")
			else:
				await ctx.send("That's not a valid channel. Please type the whole channel, not just the id or name.")
		else:
			await ctx.send("That's an invalid option. The current config option's are prefix, welcome_message, leave_message, welcome/leave_channel, and mod_log")

	@commands.command(aliases=["welcome/leave_channel"])
	@commands.has_permissions(manage_guild=True)
	async def welcome_leave_channel(self, ctx):
		"Enable or disable the custom welcome/leave message channel."
		server = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if not server:
			await self.bot.db.config.insert_one({"_id": ctx.guild.id, "channel": True})
			await ctx.send(f"Enabled the message channel, but no messages are set. Please set them with {ctx.prefix}config")
		elif server["channel"]:
			await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"channel": False}})
			await ctx.send("Disabled the message channel. To enable it again please run this command again")
		elif not server["channel"]:
			await self.bot.db.config.update_one({"_id": ctx.guild.id}, {"$set": {"channel": True}})
			await ctx.send("Enabled the message channel. To disable it again please run this command again")

def setup(bot):
	bot.add_cog(Config(bot))
