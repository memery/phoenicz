
import ircparser


def test_split(logger):
    logger.print('Testing without user...')
    assert ircparser.split('CMD :args together') == (None, 'CMD', ['args together'])

    logger.print('Testing with a single argument...')
    assert ircparser.split('CMD arg') == (None, 'CMD', ['arg'])

    logger.print('Testing with two arguments...')
    assert ircparser.split('CMD arg varg') == (None, 'CMD', ['arg', 'varg'])

    logger.print('Testing without user and arguments...')
    assert ircparser.split('CMD') == (None, 'CMD', [])

    logger.print('Testing without arguments...')
    assert ircparser.split(':test!user@host CMD') == ('test!user@host', 'CMD', [])

    logger.print('Testing with three fields...')
    assert ircparser.split(':test!user@host CMD :args together') == ('test!user@host', 'CMD', ['args together'])

    logger.print('Testing with many arguments...')
    assert ircparser.split('CMD with many :arguments together') == (None, 'CMD', ['with', 'many', 'arguments together'])

    logger.print('Testing with a stray colon...')
    assert ircparser.split('CMD :arguments separated :by a colon') == (None, 'CMD', ['arguments separated :by a colon'])

    return True

def test_get_nick(logger):
    logger.print('Testing on normal data...')
    assert ircparser.get_nick('~nick!host.thing') == 'nick'
    assert ircparser.get_nick('~dave!host.with!weird.thing') == 'dave'
    assert ircparser.get_nick('sam!host~john!thing') == 'sam'

    logger.print('Testing with only nick...')
    try: ircparser.get_nick('~john')
    except ValueError: pass
    else: return False

    logger.print('Testing with empty nick...')
    try: ircparser.get_nick('~!host.thing')
    except ValueError: pass
    else: return False

    logger.print('Testing with tilde nick...')
    try: ircparser.get_nick('~~~~!host.thing')
    except ValueError: pass
    else: return False

    logger.print('Testing with a completely invalid string...')
    try: ircparser.get_nick('arstuaw~~3439')
    except ValueError: pass
    else: return False

    logger.print('Testring with not a string...')
    assert ircparser.get_nick(None) == None

    return True

def test_make_privmsg(logger):
    logger.print('Trying to create a privmsg...')
    assert ircparser.make_privmsg('#22', 'hello') == 'PRIVMSG #22 :hello'

    logger.print('Trying to create a privmsg to an empty channel name...')
    try: ircparser.make_privmsg('', 'ho ho ho')
    except ValueError: pass
    else: return False

    logger.print('Trying to create a privmsg to an empty channel name again...')
    try: ircparser.make_privmsg('#', 'again')
    except ValueError: pass
    else: return False

    logger.print('Trying to create a privmsg with no content...')
    assert ircparser.make_privmsg('#m', '') == 'PRIVMSG #m :'

    return True

def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_split(logger.deeper('split'))
    assert test_get_nick(logger.deeper('get_nick'))
    assert test_make_privmsg(logger.deeper('make_privmsg'))
    logger.print('All tests complete!')
    return True


