'''
    Title: Basic IRC bot
    Last edit: 16:05 11/01/2016 (GMT -3)
    Version: 1.0

    Description:
        This is a raw irc input handle library. It's main purpose is to facaili-
        te the working with raw irc protocol. Most functions will take a text 
        variable that represents one like of full raw irc uotput. The normal
        format for this is the following:

        :<USERNAME>!<HOST>:<IP> <COMMAND>

    Functions:
        getCommand()
        getUserName()
        getChannel()
'''


class Message:

    def __init__(self, text, bot_nick):
        self.nick = bot_nick
        self.raw = text

        if not contains(text, "PRIVMSG"):
            self.userName = ""
            self.channel = ""
            self.text = text
            return

        self.userName = get_user_name(text)
        self.text = get_command(text)
        self.channel = get_channel(text, self.nick)

    def reply(self, text):
        return ("PRIVMSG " + self.channel + " :" + text + "\r\n").encode("utf-8")


def contains(text, content):
    return text.find(content) != -1


def get_command(text):
    '''
        Paramenters:
            text: String. Raw entry right out of the IRC protocol.

        Returns the command sent, which is the following:
            "!command <extra>"
    '''
    parts = text.split(":")
    return parts[len(parts)-1]


def get_user_name(text):
    '''
        Paramenters:
            text: String of data, raw command that comes from irc.

        Returns:
            Username
    '''
    parts = text.split(":")
    name = parts[1].split("!")[0]
    return name


def get_channel(text, bot_nick):
    '''
        Paramenters:
            text: String of data, raw command that comes from irc.

        Returns: "#<CHANNEL NAME>"
        If the channel the message is sent to is the name of the bot (AKA it is a PM)
        Then Returns: "<Username>" where <Username> is the username of the user
        who PMd the bot
    '''
    channel = ""
    sub_sections = text.split(":")
    for section in sub_sections:
        if contains(section, "PRIVMSG"):
            temp_var = section
    for word in temp_var.split(" "):
        if contains(word, "#"):
            channel = word
        if word == bot_nick:
            channel = get_user_name(text)

    if channel == "":
        raise Exception("No channel found")
    return channel
    #temp_var = sub_sections[len(sub_sections)-2]
    if len(sub_sections) < 3:
        return "no channel"
    if temp_var == bot_nick.upper():
        return get_user_name(text)
    else:
        return temp_var.split(" ")[2]
