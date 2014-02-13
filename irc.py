import admin, common, ircparser, logger, statekeeper

import socket
import random
import string
import errno
from ssl import wrap_socket, SSLError
from time import sleep, time


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
            try:
                irc = Socket(
                    settings['irc']['server'],
                    settings['irc']['port'],
                    settings['irc']['ssl'],
                )
            except (socket.error, socket.herror, socket.gaierror):
                log('error', 'Connection failed.')
                return 'reconnect'

        state['last_message'] = time()
        state['pinged'] = False
        state['nick'] = settings['irc']['nick']
        state['joined_channel'] = None

        irc.send('NICK {}'.format(state['nick']))
        irc.send('USER {0} 0 * :IRC Bot {0}'.format(settings['irc']['nick']))

        sleep(1)

    except SocketError as e:
        # e is equal to ((errno, reason), recommendation)
        log('error', e[0][1])
        return e[1]

    except Exception as e:
        log('error', e)

    while True:
        try:
            line = irc.read()

            if line:
                state['last_message'] = time()
                for response in handle(line, settings, state):
                    irc.send(response)
            else:
                if not state['pinged'] and time() - state['last_message'] > settings['irc']['grace_period']:
                    irc.send('PING :arst')
                    state['pinged'] = True
                elif state['pinged'] and time() - state['last_message'] > settings['irc']['grace_period']:
                    log('error', 'Connection timed out.')
                    return 'reconnect'

        except SocketError as e:
            # e is equal to ((errno, reason), recommendation)
            log('error', e[0][1])
            return e[1]

        except Exception as e:
            log('error', e)

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

    if command == 'PONG':
        state['pinged'] = False

    if command == '433':
        def new_nick(nick):
            nick = nick[:min(len(nick), 6)] # determine how much to shave off to make room for random chars
            return '{}_{}'.format(nick, ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(2)))

        log('warning', '[statekeeping] Nick {} already in use, trying another one.'.format(state['nick']))
        state['nick'] = new_nick(settings['irc']['nick'])
        yield 'NICK {}'.format(state['nick'])

    if command == 'JOIN' and nick == state['nick']:
        # TODO: Fancy logging
        print('--> joined {}'.format(arguments[0]))

        if state['joined_channel']:
            # TODO: raise some sort of illegal state exception. remember to test for it
            # then what? have we joined two channels? what the shit are we supposed to do?
            pass

        state['joined_channel'] = arguments[0]

    if command == 'KICK' and arguments[1] == state['nick']:
        log('warning', '[statekeeping] Kicked from channel {} because {}'.format(arguments[0], ' '.join(arguments[1:])))

        if arguments[0] != state['joined_channel']:
            # TODO: raise some sort of illegal state exception
            pass

        state['joined_channel'] = None
        settings['irc']['channel'] = None

    if command == 'PRIVMSG':
        # Make the author the target for replies if it is a private message
        channel = nick if arguments[0] == state['nick'] else arguments[0]

        message = ' '.join(arguments[1:])
        # TODO: Turn this into some sort of cooler logging
        print('{}> {}'.format(channel, message))

        # TODO: Better admin shit, this is just poc/temporary
        if admin.is_admin(user):
            admin_result = admin.parse_admin_command(message, state['nick'])
            if admin_result:
                yield ircparser.make_privmsg(channel, admin_result)

        if message == 'hello, world':
            yield ircparser.make_privmsg(channel, 'why, hello!')
    else:
        log('raw', line)


    # TODO: Fix the state object so this isn't needed
    if 'joined_channel' not in state:
        state['joined_channel'] = None

    if not state['joined_channel'] and settings['irc']['channel']:
        yield 'JOIN {}'.format(settings['irc']['channel'])


class SocketError(Exception):
    def __init__(self, error):
        self.error = error
       
    def __get__(self):
        try:
            return  { errno.EPIPE:        (self.error, 'reconnect'),
                      errno.ECONNRESET:   (self.error, 'reconnect'),
                      errno.ECONNABORTED: (self.error, 'quit'),
                      errno.ECONNREFUSED: (self.error, 'quit'),
                    }[self.error[0]]
        except KeyError:
            raise socket.error(self.error)

class Socket:

    """ A line buffered IRC socket interface. send(text) sends
        text as UTF-8 and appends a newline, read() reads text
        and returns a list of strings which are the read lines
        without a line separator."""

    def __init__(self, server, port, ssl_enabled,
                   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                   ssl_wrap=wrap_socket):
        # try to connect
        try: sock.connect((server, port))
        # try really, really hard
        # TODO: except what!?
        except: sock.send(bytes('', 'utf-8'))

        if ssl_enabled:
            sock = ssl_wrap(sock)

        sock.settimeout(1)

        self.ssl_enabled = ssl_enabled
        self.sock = sock

        # initialise an empty buffer
        self.buffer = b''

    def send(self, text):
        # TODO: sanity checking
        try:
            self.sock.send(bytes(text + '\n', 'utf-8'))
        except socket.error as e:
            raise SocketError(e)

    def read(self):
        try:
            if b'\r\n' not in self.buffer:
                self.buffer += self.sock.read(4096) if self.ssl_enabled else self.sock.recv(4096)
        except socket.timeout:
            return None
        except socket.error as e:
            raise SocketError(e)
    
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
