import discord
from discord.ext import commands

class Mod():
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
	@commands.has_permisions(ban_members=True)
	async def ban(self, ctx, user, *, reason=None)
		mod_log = await self.bot.db.config.find_one({"_id": ctx.guild.id})
		if user.startswith("<@") and user.endswith(">"):
			user = ctx.guild.get_member(int(user.lstrip("<@").strip(">")))
		else:
			user = ctx.guild.get_member(int(user))
		try:
			await user.ban(reason=reason)
		except: discord.Forbidden(
			await ctx.send("I don't have the proper permissions to ban this member")
		await ctx.send(f"**{user} was banned**")
		if mod_log["mod_log"]:
			channel = self.bot.get_channel(mod_log["mod_log"])
			embed = discord.Embed(title="Member banned!", color=discord.Color.red(), description=f"{user} was banned by {ctx.author}")
			embed.add_field(name="Reason", value=reason)
			embed.set_image(url=user.avatar_url)
			await channel.send(embed=embed)




def setup(bot):
	bot.add_cog(Mod(bot))