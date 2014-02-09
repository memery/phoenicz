import main, test_irc

def test_validate_settings(logger):
    flog = test_irc.FakeLogger()
    
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

    logger.print('Testing with valid settings...')

    flog.logged = False
    settings['irc']['nick'] = 'nick'
    result = main.validate_settings(settings, log=flog.log)

    assert result != 'quit'
    assert not flog.logged

    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_validate_settings(logger.deeper('Settings validation'))
    logger.print('All tests complete!')
    return True

