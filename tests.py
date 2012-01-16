#!/usr/bin/env python

import unittest
import muirc

class TranslateTestCase(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            muirc.translate("PRIVMSG #irc :Hello, World! :-)\r\n"),
            {'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']}
        )

    def test_generate(self):
        self.assertEqual(
            muirc.translate({'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']}),
            'PRIVMSG #irc :Hello, World! :-)\r\n'
        )

    def test_identity(self):
        self.assertEqual(
            muirc.translate(muirc.translate("PRIVMSG #irc :Hello, World! :-)\r\n")),
            'PRIVMSG #irc :Hello, World! :-)\r\n'
        )

        self.assertEqual(
            muirc.translate(muirc.translate({'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']})),
            {'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']}
        )

    def test_parse_adv(self):
        self.assertEqual(
            muirc.translate(":nick!user@host PRIVMSG #irc :Hello, World! :-)"),
            {'nick': 'nick', 'host': 'host', 'command': 'PRIVMSG', 'user': 'user', 'params': ['#irc', 'Hello, World! :-)']}
        )

    def test_generate_adv(self):
        self.assertEqual(
            muirc.translate(muirc.translate(":nick!user@host PRIVMSG #irc :Hello, World! :-)")),
            ':nick!user@host PRIVMSG #irc :Hello, World! :-)\r\n'
        )

if __name__ == "__main__":
    unittest.main()

