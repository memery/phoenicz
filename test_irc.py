import socket
import testlib
import irc

import unittest

class PretendSocket:
    def __init__(self, *args):
        self.connected = False
        self.ssl_wrapped = False
        self.contents = b''
        self.explode = False
        self.explosion = None

    def connect(self, *args):
        if self.explode:
            raise self.explosion()
        self.connected = True

    def settimeout(self, *args):
        assert self.connected

    def send(self, msg):
        if self.explode:
            raise self.explosion()
        assert not self.explode
        assert self.connected

    def read(self, *args):
        assert self.ssl_wrapped
        return self.recv(*args)

    def recv(self, *args):
        if self.explode:
            raise self.explosion()
        assert not self.explode
        assert self.connected
        contents = self.contents
        self.contents = b''
        return contents


class SocketTest(unittest.TestCase):

    def test_socket(self):
        def fakewrapper(sock):
            sock.ssl_wrapped = True
            return sock

        for ssl in (False, True):
            pret = PretendSocket()
            sock = irc.Socket('server', 42, ssl, sock=pret, ssl_wrap=fakewrapper)

            # no contents, reading should be empty string
            self.assertIsNone(sock.read())

            # no complete line available, reading should still be empty
            pret.contents = b'hello, wor'
            self.assertIsNone(sock.read())

            # complete line should be returned!
            pret.contents = b'ld!\r\n'
            self.assertEqual(sock.read(), 'hello, world!')

            # only one line should be returned at a time
            # last line is not complete and should not be returned
            pret.contents = b'a\r\nb\r\nc\r\nd'
            self.assertEqual(sock.read(), 'a')
            self.assertEqual(sock.read(), 'b')
            self.assertEqual(sock.read(), 'c')
            self.assertIsNone(sock.read())
            self.assertIsNone(sock.read())


class RunTest(unittest.TestCase):

    def setUp(self):
        self.pret = PretendSocket()
        self.flog = testlib.FakeLogger()

    def test_with_invalid_settings(self):
        try:
            result = irc.run('', {}, log=self.flog.log_to_list, sock=self.pret)
            self.assertTrue(self.flog.logged_list[0])
            irc.run({}, {}, log=self.flog.log_to_list, sock=self.pret)
            self.assertTrue(self.flog.logged_list[1])
            irc.run({'irc': {'server': 'test', 'port': 'bark', 'ssl': 0, 'reconnect_delay': 12}}, {}, log=self.flog.log_to_list, sock=self.pret)
            self.assertTrue(self.flog.logged_list[2])
        except IndexError:
            self.fail('run() didn\'t log')
        except Exception as e:
            self.fail(str(e))
        else:
            self.assertEqual(result, 'reconnect')

    def test_with_bad_socket(self):
        self.pret.explode = True
        try:
            for i, self.pret.explosion in enumerate([BrokenPipeError, ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError, socket.timeout]):
                result = irc.run({'irc': {'server': 'test', 'port': 587, 'ssl': False, 'reconnect_delay': 12}},
                                 {}, log=self.flog.log_to_list, sock=self.pret)
                self.assertTrue(self.flog.logged_list[i])
                self.assertEqual(result, 'reconnect')
        except IndexError:
            self.fail('run() didn\'t log')


class HandleTest(unittest.TestCase):

    def setUp(self):
        self.frog = testlib.FakeLogger()
        self.fakesettings = {'irc': {'channel': '#channel'}}

    def force_evaluation(self, mygen):
        for _ in mygen:
            pass

    def test_ping_response(self):
        self.assertIn('PONG :abracadabra', irc.handle('PING :abracadabra', self.fakesettings, {}))

    def test_log_broken_message(self):
        self.force_evaluation(irc.handle('completely geschtonkenflapped', self.fakesettings, {}, log=self.frog.log))
        self.assertTrue(self.frog.logged)

    def test_nick_change_when_in_use(self):
        responses = irc.handle('433 anything', {'irc': {'nick': 'orignick'}}, {'nick': 'lolbawt'}, log=self.frog.log)
        self.assertTrue(any('NICK ' in response for response in responses))
        self.assertTrue(self.frog.logged)

    def test_state_change_after_channel_join(self):
        fakestate = {'joined_channel': None, 'nick': 'tnick'}
        self.force_evaluation(irc.handle(':tnick!example.com JOIN :#channel', {'irc': {'channel': '#channel'}}, fakestate, log=self.frog.log))
        self.assertEqual(fakestate['joined_channel'], '#channel')

    def test_channel_removal_after_kick(self):
        fakestate = {'joined_channel': '#channel', 'nick': 'tnick'}
        self.force_evaluation(irc.handle('KICK #channel tnick :asdkfb', self.fakesettings, fakestate, log=self.frog.log))
        self.assertIsNone(fakestate['joined_channel'])
        self.assertIsNone(self.fakesettings['irc']['channel'])
        self.assertTrue(self.frog.logged)
        self.assertIn('asdkfb', self.frog.contents)

    def test_status_unaffected_after_others_kick(self):
        fakestate = {'joined_channel': '#channel', 'nick': 'tnick'}
        self.force_evaluation(irc.handle('KICK #channel wrongnick :reason', self.fakesettings, fakestate, log=self.frog.log))
        self.assertEqual(fakestate['joined_channel'], '#channel')
        self.assertEqual(self.fakesettings['irc']['channel'], '#channel')

    def test_join_channel_when_applicable(self):
        responses = irc.handle('666', {'irc': {'channel': '#testchan'}}, {'joined_channel': None}, log=self.frog.log)
        self.assertIn('JOIN #testchan', responses)

    def test_join_channel_when_not_applicable(self):
        responses = irc.handle('666', {'irc': {'channel': '#testchan'}}, {'joined_channel': '#testchan'}, log=self.frog.log)
        self.assertNotIn('JOIN ', responses)
        responses = irc.handle('666', {'irc': {'channel': None}}, {'joined_channel': None}, log=self.frog.log)
        self.assertNotIn('JOIN ', responses)

