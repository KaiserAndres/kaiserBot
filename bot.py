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

def getCommand(text):
    '''
        Paramenters:
            text: String. Raw entry right out of the IRC protocol.

        Returns the command sent, which is the following:
            "!command <extra>"
    '''
    parts = text.split(":")
    return parts[len(parts)-1]

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

def canRoll(irc, channel):
    '''
        Paramenters:
            channel: string with the following format:
                #<CHANNEL_NAME>
            irc: connection socket.
        Returns:
            Boolean. True if can roll, false if not.
            Come one guys it's straight forward.
    '''
    irc.send(("NAMES "+channel+"\r\n").encode("utf-8"))
    if irc.recv(2040).decode("utf-8").find("Tyche[Dice]") != -1:
        Roll = False
    else:
        Roll = True
    irc.recv(2040)
    return Roll


server = "irc.esper.net"
channel = "#RPGStuck"
botnick = "KaiserBot"

user = "USER "+ botnick +" "+ botnick +" "+ botnick +" :This is the KaiserBot!\n"
nick = "NICK "+ botnick +"\n"
join = "JOIN "+ channel +"\n"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to:"+server)
irc.connect((server, 6667))
irc.send(user.encode("utf-8"))
irc.send(nick.encode("utf-8"))
irc.send("PRIVMSG nickserv :iNOOPE\r\n".encode("utf-8"))

while 1:
    text=irc.recv(2040)
    text = text.decode("utf-8").upper()
    print(text)

    if text.find("End of /MOTD command.".upper()) != -1:
        irc.send(join.encode("utf-8"))      #Used to join the channel, this is specific to
                                            #esper, stupid motd...


    if text.find('PING') != -1:
        pong = 'PONG ' + text.split() [1] + '\r\n'
        irc.send(pong.encode("utf-8"))

    # All checking code goes here
    if text.find("!ROLL") != -1:
        '''
            A !roll comand has the following structure:
                !roll diceAmount+d+diceSize+"+"+modifier

            * Dice amount is an integer up to 99
            * Dice Size is an integer up to 999
            * Modifier is an integer up to 99 that is added onto the roll after

            The !Roll command can also have this structure:
                !!roll d+diceAmount+d+diceSize+"+"+modifier

            * Dice amount is the result of a roll of said size and then proceeds
                to roll that many of the following dice
            * Dice Size is an integer up o 999
            * Modifier is an integer up to 99 that is added onto the roll after            
        '''

        command = getCommand(text)
        if command[0] == "!":
            chann = (text.split(":")[1]).split(" ")[2]
            if canRoll(irc, chann):
                diceNumbers = [0,0,0,1] # First element the amount of dice
                                        # Second element is the dice size
                                        # Third element is the modifier
                                        # Fourth is time rolled (hash)
                middleDFlag = False
                plusFlag = False
                hashFlag = False
                numberInCommand = "" # Buffer for the number
                messageToSend = ""
                command = command + " "
                for index in range(0, len(command)):

                    # Separates the values

                    if command[index] == "#":
                        diceNumbers[3] = int(numberInCommand)
                        numberInCommand = ""
                        continue

                    if command[index] == "D":
                        diceNumbers[0] = int(numberInCommand)
                        numberInCommand = ""
                        middleDFlag = True
                        continue               

                    if (command[index] == "+" or command[index+1] == " ") and middleDFlag and not plusFlag:
                        diceNumbers[1] = int(numberInCommand)
                        numberInCommand = ""
                        if command[index] == "+":
                            plusFlag = True
                            continue
                        if command[index+1] == " ":
                            break

                    if command[index+1] == " " and plusFlag:
                        diceNumbers[2] = int(numberInCommand)
                        numberInCommand = ""
                        break

                    try:
                        int(command[index])
                        numberInCommand = numberInCommand + command[index] #Makes a number from the string
                    except ValueError:
                        continue 

                if diceNumbers[0] > 20000:
                    diceNumbers[0] = 20000
                
                if diceNumbers[3] > 10:
                    diceNumbers[3] = 10

                rolledArray = []
                for time in range(0, diceNumbers[3]):
                    rollSum = 0
                    for time in range(0, diceNumbers[0]):
                        roll = random.randint(1, diceNumbers[1])
                        rollSum = rollSum + roll
                    rolledArray.append(rollSum)

                for roll in rolledArray:
                    messageToSend = messageToSend + "("+str(diceNumbers[0])+"d"+str(diceNumbers[1])+"+"+str(diceNumbers[2])+") = ["+str(roll)+"+"+str(diceNumbers[2])+"] ==> {"+str(roll+diceNumbers[2])+"}. "
                message = "PRIVMSG "+chann+" :"+messageToSend+"\r\n"
                irc.send(message.encode("utf-8"))
                print(text)

    if text.find("!JOIN") != -1 :
        '''
            A join command has the following structure:
                !JOIN #CHANNEL 
            A message is sent to the irc server requesting to join #CHANNEL
        '''
        command = getCommand(text)
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
                chann = (text.split(":")[1]).split(" ")[2]
                message = "PRIVMSG "+chann+" :"+"Error 02: bad channel."+"\r\n"
                irc.send(message.encode("utf-8"))

    if text.find("!TAROT") != -1:
        command = getCommand(text)
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

            chann = (text.split(":")[1]).split(" ")[2]
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
        command = getCommand(text)
        if command[0] == "!":
            chann = (text.split(":")[1]).split(" ")[2]
            message = "PRIVMSG "+chann+" :"+"Hello! I am KaiserBot, I am a tiny bot made my KaiserA, you can run the following commands on me: !roll, !join !help.!Roll uses the following parameters: !Roll <TIMES>#<AMOUNT OF DICE>d<MAX DIE>+<MOD> AMOUNT OF DIE and MAX DIE are obligatory.!Join takes the following parameters: !Join #<CHANNELNAME>. I am version 1.0 and I can be downloaded at the following adress: https://github.com/KaiserAndres/kaiserBot. I run on python 3.x so anyone who wants can host me!\r\n"
            irc.send(message.encode("utf-8"))
