
import ircparser, logger

import socket
from ssl import wrap_socket, SSLError
from time import sleep


# run() should *never* for *any* reason throw any exceptions.
# the absolute worst cases should be caught in here and
# then 'reconnect' returned back to main
# This means that every single line should be covered
# by a general "except Exception as e"!!
def run(settings, sock=None):
    try:
        if sock:
            irc = sock
        else:
            irc = Socket(
                settings['irc']['server'],
                settings['irc']['port'],
                settings['irc']['ssl'],
                settings['irc']['reconnect_delay']/10
            )

        irc.send('NICK {}'.format(settings['irc']['nick']))
        irc.send('USER {0} 0 * :IRC Bot {0}'.format(settings['irc']['nick']))
        sleep(1)
        irc.send('JOIN {}'.format(settings['irc']['channel']))

    except (socket.error, socket.herror, socket.gaierror):
        logger.log('error', 'Connection failed. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))

        return 'reconnect'
    except Exception as e:
        try:
            logger.log('error', '{}. Reconnecting in {} seconds...'.format(e, settings['irc']['reconnect_delay']))
        except:
            logger.log('error', 'Bad config.')

        return 'reconnect'

    while True:
        try:
            line = irc.read()
            if line:
                for response in handle(line, settings):
                    irc.send(response)

        except BrokenPipeError:
            logger.log('error', 'Broken pipe. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))
            return 'reconnect'
        except ConnectionResetError:
            logger.log('error', 'Connection reset. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))
            return 'reconnect'
        except (ConnectionAbortedError, ConnectionRefusedError):
            logger.log('error', 'Connection refused or aborted. Closing...')
            return 'quit'
        except socket.timeout:
            logger.log('error', 'Connection timed out. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))
            return 'reconnect'
            # TODO: More of these errors. stolen from legacy:
            # probably also
            #  *  SSLError (if 'timed out' in str(e))?
        except Exception as e:
            logger.log('error', str(e))

    return 'reconnect'


# TODO: A lot of the stuff in here are candidates for
# admin.py or behaviour.py of course. I'm just putting
# it here for safekeeping
def handle(line, settings):
    # TODO: Write docstring about how this yields responses
    user, command, arguments = ircparser.split(line)
    nick = ircparser.get_nick(user)

    if command == 'PING':
        yield 'PONG :' + arguments[0]

    if command == 'PRIVMSG':
        channel = arguments[0]
        message = ' '.join(arguments[1:])
        print('{}> {}'.format(channel, message))

        if message == 'hello, world':
            yield ircparser.make_privmsg(settings['irc']['channel'], 'why, hello!')
    else:
        logger.log('raw', line)

class Socket:

    """ A line buffered IRC socket interface. send(text) sends
        text as UTF-8 and appends a newline, read() reads text
        and returns a list of strings which are the read lines
        without a line separator."""

    def __init__(self, server, port, ssl_enabled, timeout,
                   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                   ssl_wrap=wrap_socket):
        # try to connect
        try: sock.connect((server, port))
        # try really, really hard
        # TODO: except what!?
        except: sock.send(bytes('', 'utf-8'))

        if ssl_enabled:
            sock = ssl_wrap(sock)

        sock.settimeout(timeout)

        self.ssl_enabled = ssl_enabled
        self.sock = sock

        # initialise an empty buffer
        self.buffer = b''

    def send(self, text):
        # TODO: sanity checking
        self.sock.send(bytes(text + '\n', 'utf-8'))

    def read(self):
        try:
            if b'\r\n' not in self.buffer:
                self.buffer += self.sock.read(4096) if self.ssl_enabled else self.sock.recv(4096)
        except socket.timeout:
            pass
        except SSLError as e:
            if 'timed out' in str(e): pass
            else: raise

        try:
            [byteline, self.buffer] = self.buffer.split(b'\r\n', 1)
        except ValueError:
            return None

        def decode(text, encs):
            for enc in encs:
                try: return text.decode(enc)
                # TODO: except what?
                except: continue
            # fallback is iso-8859-1
            # TODO: why is it, though? why not utf-8?
            return text.decode('latin-1', 'replace')
        
        return decode(byteline, ['utf-8', 'latin-1', 'cp1252'])



