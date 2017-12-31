import unittest
from rawhandle import Message


BOT_NAME = "kaiTest"


class MessageTest(unittest.TestCase):
    def test_ping_identity(self):
        message = Message("PING :300472EC", BOT_NAME)
        self.assertEqual("PING :300472EC", message.text)

    def test_ping_username_is_empty(self):
        message = Message("PING :300472EC", BOT_NAME)
        self.assertEqual("", message.userName)

    def test_timeout_message_empty_username(self):
        message = Message(":CLOSING LINK: HOST55.170-80-170.NETWORK.NET (CONNECTION TIMED OUT)", BOT_NAME)
        self.assertEqual("", message.userName)

    def test_username(self):
        message = Message(":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!TAROT 6", BOT_NAME)
        self.assertEqual("KAISER_", message.userName)

    def test_text(self):
        message = Message(":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!TAROT 1", BOT_NAME)
        self.assertEqual("!TAROT 1", message.text,)

    def test_public_channel(self):
        message = Message(":KAISER_!~QUASSEL@HOST55.170-80-170.NETWORK.NET PRIVMSG #KAISER_TEST :!TAROT 1", BOT_NAME)
        self.assertEqual("#KAISER_TEST", message.channel)

    def test_private_channel(self):
        message = Message(":KAISER_!~QUASSEL@HOST92.170-80-171.NETWORK.NET PRIVMSG " + BOT_NAME + " :!ROLL 1D20", BOT_NAME)
        self.assertEqual(message.userName, message.channel)

    def test_frowny_face_bug(self):
        message = Message(":OREA!KIWIIRC@CPC1166-HEHE14-2-0-CUST57.9-1.CABLE.VIRGINM.NET PRIVMSG #RPGSTUCK_REDLOTUS::C", BOT_NAME)
        self.assertEqual("#RPGSTUCK_REDLOTUS", message.channel)

    def test_message_with_url(self):
        text = ":SEAN_AYRES!WEBCHAT@D162-156.NETWORK:COM PRIVMSG #RPGSTUCK_REDLOTUS :HTTPS://PASTEBIN.COM/A6ECRGD7"
        message = Message(text, BOT_NAME)
        self.assertEqual("HTTPS://PASTEBIN.COM/A6ECRGD7", message.text)


if __name__ == '__main__':
    unittest.main()
