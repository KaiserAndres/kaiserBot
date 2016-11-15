import random

def roll(pararelRolls, diceAmmount, diceSize):
    rolledArray = []
    for time in range(0, pararelRolls):
        rollSum = 0
        for time in range(0, diceAmmount):
            roll = random.randint(1, diceSize)
            rollSum = rollSum + roll
        rolledArray.append(rollSum)
    return rolledArray

def getRolledNumbers(command, isIrc = True):
    '''
        parameters:
            command: String with the following format:
                !roll a#xdy+z
        Returns an array where the indexes give:
            0: pararelRolls -> default: 1
            1: diceAmmount  -> default: 1
            2: diceSize     -> default: 20
            3: modifier     -> default: 0
    '''
    rollNumbers = [1, 1, 20, 0]
    if isIrc:
        try:
            numbers = command.split()[1] #Will always be 1 because of space locations.
        except:
            numbers = ''
    if not isIrc:
        numbers = command
    if numbers.find("#") != -1:
        try:
            rollNumbers[0] = int(numbers.split("#")[0])
        except:
            rollNumbers[0] = 1
        numbers = numbers.split("#")[1]
    if numbers.find("D") != -1:
        try:
            rollNumbers[1] = int(numbers.split("D")[0])
        except:
            rollNumbers[1] = 1
        try:
            rollNumbers[2] = int(numbers.split("D")[1])
        except:
            rollNumbers[2] = 20
        numbers = numbers.split("D")[1]
    if numbers.find("+") != -1:
        try:
            rollNumbers[2] = int(numbers.split("+")[0])
        except:
            rollNumbers[2] = 20
        try:    
            rollNumbers[3] = int(numbers.split("+")[1])
        except:
            rollNumbers[3] = 0
        numbers = ""
    if numbers.find("-") != -1:
        try:
            rollNumbers[2] = int(numbers.split("-")[0])
        except:
            rollNumbers[2]
        try:
            rollNumbers[3] = int(numbers.split("-")[1])*(-1)
        except:
            rollNumbers[3] = 0
        numbers = ""
    if rollNumbers[0] > 100:
        rollNumbers[0] = 100
    if rollNumbers[1] > 100:
        rollNumbers[1] = 100 
    return rollNumbers
