import ircparser

import unittest

class SplitTest(unittest.TestCase):

    def test_without_user(self):
        self.assertEqual(ircparser.split('CMD :args together'), (None, 'CMD', ['args together']))

    def test_single_argument(self):
        self.assertEqual(ircparser.split('CMD arg'), (None, 'CMD', ['arg']))

    def test_two_arguments(self):
        self.assertEqual(ircparser.split('CMD arg varg'), (None, 'CMD', ['arg', 'varg']))

    def test_without_user_and_arguments(self):
        self.assertEqual(ircparser.split('CMD'), (None, 'CMD', []))

    def test_without_arguments(self):
        self.assertEqual(ircparser.split(':test!user@host CMD'), ('test!user@host', 'CMD', []))

    def test_with_three_fields(self):
        self.assertEqual(ircparser.split(':test!user@host CMD :args together'), ('test!user@host', 'CMD', ['args together']))

    def test_with_many_arguments(self):
        self.assertEqual(ircparser.split('CMD with many :arguments together'), (None, 'CMD', ['with', 'many', 'arguments together']))

    def test_with_stray_colon(self):
        self.assertEqual(ircparser.split('CMD :arguments separated :by a colon'), (None, 'CMD', ['arguments separated :by a colon']))


class GetNickTest(unittest.TestCase):

    def test_with_normal_data(self):
        self.assertEqual(ircparser.get_nick('~nick!host.thing'), 'nick')
        self.assertEqual(ircparser.get_nick('~dave!host.with!weird.thing'), 'dave')
        self.assertEqual(ircparser.get_nick('sam!host~john!thing'), 'sam')

    def test_with_only_nick(self):
        self.assertIsNone(ircparser.get_nick('~john'))

    def test_with_empty_nick(self):
        self.assertIsNone(ircparser.get_nick('~!host.thing'))

    def test_with_tilde_nick(self):
        self.assertIsNone(ircparser.get_nick('~~~~!host.thing'))

    def test_with_invalid_string(self):
        self.assertIsNone(ircparser.get_nick('arstuaw~~3439'))

    def test_with_not_a_string(self):
        self.assertIsNone(ircparser.get_nick(None))


class MakePrivmsgTest(unittest.TestCase):

    def test_create_privmsg(self):
        self.assertEqual(ircparser.make_privmsg('#22', 'hello'), 'PRIVMSG #22 :hello')

    def test_to_empty_channel_name(self):
        with self.assertRaises(ValueError):
            ircparser.make_privmsg('', 'ho ho ho')

    def test_to_hash_channel_name(self):
        with self.assertRaises(ValueError):
            ircparser.make_privmsg('#', 'again')

    def test_without_content(self):
        self.assertEqual(ircparser.make_privmsg('#m', ''), 'PRIVMSG #m :')
