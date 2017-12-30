import socket
import logging
from rawhandle import Message
from bot_executables import ping_exec, join_exec, roll_exec, tarot_exec


logging.basicConfig(filename="bot.log", level=logging.DEBUG)

logging.info("Loading settings")


def load_config():
    config_dict = {}
    with open('settings.txt', 'r') as f:
        for line in f:
            if line[len(line) - 1] == "\n":
                line = line[:-1]
            split_line = line.split("|")
            config_dict[split_line[0]] = ",".join(split_line[1:])
        f.close()
    return config_dict


settings = load_config()

bot_nick = settings['BotNick']
ip, port = settings['Server'].split(":")
channel_list = settings['Channels'].split(",")


def connect(ip, port, bot_nick):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("Connecting to: " + ip)
    irc.connect((ip, int(port)))
    irc.send(("USER " + bot_nick + " " + bot_nick + " " + bot_nick + " :This is the KaiserBot!\n").encode("utf-8"))
    irc.send(("NICK " + bot_nick + "\n").encode("utf-8"))
    logging.info("Connection successful.")
    return irc


irc = connect(ip, port, bot_nick)


def log_failure(error, text):
    logging.error(error.__class__)
    logging.error(error.args)
    logging.error(error.message)
    logging.error(text)


while 1:
    text = irc.recv(2040)
    text = text.decode("utf-8").upper()
    try:
        logging.debug(text)
    except UnicodeEncodeError:
        logging.error("There was an invalid character here!")

    try:
        mess = Message(text, bot_nick)
    except Exception as inst:
        log_failure(inst, text)
        continue

    try:
        if text.find("End of /MOTD command.".upper()) != -1:
            logging.info("Connection established, joining channels.")
            for channel in channel_list:
                logging.debug("Joining " + channel)
                join = "JOIN " + channel + "\n"
                irc.send(join.encode("utf-8"))

        if mess.text.startswith('PING'):
            logging.debug("Sending PONG message.")
            ping_exec(irc, mess)

        if mess.text.startswith("!ROLL"):
            roll_exec(irc, mess)

        if mess.text.startswith("!JOIN"):
            join_exec(irc, mess)

        if mess.text.startswith("!TAROT"):
            tarot_exec(irc, mess)

        if mess.text.startswith("!HELP"):
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
                irc.send(mess.reply(help_string))

        if mess.text.startswith("!LEAVE"):
            if mess.text[0] == "!":
                if mess.channel != channel_list[0]:
                    message = "PART " + mess.channel + "\r\n"
                    irc.send(message.encode("utf-8"))

    except Exception as inst:
        log_failure(inst, mess.raw)
        continue
