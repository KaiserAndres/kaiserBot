import unittest
from bot_executables import *
from rawhandle import Message

BOT_NICK = "test_bot"


class MockIrc():
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)


def build_join_command(rooms):
    return ":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!JOIN " + " ".join(rooms)


def build_join_message(message_string):
    return Message(message_string, BOT_NICK)


def room_is_valid(room):
    return room.startswith("#")


class BotCommandsTestCase(unittest.TestCase):
    def setUp(self):
        self.irc = MockIrc()

    def test_join_command_valids(self):
        rooms = ["#fake_room_1", "#fake_room_3"]
        join_exec(self.irc, build_join_message(build_join_command(rooms)))
        for n, result in enumerate(self.irc.messages):
            self.assertEqual(("JOIN " + rooms[n] + "\n").encode("utf-8"), result)

    def test_join_command_invalids(self):
        rooms = ["Henlo", "bad_room", "iske", "ta-da"]
        join_exec(self.irc, build_join_message(build_join_command(rooms)))
        self.assertEqual([], self.irc.messages)

    def test_join_command_mixed(self):
        rooms = ["Bad_room", "#good_room", "another_bad_room", "#python", "#an_actual_room"]
        join_exec(self.irc, build_join_message(build_join_command(rooms)))
        for room in rooms:
            if room_is_valid(room):
                self.assertIn(("JOIN " + room + "\n").encode("utf-8"), self.irc.messages)
            else:
                self.assertNotIn(("JOIN " + room + "\n").encode("utf-8"), self.irc.messages)


if __name__ == '__main__':
    unittest.main()
