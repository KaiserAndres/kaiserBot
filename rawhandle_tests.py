import unittest
from rawhandle import Message


BOT_NAME = "kaiTest"

class MessageTest(unittest.TestCase):
    def test_ping(self):
        message = Message("PING :300472EC", BOT_NAME)
        self.assertEqual(message.text, "PING :300472EC")

    def test_username(self):
        message = Message(":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!TAROT 6", BOT_NAME)
        self.assertEqual(message.userName, "KAISER_")

    def test_text(self):
        message = Message(":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!TAROT 1", BOT_NAME)
        self.assertEqual(message.text, "!TAROT 1")

    def test_public_channel(self):
        message = Message(":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!TAROT 1", BOT_NAME)
        self.assertEqual(message.channel, "#KAISER_TEST")

if __name__ == '__main__':
    unittest.main()
