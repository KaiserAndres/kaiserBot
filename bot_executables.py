import roller
import random
from startup import join

DEFAULT_CARD_AMOUNT = 1
MAX_CARDS = 15
CARD_SEPARATOR = "||"


def ping_exec(irc, message):
    pong = 'PONG ' + message.text.split(" ")[1] + '\r\n'
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
    for room in message.text.split():
        if room.startswith("#"):
            join(irc, room)


def tarot_exec(irc, message):
    '''
        Tarot command asks for the number of cards to be drawn and returns them.
        A tarot command has the following structure:
            !tarot <NUMBER OF CARDS>
    '''
    card_amount = get_card_amount(message)
    card_spread = spread_cards(card_amount)
    output_message = "You got these cards: " + CARD_SEPARATOR.join(card_spread)

    irc.send(message.reply(output_message))


def spread_cards(card_amount):
    card_spread = []
    local_deck = load_deck("deck")
    for time in range(0, card_amount):
        card_index = random.randint(0, len(local_deck) - 1)
        is_reversed = random.randint(0, 1) == 1

        card_text = local_deck[card_index]
        if is_reversed:
            card_text = card_text + "(reversed)"
        card_spread.append(card_text)

        local_deck.remove(local_deck[card_index])
    return card_spread


def get_card_amount(message):
    number_buffer = ""
    number_end = 9
    for characterIndex in range(0, len(message.text)):
        try:
            int(message.text[characterIndex])
            if characterIndex < number_end:
                number_buffer = number_buffer + message.text[characterIndex]
        except ValueError:
            continue
    try:
        card_amount = int(number_buffer)
    except ValueError:
        card_amount = DEFAULT_CARD_AMOUNT

    if card_amount > MAX_CARDS:
        card_amount = MAX_CARDS

    if card_amount <= 0:
        card_amount = 1

    return card_amount


def load_deck(deck_file_name):
    deck_file = open(deck_file_name, "r")
    deck_text = deck_file.readlines()
    deck = []
    deck_file.close()

    for card in deck_text:
        deck.append(card[:-1])
    return deck
