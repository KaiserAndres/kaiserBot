import socket
import rawhandle
import helper_functions as hf

settings = {}
with open('settings.txt', 'r') as f:
    for line in f:
        if line[len(line)-1] == "\n":
            line = line[:-1]
        splitLine = line.split("|")
        settings[splitLine[0]] = ",".join(splitLine[1:])

bot_nick = settings['BotNick']
server = settings['Server'].split(":")
channel_list = settings['Channels'].split(",")
f.close()

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to:" + server[0])
irc.connect((server[0], int(server[1])))
irc.send(("USER " + bot_nick + " " + bot_nick + " " + bot_nick + " :This is the KaiserBot!\n").encode("utf-8"))
irc.send(("NICK " + bot_nick + "\n").encode("utf-8"))

while 1:
    text = irc.recv(2040)
    text = text.decode("utf-8").upper()
    try:
        print(text)
    except UnicodeEncodeError:
        print("There was an invalid character here!")

    mess = rawhandle.Message(text, bot_nick)

    if text.find("End of /MOTD command.".upper()) != -1:
        for channel in channel_list:
            join = "JOIN " + channel + "\n"
            irc.send(join.encode("utf-8"))

    if text.find('PING') != -1:
        hf.ping_exec(irc, mess)

    if text.find("!ROLL") != -1:
        hf.roll_exec(irc, mess)

    if text.find("!JOIN") != -1:
        hf.join_exec(irc, mess)

    if text.find("!TAROT") != -1:
        hf.tarot_exec(irc, mess)

    if text.find("!HELP") != -1:
        if mess.text[0] == "!":
            help_string = ("Hello! I am KaiserBot, I am a " +
                            "tiny bot made my KaiserA, you can run the following " +
                            "commands on me: !roll, !join !help.!Roll uses the " +
                            "following parameters: !Roll <TIMES>#<AMOUNT OF " +
                            "DICE>d<MAX DIE>+<MOD> AMOUNT OF DIE and MAX DIE are " +
                            "obligatory.!Join takes the following parameters: !Join" +
                            " #<CHANNELNAME>. I am version 1.0 and I can be " +
                            "downloaded at the following address: " +
                            "https://github.com/KaiserAndres/kaiserBot. " +
                            "I run on python 3.x so anyone who " +
                            "wants can host me!\r\n")
            irc.send(mess.reply(help_string).encode("utf-8"))

    if text.find("!LEAVE") != -1:
        if mess.text[0] == "!":
            if mess.channel != channel_list[0]:
                message = "PART " + mess.channel + "\r\n"
                irc.send(message.encode("utf-8"))
