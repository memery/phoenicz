import tests
import main

def test_validate_settings(logger):
    flog = tests.FakeLogger()
    
    logger.print('Testing validation of broken settings...')

    result = main.validate_settings({}, log=flog.log)
    assert result == 'quit'
    assert flog.logged

    settings = {'irc': {
                   'nick': 1,
                   'channel': '#channel',
                   'server': 'irc.example.org',
                   'port': 6667,
                   'ssl': True,
                   'reconnect_delay': 12,
               }}

    flog.logged = False
    result = main.validate_settings(settings, log=flog.log)

    assert result == 'quit'
    assert flog.logged

    logger.print('Testing with missing settings')

    settings['irc'].pop('nick')
    flog.logged = False
    result = main.validate_settings(settings, log=flog.log)

    assert result == 'quit'
    assert flog.logged

    logger.print('Testing with valid settings...')

    flog.logged = False
    settings['irc']['nick'] = 'nick'
    result = main.validate_settings(settings, log=flog.log)

    assert result != 'quit'
    assert not flog.logged

    logger.print('Testing with additional settings...')

    flog.logged = False
    settings['irc']['lag'] = 'don\'t'
    result = main.validate_settings(settings, log=flog.log)

    assert result != 'quit'
    assert not flog.logged

    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_validate_settings(logger.deeper('validate_settings'))
    logger.print('All tests complete!')
    return True

