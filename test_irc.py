import socket
import tests
import irc


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

def fakewrapper(sock):
    sock.ssl_wrapped = True
    return sock

def test_socket(logger):
    for ssl in [False, True]:
        if ssl: logger = logger.deeper('ssl')

        logger.print('Creating pretend socket with{} ssl...'.format('out' if not ssl else ''))
        pret = PretendSocket()
        sock = irc.Socket('server', 42, ssl, 300, sock=pret, ssl_wrap=fakewrapper)
        
        # no contents, reading should be empty string
        logger.print('Reading without any socket contents...')
        assert sock.read() == None

        # no complete line available, reading should still be empty
        logger.print('Reading with an incomplete line...')
        pret.contents = b'hello, wor'
        assert sock.read() == None

        # complete line should be returned!
        logger.print('Reading with a single complete line...')
        pret.contents = b'ld!\r\n'
        assert sock.read() == 'hello, world!'

        # only one line should be returned at a time
        # last line is not complete and should not be returned
        logger.print('Reading quite a few lines...')
        pret.contents = b'a\r\nb\r\nc\r\nd'
        assert sock.read() == 'a'
        assert sock.read() == 'b'
        assert sock.read() == 'c'
        assert sock.read() == None
        assert sock.read() == None

    return True

def test_run(logger):
    pret = PretendSocket()

    flog = tests.FakeLogger()

    logger.print('Testing run with invalid settings...')
    try:
        result = irc.run('', {}, log=flog.log_to_list, sock=pret)
        assert flog.logged_list[0]
        irc.run({}, {}, log=flog.log_to_list, sock=pret)
        assert flog.logged_list[1]
        irc.run({'irc': {'server': 'test', 'port': 'bark', 'ssl': 0, 'reconnect_delay': 12}}, {}, log=flog.log_to_list, sock=pret)
        assert flog.logged_list[2]
    except IndexError:
        raise AssertionError('run() didn\'t log')
    except Exception as e:
        raise AssertionError(str(e))
    else:
        assert result == 'reconnect'


    logger.print('Testing run with bad socket...')
    pret.explode = True
    try:
        for i, pret.explosion in enumerate([BrokenPipeError, ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError, socket.timeout]):
            result = irc.run({'irc': {'server': 'test', 'port': 587, 'ssl': False, 'reconnect_delay': 12}},
                             {}, log=flog.log_to_list, sock=pret)
            assert flog.logged_list[3 + i]
            assert result == 'reconnect'
    except IndexError:
        raise AssertionError('run() didn\'t log')

    return True


def test_handle(logger):
    def force_evaluation(mygen):
        for _ in mygen:
            pass

    frog = tests.FakeLogger()

    logger.print('Checking for response to PING...')
    responses = irc.handle('PING :abracadabra', {}, {})
    assert 'PONG :abracadabra' in responses

    logger.print('Checking a broken message results in logging...')
    force_evaluation(irc.handle('completely geschtonkenflapped', {}, {}, log=frog.log))
    assert frog.logged

    frog.reset()
    logger.print('Checking that a nick change happens when nick is in use...')
    responses = irc.handle('433 anything', {'irc': {'nick': 'orignick'}}, {'nick': 'lolbawt'}, log=frog.log)
    assert any('NICK ' in response for response in responses)
    assert frog.logged

    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_socket(logger.deeper('Socket'))
    assert test_run(logger.deeper('run'))
    assert test_handle(logger.deeper('handle'))
    logger.print('All tests complete!')
    return True

