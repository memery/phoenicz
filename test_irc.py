
import irc

class PretendSocket:
    def __init__(self, *args):
        self.connected = False
        self.ssl_wrapped = False
        self.contents = b''

    def connect(self, *args):
        self.connected = True

    def settimeout(self, *args):
        assert self.connected

    def send(self, msg):
        assert self.connected

    def read(self, *args):
        assert self.ssl_wrapped
        return self.recv(*args)

    def recv(self, *args):
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
        assert sock.read() == ''

        # no complete line available, reading should still be empty
        logger.print('Reading with an incomplete line...')
        pret.contents = b'hello, wor'
        assert sock.read() == ''

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
        assert sock.read() == ''
        assert sock.read() == ''

    return True

def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_socket(logger.deeper('socket'))
    logger.print('All tests complete!')
    return True

