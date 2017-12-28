

import socket
import random
import roller
import rawhandle
import helper_functions as hf

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

botnick = settings['BotNick']
server = settings['Server'].split(":")
channel = settings['Channels'].split(",")
f.close()

user = "USER "+ botnick +" "+ botnick +" "+ botnick +" :This is the KaiserBot!\n"
nick = "NICK "+ botnick +"\n"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to:"+server[0])
irc.connect((server[0], int(server[1])))
irc.send(user.encode("utf-8"))
irc.send(nick.encode("utf-8"))
#irc.send("PRIVMSG nickserv :iNOOPE\r\n".encode("utf-8"))

while 1:
    text=irc.recv(2040)
    text = text.decode("utf-8").upper()
    try:
        print(text)
    except(UnicodeEncodeError):
        print("There was an invalid character here!")

    mess = rawhandle.Message(text, botnick)

    #---------------------------------------------------------------------------
    #   Joins the room after the MOTD has been fully recieved.
    #   Change to whatever your irc server sends at the end of MOTD.
    #---------------------------------------------------------------------------

    if text.find("End of /MOTD command.".upper()) != -1:
        for chans in channel:
            join = "JOIN "+chans + "\n"
            irc.send(join.encode("utf-8"))

    if text.find('PING') != -1:
        hf.ping_exec(irc, mess)

    #---------------------------------------------------------------------------
    #   This area is for all commands sent in via the irc
    #---------------------------------------------------------------------------

    if text.find("!ROLL") != -1:
        hf.roll_exec(irc, mess)

    if text.find("!JOIN") != -1:
        hf.join_exec(irc, mess)

    if text.find("!TAROT") != -1:
        hf.tarot_exec(irc, mess)

    if text.find("!HELP") != -1:
        '''
            Help command, displays a string with help info.
                * What the bot is
                * How to use the commands
                * Where do download the bot
        '''
        command = rawhandle.getCommand(text)
        if command[0] == "!":
            chann = rawhandle.getChannel(text, botnick)
            message = ("PRIVMSG "+chann+" :"+"Hello! I am KaiserBot, I am a "+
                       "tiny bot made my KaiserA, you can run the following "+
                       "commands on me: !roll, !join !help.!Roll uses the "+
                       "following parameters: !Roll <TIMES>#<AMOUNT OF "+
                       "DICE>d<MAX DIE>+<MOD> AMOUNT OF DIE and MAX DIE are "+
                       "obligatory.!Join takes the following parameters: !Join"+
                       " #<CHANNELNAME>. I am version 1.0 and I can be "+
                       "downloaded at the following adress: "+
                       "https://github.com/KaiserAndres/kaiserBot. "+
                       "I run on python 3.x so anyone who "+
                       "wants can host me!\r\n")
            irc.send(message.encode("utf-8"))

    if text.find("!LEAVE") != -1:
        command = rawhandle.getCommand(text)
        if command[0] == "!":
            chann = rawhandle.getChannel(text, botnick)
            if chann != channel:
                message = "PART "+chann+"\r\n"
                irc.send(message.encode("utf-8"))
