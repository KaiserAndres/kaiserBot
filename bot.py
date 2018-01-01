import logging
from startup import load_config, connect, log_failure
from rawhandle import Message
from bot_executables import ping_exec, join_exec, roll_exec, tarot_exec


version = "1.6"

logging.basicConfig(filename="bot.log",
                    format="%(asctime)s - %(levelname)s : %(message)s",
                    level=logging.DEBUG if version.endswith("a") else logging.INFO)
logging.info("Loading settings")
settings = load_config()
bot_nick = settings['BotNick']
ip, port = settings['Server'].split(":")
channel_list = settings['Channels'].split(",")
irc = connect(ip, port, bot_nick)

while 1:
    text = irc.recv(2040)
    text = text.decode("utf-8").upper()

    if not text:
        logging.error("Connection died, attempting reconnecting:")
        irc = connect(ip, port, bot_nick)

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
            if mess.channel != settings["DefaultChannel"].upper():
                logging.info("Leaving channel " + mess.channel + ": " + mess.userName + " sent the command.")
                message = "PART " + mess.channel + "\r\n"
                irc.send(message.encode("utf-8"))

    except Exception as inst:
        log_failure(inst, mess.raw)
        continue
