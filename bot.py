'''
    Title: Basic IRC bot
    Author: Andrés Villagra de la Fuente
    Creation date: 23:11 28/12/2015 (GMT-3)
    Last edit: 16:14 29/12/2015 (GMT-3)
    Version: 1.1

    Description:
        This is a simple IRC bot made to work whenever the normal bot collapses
    also to perform other sort of stuff such as a personal archive for me cause
    I really never set that up.

    Finished features:
        * Rolling
        * Joining channels
        * Tarot spreading
    '''

import socket
import sys
import random
import roller
import rawhandle

def makeDeck(deck):
    '''
        Paramenters:
            deck: string of the location fo the file with the cards saved
                as a line each.

        Returns a deck array containing the cards located in the file deck.
    '''
    deckFile = open(deck, "r")
    baseDeck = deckFile.readlines()
    for index in range(0, len(baseDeck)):
        baseDeck[index] = baseDeck[index][:-1]
    return baseDeck
    deckFile.close()


settings = {}
with open('settings.txt','r') as f:
	for line in f:
		if line[len(line)-1] == "\n":
			line = line[:-1]
		splitLine = line.split("|")
		settings[splitLine[0]] = ",".join(splitLine[1:])

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
irc.send("PRIVMSG nickserv :iNOOPE\r\n".encode("utf-8"))

while 1:
    text=irc.recv(2040)
    text = text.decode("utf-8").upper()
    print(text)

    if text.find("End of /MOTD command.".upper()) != -1:
        for chans in channel:
            join = "JOIN "+chans + "\n"
            irc.send(join.encode("utf-8"))


    if text.find('PING') != -1:
        pong = 'PONG ' + text.split() [1] + '\r\n'
        irc.send(pong.encode("utf-8"))

    # All checking code goes here
    if text.find("!ROLL") != -1:
        '''
            A !roll comand has the following structure:
                !roll diceAmount+d+diceSize+"+"+modifier

            * Dice amount is an integer up to 20000
            * Dice Size is an integer
            * Modifier is an integer that is added onto the roll after

            The !Roll command can also have this structure:
                !!roll d+diceAmount+d+diceSize+"+"+modifier

            * Dice amount is the result of a roll of said size and then proceeds
                to roll that many of the following dice
            * Dice Size is an integer
            * Modifier is an integer that is added onto the roll after            
        '''

        command = rawhandle.getCommand(text)
        if command[0] == "!":
            chann = rawhandle.getChannel(text, botnick)
            diceNumbers = roller.getRolledNumbers(command)
            messageToSend = ''

            if diceNumbers[0] > 10:
                diceNumbers[0] = 10
            
            if diceNumbers[1] > 2000:
                diceNumbers[1] = 2000

            rolledArray = roller.roll(diceNumbers[0], diceNumbers[1], diceNumbers[2])

            for rollNum in rolledArray:
                if(diceNumbers[3] == 0):
                    messageToSend = messageToSend + "\x0312,15("+str(diceNumbers[1])+"d"+str(diceNumbers[2])+") \x032,15["+str(rollNum)+"]\x031,15 : \x034,15{"+str(rollNum+diceNumbers[3])+"} "
                else:
                    messageToSend = messageToSend + "\x0312,15("+str(diceNumbers[1])+"d"+str(diceNumbers[2])+"+"+str(diceNumbers[3])+") \x032,15["+str(rollNum)+"+"+str(diceNumbers[3])+"]\x031,15 : \x034,15{"+str(rollNum+diceNumbers[3])+"} "
            message = "PRIVMSG "+chann+" :"+messageToSend+"\r\n"
            irc.send(message.encode("utf-8"))

    if text.find("!JOIN") != -1 :
        '''
            A join command has the following structure:
                !JOIN #CHANNEL 
            A message is sent to the irc server requesting to join #CHANNEL
        '''
        command = rawhandle.getCommand(text)
        if command[0] == "!":
            chann = ""
            foundLink = False
            for char in command:
                if char == "#":
                    foundLink = True
                if foundLink:
                    chann = chann + char
            if chann != "":
                joinMessage = "JOIN "+ chann +"\n"        
                irc.send(joinMessage.encode("utf-8"))
            else:
                chann = rawhandle.getChannel(text, botnick)
                message = "PRIVMSG "+chann+" :"+"Error 02: bad channel."+"\r\n"
                irc.send(message.encode("utf-8"))

    if text.find("!TAROT") != -1:
        command = rawhandle.getCommand(text)
        if command[0] == "!" and text.find("PRIVMSG") != -1:
            '''
                Tarot command asks for the number of cards to be drawed and returns them.
                A tarot command has the following structure:
                    !tarot <NUMBER OF CARDS>
                Thre are 5 types:
                    * Major arcana
                    * Swords
                    * Wands
                    * Pentacles
                    * Cups
                The minor arcana have the following cards:
                    * 1
                    * 2
                    * 3
                    * 4
                    * 5
                    * 6
                    * 7
                    * 8
                    * 9
                    * 10
                    * page
                    * queen
                    * king
                Major arcana have 22 cards.
            '''
            localDeck = makeDeck("deck")
            numberBuffer = ""
            numberEnd = 9

            for characterIndex in range(0, len(command)):
                try:
                    int(command[characterIndex])
                    if characterIndex < numberEnd:
                        numberBuffer = numberBuffer + command[characterIndex]
                except ValueError:
                    continue

            try:
                amountOfCards = int(numberBuffer)
            except ValueError:
                amountOfCards = 1

            cardsSpreaded = []

            if amountOfCards > 15:
                amountOfCards = 15

            for time in range(0, amountOfCards):
                cardIndex = random.randint(0, len(localDeck)-1)
                reversedOrNot = random.randint(0,1)
                if reversedOrNot == 1:
                    if time != 0:
                        cardsSpreaded.append("||"+localDeck[cardIndex]+"(reversed)")
                    else:
                        cardsSpreaded.append(localDeck[cardIndex]+"(reversed)")

                elif reversedOrNot != 1:
                    if time != 0:
                        cardsSpreaded.append("||"+localDeck[cardIndex])
                    else:
                        cardsSpreaded.append(localDeck[cardIndex])
                localDeck.remove(localDeck[cardIndex]) # Eliminates the card from the deck so it doesn't come twice

            chann = rawhandle.getChannel(text, botnick)
            messageToSend = "You got these cards: "

            for card in cardsSpreaded:
                messageToSend = messageToSend + card

            message = "PRIVMSG "+chann+" :"+messageToSend+"\r\n"
            irc.send(message.encode("utf-8"))

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
            message = "PRIVMSG "+chann+" :"+"Hello! I am KaiserBot, I am a tiny bot made my KaiserA, you can run the following commands on me: !roll, !join !help.!Roll uses the following parameters: !Roll <TIMES>#<AMOUNT OF DICE>d<MAX DIE>+<MOD> AMOUNT OF DIE and MAX DIE are obligatory.!Join takes the following parameters: !Join #<CHANNELNAME>. I am version 1.0 and I can be downloaded at the following adress: https://github.com/KaiserAndres/kaiserBot. I run on python 3.x so anyone who wants can host me!\r\n"
            irc.send(message.encode("utf-8"))

    if text.find("!LEAVE") != -1:
        command = rawhandle.getCommand(text)
        if command[0] == "!":
            chann = rawhandle.getChannel(text)
            if chann != channel:
                message = "PART "+chann+"\r\n"
                irc.send(message.encode("utf-8"))
