import re, datetime
import logger

def test_log(logger_):
    logger_.print('Testing log output format...')

    ret = logger.log('error1', 'error', test=True)

    assert ret['filename'] == 'log/error.log'

    m = re.search('(.+) \[(.+)\]: (.+)', ret['msg'])

    assert m.group(1) == __name__
    assert m.group(3) == 'error1'

    datetime.datetime.strptime(m.group(2), '%Y-%m-%d %H:%M:%S')

    return True

def test_run_all(logger_):
    logger_.print('Running all tests...')
    assert test_log(logger_.deeper('log'))
    logger_.print('All tests complete!')
    return True
