import discord
from discord.ext import commands
import time
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import io
import traceback
from contextlib import redirect_stdout
import textwrap
import inspect
import aiohttp

async def get_prefix(bot, message):
    server = await bot.db.config.find_one({"_id": message.guild.id})
    if not server or "prefix" not in server:
        if bot.user.id == 473943707213889568:
            return "test."
        elif bot.user.id == 473565271106256896:
            return "~"
    else:
        return server["prefix"]
#got the Token this way because Python was being stupid and wouldn't import another file and I was too lazy to figure it out XD
bot = commands.Bot(command_prefix=get_prefix)
bot._last_result = None

cogs = {"fun", "ranks", "config", "mod"}

@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: The Programming Discord :D')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    mongo = AsyncIOMotorClient(os.environ.get("mongo"))
    bot.db = mongo.programmingdiscordbot
    bot.session = aiohttp.ClientSession(loop=bot.loop)

def is_owner():
    return commands.check(lambda ctx: ctx.author.id == 300396755193954306)




#Welcome and leave message handling
@bot.event
async def on_member_join(member):
    server = await bot.db.config.find_one({"_id": member.guild.id})
    if not server:
        pass
    elif server["channel"]:
        channel = bot.get_channel(server["welcome/leave_channel"])
        message = server["welcome_message"]
        formatting = {"server_name": member.guild.name, "member_count": len(member.guild.members), "member_name": member.name, "member_mention": member.mention}
        for x in formatting:
            if x in message:
                message = message.replace(x, str(formatting[x]))
        await channel.send(message)

@bot.event
async def on_member_remove(member):
    server = await bot.db.config.find_one({"_id": member.guild.id})
    if not server:
        pass
    elif server["channel"]:
        channel = bot.get_channel(server["welcome/leave_channel"])
        message = server["leave_message"]
        formatting = {"server_name": member.guild.name, "member_count": len(member.guild.members), "member_name": member.name, "member_mention": member.mention}
        for x in formatting:
            if x in message:
                message = message.replace(x, str(formatting[x]))
        await channel.send(message)

#Error handling
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"`Usage: {ctx.prefix + ctx.command.signature}`")
        print('Sent command help')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("That command is disabled.")
        print('Command disabled.')
    elif isinstance(error, commands.NotOwner):
        await ctx.send("You have to be a dev to use this command!")
        print("Attemepted dev command by non-dev")

@bot.command()
async def ping(ctx):
    t1 = time.perf_counter()
    message = await ctx.send("Checking ping...")
    t2 = time.perf_counter()
    ping = round((t2-t1)*1000)
    await message.edit(content=f":ping_pong: Pong! `{ping}`ms")

def paginate(text: str):
    '''Simple generator that paginates text.'''
    last = 0
    pages = []
    for curr in range(0, len(text)):
        if curr % 1980 == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr
    if appd_index != len(text) - 1:
        pages.append(text[last:curr])
    return list(filter(lambda a: a != '', pages))

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')



@bot.command(name='eval', hidden=True)
async def _eval(ctx, *, body):
    """Evaluates python code"""
    user = await bot.db.trusted.find_one({"_id": ctx.author.id})
    if user:
        env = {
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': bot._last_result,
            'source': inspect.getsource
        }

        env.update(globals())
        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None
        to_compile = f'async def func(): \n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                bot._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')
    else:
        await ctx.send("You aren't a trusted user")

@bot.command()
@is_owner()
async def add_trusted(ctx, user: discord.Member):
    x = await bot.db.trusted.find_one({"_id": user.id})
    if not x:
        await bot.db.trusted.insert_one({"_id": user.id, "name": f"{user.name}#{user.discriminator}"})
        await ctx.send(f"Added {user.name}#{user.discriminator} to the trusted users")
    else:
        await ctx.send('That user is already trusted')

@bot.command()
@is_owner()
async def remove_trusted(ctx, user: discord.Member):
    x = await bot.db.trusted.find_one({"_id": user.id})
    if x:
        await bot.db.trusted.delete_many({"name": f"{user.name}#{user.discriminator}"})
        await ctx.send(f"Removed {user.name}#{user.discriminator} from the trusted users")
    else:
        await ctx.send('That user is not even trusted.')


if __name__ == "__main__":
    for extension in cogs:
        try:
            bot.load_extension(f"cogs.{extension}")
            print('Loaded: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error on load: {}\n{}'.format(extension, exc))

	
bot.run(os.environ.get("TOKEN"))
