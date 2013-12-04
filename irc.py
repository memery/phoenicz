
import socket
from ssl import wrap_socket



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
        self.buffer += self.sock.read(4096) if self.ssl_enabled else self.sock.recv(4096)
        try:
            [byteline, self.buffer] = self.buffer.split(b'\r\n', 1)
        except ValueError:
            # if there is no complete line in the buffer yet, return empty string
            return ''
        else:
            def decode(text, encs):
                for enc in encs:
                    try: return text.decode(enc)
                    # TODO: except what?
                    except: continue
                # fallback is iso-8859-1
                # TODO: why is it, though? why not utf-8?
                return text.decode('latin-1', 'replace')
            
            return decode(byteline, ['utf-8', 'latin-1', 'cp1252'])




def run(*args):
    print('stub!')

