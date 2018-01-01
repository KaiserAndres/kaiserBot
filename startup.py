import socket
import logging


def connect(ip, port, bot_nick):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("Connecting to: " + ip)
    irc.connect((ip, int(port)))
    irc.send(("USER " + bot_nick + " " + bot_nick + " " + bot_nick + " :This is the KaiserBot!\n").encode("utf-8"))
    irc.send(("NICK " + bot_nick + "\n").encode("utf-8"))
    logging.info("Connection successful.")
    return irc


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


def log_failure(error, text):
    logging.exception("Found an exeption while executing: ")
    logging.error(text)


def join(irc, room):
    logging.info("Joining " + room)
    irc.send(("JOIN " + room + "\n").encode("utf-8"))
