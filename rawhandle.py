def getCommand(text):
    '''
        Paramenters:
            text: String. Raw entry right out of the IRC protocol.

        Returns the command sent, which is the following:
            "!command <extra>"
    '''
    parts = text.split(":")
    return parts[len(parts)-1]

def getChannel(text):
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
        return((parts[len(parts)-2]).split(" ")[0].split("!")[0])
    else:
        return ((parts[len(parts)-2]).split(" ")[2])
