from discord.ext import commands
from os import listdir
from constants import *


def get_prefix(clnt, message):
    session = sessions["bot_serversettings"]
    prefix = session.query(Prefix).filter(Prefix.server_id == message.guild.id).first()
    return prefix.prefix


client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")


@client.command()
async def load(ctx, extension):
    if ctx.author.id == AUTHOR_ID:
        client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog is loading...")
    else:
        await ctx.send("You're not the Developer...")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == AUTHOR_ID:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send("Cog is unloading...")
    else:
        await ctx.send("You're not the Developer...")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == AUTHOR_ID:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog is reloading...")
    else:
        await ctx.send("You're not the Developer...")


for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
