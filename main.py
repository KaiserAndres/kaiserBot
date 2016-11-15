import socket
import logging
import rawhandle

'''
Start execution of the bot daemon from here.
'''

settings = {}
commands = {}
logging.basicConfig(filename='bot.log', level=logging.DEBUG)


def main():
    load_config()
    server = connect()
    await_responce(server)
    join_rooms(server)
    while True:
        ping_back(server)
        run_commands(server)


def connect():
    user = "USER {} {} {}  :This is the KaiserBot!\n".format(settings['BotNick'], settings['BotNick'],
                                                             settings['BotNick']).encode('utf-8')
    nick = "NICK {} \n".format(settings['BotNick']).encode('utf-8')

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((settings["Server"], int(settings["Port"])))
        logging.info("Connecting to {}".format(settings["Server"]))
        server.send(user)
        server.send(nick)
        return server
    except socket.timeout:
        logging.error("Could not connect to {}: connection timed out.".format(settings["Server"]))


def load_config():
    f = open('settings.txt', 'r').read()
    for line in f.split("\n"):
        conf_name = line.split("|")[0]
        conf_data = line.split("|")[1]
        if "," in conf_data:
            conf_data.split(",")
        settings[conf_name] = conf_data


def await_responce(server):
    while "End of /MOTD command.".upper() not in server.recv(2048).decode('utf-8').upper():
        continue


def join_rooms(server):
    for room in settings["Channels"]:
        join_message = "JOIN {} \n".format(room).encode('utf-8')
        server.send(join_message)


def ping_back(server):
    current_text = receive_text()
    if "PING" in current_text:
        pong_code = current_text.split()[1]
        pong_message = "PONG {} \r\n".format(pong_code).encode('uft-8')
        server.send(pong_message)


def run_commands():
    current_text = rawhandle.getCommand(receive_text())
    if current_text.startswith("!"):
        cmd = current_text.split()[0].split("!")[1]
        args = " ".join(current_text.split[1:])
        commands[cmd](args)


def receive_text(server):
    return server.recv(2048).decode('utf-8').upper()


if __name__ == "__main__":
    main()
