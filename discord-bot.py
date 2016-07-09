import discord
from discord.ext import commands
import roller

description = "A test bot"

client = commands.Bot(command_prefix='!', description=description)

#-------------------------------------------------------------------------------
#
#   Settings loader
#
#-------------------------------------------------------------------------------
#   Loads the settings from the settings.txt file and loads them in the settings
#   dictionary.
#-------------------------------------------------------------------------------

settings = {}
with open('settings.txt','r') as f:
  for line in f:
    if line[len(line)-1] == "\n":
      line = line[:-1]
    splitLine = line.split("|")
    settings[splitLine[0]] = ",".join(splitLine[1:])

#-------------------------------------------------------------------------------

@client.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await client.say(left + right)

@client.command()
async def info():
  message = "I am a small bot that rolls, more functionality comming soon!"
  await client.say(message)

@client.command()
async def roll(text : str):
  messageToSend = ""
  diceNumbers = roller.getRolledNumbers(text.upper(), False)
  results = roller.roll(diceNumbers[0], diceNumbers[1], diceNumbers[2])

  for rollNum in results:
    if(diceNumbers[3] == 0):
        messageToSend = (messageToSend + 
                        "("+str(diceNumbers[1])+
                        "d"+str(diceNumbers[2])+") ["+
                        str(rollNum)+"] : {"+
                        str(rollNum+diceNumbers[3])+"} \n")
    else:
        messageToSend = (messageToSend + "("+
                         str(diceNumbers[1])+"d"+
                         str(diceNumbers[2])+"+"+
                         str(diceNumbers[3])+") ["+
                         str(rollNum)+"+"+
                         str(diceNumbers[3])+
                         "] : {"+
                         str(rollNum+diceNumbers[3])+"} \n")
  await client.say(messageToSend)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(settings["Mail"], settings["Pass"])