import unittest
from bot_executables import *
from rawhandle import Message

BOT_NICK = "test_bot"


class MockIrc():
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)


class ExecutionTest(unittest.TestCase):
    def setUp(self):
        self.irc = MockIrc()


def build_join_command(rooms):
    return ":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!JOIN " + " ".join(rooms)


def build_join_message(message_string):
    return Message(message_string, BOT_NICK)


def room_is_valid(room):
    return room.startswith("#")


def build_irc_join_command(room):
    return ("JOIN " + room + "\n").encode("utf-8")


def build_tarot_command(number):
    return "!TAROT " + str(number)


class JoinCommandTestCase(ExecutionTest):
    def test_join_command_valids(self):
        rooms = ["#fake_room_1", "#fake_room_3"]
        join_exec(self.irc, build_join_message(build_join_command(rooms)))
        for n, result in enumerate(self.irc.messages):
            self.assertEqual(build_irc_join_command(rooms[n]), result)

    def test_join_command_invalids(self):
        rooms = ["Henlo", "bad_room", "iske", "ta-da"]
        join_exec(self.irc, build_join_message(build_join_command(rooms)))
        self.assertEqual([], self.irc.messages)

    def test_join_command_mixed(self):
        rooms = ["Bad_room", "#good_room", "another_bad_room", "#python", "#an_actual_room"]
        join_exec(self.irc, build_join_message(build_join_command(rooms)))
        for room in rooms:
            if room_is_valid(room):
                self.assertIn(build_irc_join_command(room), self.irc.messages)
            else:
                self.assertNotIn(build_irc_join_command(room), self.irc.messages)


class PingCommandTestCase(ExecutionTest):
    def test_ping_call(self):
        ping_body = ":12345678910"
        ping_exec(self.irc, Message("PING "+ping_body, BOT_NICK))
        self.assertEqual(("PONG "+ping_body+"\r\n").encode("utf-8"), self.irc.messages[0])


class TarotCommandTestCase(ExecutionTest):
    def test_card_amount(self):
        result = get_card_amount(Message(build_tarot_command(5), BOT_NICK))
        self.assertEqual(5, result)

    def test_card_amount_high(self):
        result = get_card_amount(Message(build_tarot_command(99), BOT_NICK))
        self.assertEqual(MAX_CARDS, result)

    def test_card_amount_negative(self):
        result = get_card_amount(Message(build_tarot_command(-1), BOT_NICK))
        self.assertEqual(1, result)

    def test_card_amount_no_message(self):
        result = get_card_amount(Message("!TAROT", BOT_NICK))
        self.assertEqual(1, result)

    def test_card_amount_zero(self):
        result = get_card_amount(Message(build_tarot_command(0), BOT_NICK))
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()
