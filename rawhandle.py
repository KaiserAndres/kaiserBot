f = open("settings.txt", 'r')
botnick = (f.readline()).split(":")[1]
f.close()
def getCommand(text):
    '''
        Paramenters:
            text: String. Raw entry right out of the IRC protocol.

        Returns the command sent, which is the following:
            "!command <extra>"
    '''
    parts = text.split(":")
    return parts[len(parts)-1]

def gerUserName(text):
    '''
        Paramenters:
            text: String of data, raw command that comes from irc.

        Returns:
            Username
    '''
    parts = text.split(":")
    name = parts.split[1]("!")[0]
    return name

def getChannel(text, botnick):
    '''
        Paramenters:
            text: String of data, raw command that comes from irc.

        Returns: "#<CHANNEL NAME>"
        If the channel the message is sent to is the name of the bot (AKA it is a PM)
        Then Returns: "<Username>" where <Username> is the username of the user
        who PMd the bot
    '''
    parts = text.split(":")
    if (parts[len(parts)-2]).split(" ")[2] == botnick.upper():
        return getUserName(text)
    else:
        return ((parts[len(parts)-2]).split(" ")[2])

