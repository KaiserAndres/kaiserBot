import discord
from discord.ext import commands

description = "A test bot"

client = commands.Bot(command_prefix='!', description=description)

@client.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await client.say(left + right)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run("email", 'pass')