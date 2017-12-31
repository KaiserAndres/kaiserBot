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

    def test_help_message_reading_crash(self):
        text = "HELLO! I AM KAISERBOT, I AM A TINY BOT MADE MY KAISERA, YOU CAN RUN THE FOLLOWING COMMANDS ON ME: !ROLL, !JOIN !HELP.!ROLL USES THE FOLLOWING PARAMETERS: !ROLL <TIMES>#<AMOUNT OF DICE>D<MAX DIE>+<MOD> AMOUNT OF DIE AND MAX DIE ARE OBLIGATORY.!JOIN TAKES THE FOLLOWING PARAMETERS: !JOIN #<CHANNELNAME>. I AM VERSION 1.0 AND I CAN BE DOWNLOADED AT THE FOLLOWING ADDRESS: HTTPS://GITHUB.COM/KAISERANDRES/KAISERBOT. I RUN ON PYTHON 3.X S"
        irc_text = ":TYCHE[DICE-TESTING]!~TYCHEDICE@159.203.126.111 PRIVMSG " + BOT_NAME + " :" + text
        message = Message(irc_text, BOT_NAME)
        self.assertEqual(text, message.text)


if __name__ == '__main__':
    unittest.main()
