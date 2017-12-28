import roller
import random

DEFAULT_CARD_AMOUNT = 1
MAX_CARDS = 15


def ping_exec(irc, message):
    pong = 'PONG ' + message.text.split()[0] + '\r\n'
    irc.send(pong.encode("utf-8"))


def roll_exec(irc, message):
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

    if message.text[0] == "!":
        diceNumbers = roller.getRolledNumbers(message.text)
        messageToSend = ''

        # -------------------------------------------------------------------
        #   Hard limits on the dice sizes
        # -------------------------------------------------------------------

        if diceNumbers[0] > 10:
            diceNumbers[0] = 10

        if diceNumbers[0] < 1:
            diceNumbers[0] = 1

        if diceNumbers[1] > 2000:
            diceNumbers[1] = 2000

        if diceNumbers[1] < 1:
            diceNumbers[1] = 1

        if diceNumbers[2] < 1:
            diceNumbers[2] = 1
        rolledArray = roller.roll(diceNumbers[0],
                                  diceNumbers[1],
                                  diceNumbers[2])

        for rollNum in rolledArray:
            # REMINDER: make a message maker function cause this is ugly!
            if (diceNumbers[3] == 0):
                messageToSend = (messageToSend +
                                 "\x0312,15(" + str(diceNumbers[1]) +
                                 "d" + str(diceNumbers[2]) + ") \x032,15[" +
                                 str(rollNum) + "]\x031,15 : \x034,15{" +
                                 str(rollNum + diceNumbers[3]) + "} ")
            else:
                messageToSend = (messageToSend + "\x0312,15(" +
                                 str(diceNumbers[1]) + "d" +
                                 str(diceNumbers[2]) + "+" +
                                 str(diceNumbers[3]) + ") \x032,15[" +
                                 str(rollNum) + "+" +
                                 str(diceNumbers[3]) +
                                 "]\x031,15 : \x034,15{" +
                                 str(rollNum + diceNumbers[3]) + "} ")

        irc.send(message.reply(messageToSend))


def join_exec(irc, message):
    '''
    A join command has the following structure:
        !JOIN #CHANNEL 
    A message is sent to the irc server requesting to join #CHANNEL
    '''
    if message.text[0] == "!":
        chann = ""
        foundLink = False
        for char in message.text:
            if char == "#":
                foundLink = True
            if foundLink:
                chann = chann + char
        if chann != "":
            join_message = "JOIN "+ chann +"\n"
            irc.send(join_message.encode("utf-8"))
        else:
            irc.send(message.reply("Error 02: bad channel."))


def tarot_exec(irc, message):
    if message.text[0] == "!":
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
        localDeck = load_deck("deck")
        numberBuffer = ""
        numberEnd = 9

        # Gets the number from the command, should update soon.

        for characterIndex in range(0, len(message.text)):
            try:
                int(message.text[characterIndex])
                if characterIndex < numberEnd:
                    numberBuffer = numberBuffer + message.text[characterIndex]
            except ValueError:
                continue

        # In case of no number given it uses the default of one.

        try:
            amountOfCards = int(numberBuffer)
        except ValueError:
            amountOfCards = DEFAULT_CARD_AMOUNT

        cardsSpreaded = []

        # If the amount of cards it's too big the amount is set to 15
        # This is due to a limitation on the amount of data the irc will
        # Display.

        if amountOfCards > MAX_CARDS:
            amountOfCards = MAX_CARDS

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
            # Eliminates the card from the deck so it doesn't come twice
            localDeck.remove(localDeck[cardIndex])

        messageToSend = "You got these cards: "

        for card in cardsSpreaded:
            messageToSend = messageToSend + card

        # TODO: Make a message sender function some day.
        irc.send(message.reply(messageToSend))


def load_deck(deck_file_name):
    deck_file = open(deck_file_name, "r")
    deck_text = deck_file.readlines()
    deck = []
    deck_file.close()

    for card in deck_text:
        deck.append(card[:-1])
    return deck
