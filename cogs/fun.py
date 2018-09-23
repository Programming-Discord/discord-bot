import discord
from discord.ext import commands
import aiohttp
import random
import asyncio

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
		
	async def on_message(self, message):
		if "alexa play despacito" in message.content:
			lyrics = ["Ay, ¡Fonsi! ¡D.Y.!\nOhhh, oh, no, oh, no, oh'\nHey, yeah!\nDididiri Daddy, go!", 
				  "Sí, sabes que ya llevo un rato mirándote\nTengo que bailar contigo hoy\n(¡D.Y.!) Vi que tu mirada ya estaba llamándome\nMuéstrame el camino que yo voy", 
				  "¡Oh!\nTú, tú eres el imán y yo soy el metal\nMe voy acercando y voy armando el plan\nSólo con pensarlo se acelera el pulso (oh, yeah!)\nYa, ya me está gustando más de lo normal\nTodos mis sentidos van pidiendo más\nEsto hay que tomarlo sin ningún apuro", 
				  "**DES PA CITO**", 
				  "Quiero respirar tu cuello despacito\nDeja que te diga cosas al oído\nPara que te acuerdes si no estás conmigo", 
				  "**DES PA CITO**", 
				  "Quiero desnudarte a besos despacito\nFirmo en las paredes de tu laberinto\nY hacer de tu cuerpo todo un manuscrito\n(Sube, sube, sube, Sube, sube)"]
			await message.channel.send("`Now Playing: Luis Fonsi - Despacito ft. Daddy Yankee ⚪────────────── ◄◄⠀▶⠀►►⠀ 00:00 / 4:42 ⠀ ───○ 🔊⚙️`")
			for line in lyrics:
				await asyncio.sleep(4)
				await message.channel.send(line)
		

def setup(bot):
	bot.add_cog(Fun(bot))
