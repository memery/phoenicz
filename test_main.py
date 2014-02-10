import tests
import main

def test_valid_settings(logger):
    flog = tests.FakeLogger()
    
    logger.print('Testing validation of broken settings...')

    result = main.valid_settings({}, log=flog.log)
    assert not result
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
    result = main.valid_settings(settings, log=flog.log)

    assert not result
    assert flog.logged

    logger.print('Testing with missing settings')

    settings['irc'].pop('nick')
    flog.logged = False
    result = main.valid_settings(settings, log=flog.log)

    assert not result
    assert flog.logged

    logger.print('Testing with valid settings...')

    flog.logged = False
    settings['irc']['nick'] = 'nick'
    result = main.valid_settings(settings, log=flog.log)

    assert result
    assert not flog.logged

    logger.print('Testing with additional settings...')

    flog.logged = False
    settings['irc']['lag'] = 'don\'t'
    result = main.valid_settings(settings, log=flog.log)

    assert result
    assert not flog.logged

    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_valid_settings(logger.deeper('valid_settings'))
    logger.print('All tests complete!')
    return True

