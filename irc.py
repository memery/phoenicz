import ircparser, logger

import socket
import random
import string
from ssl import wrap_socket, SSLError
from time import sleep


# run() should *never* for *any* reason throw any exceptions.
# the absolute worst cases should be caught in here and
# then 'reconnect' returned back to main
# This means that every single line should be covered
# by a general "except Exception as e"!!
def run(settings, state, log=logger.log, sock=None):
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

        state['irc']['nick'] = settings['irc']['nick']
        irc.send('NICK {}'.format(state['irc']['nick']))

        irc.send('USER {0} 0 * :IRC Bot {0}'.format(settings['irc']['nick']))

        sleep(1)
        irc.send('JOIN {}'.format(settings['irc']['channel']))

    except (socket.error, socket.herror, socket.gaierror):
        log('error', 'Connection failed. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))

        return 'reconnect'
    except Exception as e:
        try:
            log('error', '{}. Reconnecting in {} seconds...'.format(e, settings['irc']['reconnect_delay']))
        except:
            log('error', 'Bad config.')

        return 'reconnect'

    while True:
        try:
            line = irc.read()
            if line:
                for response in handle(line, settings, state):
                    irc.send(response)

        # TODO: These exceptions should be handled in the socket class. They are overridden
              # earlier in this function in the handshake.
        except BrokenPipeError:
            log('error', 'Broken pipe. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))
            return 'reconnect'
        except ConnectionResetError:
            log('error', 'Connection reset. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))
            return 'reconnect'
        except (ConnectionAbortedError, ConnectionRefusedError):
            log('error', 'Connection refused or aborted. Closing...')
            return 'quit'
        except socket.timeout:
            log('error', 'Connection timed out. Reconnecting in {} seconds...'.format(settings['irc']['reconnect_delay']))
            return 'reconnect'
            # TODO: More of these errors. stolen from legacy:
            # probably also
            #  *  SSLError (if 'timed out' in str(e))?
        except Exception as e:
            log('error', str(e))

    return 'reconnect'


# TODO: A lot of the stuff in here are candidates for
# admin.py or behaviour.py of course. I'm just putting
# it here for safekeeping
def handle(line, settings, state, log=logger.log):
    # TODO: Write docstring about how this yields responses
    user, command, arguments = ircparser.split(line)
    nick = ircparser.get_nick(user)

    if command == 'PING':
        yield 'PONG :' + arguments[0]

    if command == '433':
        def new_nick(nick):
            nick = nick[:min(len(nick), 6)] # determine how much to shave off to make room for random chars
            return '{}_{}'.format(nick, ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(2)))

        log('warning', '[statekeeping] Nick {} already in use, trying another one.'.format(state['irc']['nick']))
        state['irc']['nick'] = new_nick(settings['irc']['nick'])
        yield 'NICK {}'.format(state['irc']['nick'])


    if command == 'PRIVMSG':
        channel = arguments[0]
        message = ' '.join(arguments[1:])
        # TODO: Turn this into some sort of cooler logging
        print('{}> {}'.format(channel, message))

        if message == 'hello, world':
            yield ircparser.make_privmsg(settings['irc']['channel'], 'why, hello!')
    else:
        log('raw', line)


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



