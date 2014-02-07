import os, re, datetime
import logger

def test_append_file(logger_):
    logger.append_file('test.txt', 'testdata')    

    logger_.print('Reading appended data and verifying it\'s correct')
    with open('test.txt', 'r') as f:
        lines = f.readlines()

    assert lines[-1].strip('\n') == 'testdata'

    os.remove('test.txt')

    return True

def test_log(logger_):
    logger_.print('Testing log output format...')

    ret = logger.log('error1', 'error', output_to_file=False)

    assert ret['filename'] == 'log/error.log'

    m = re.search('(.+) \[(.+)\]: (.+)', ret['msg'])

    assert m.group(1) == __name__
    assert m.group(3) == 'error1'

    logger_.print('Testing date and time format...')
    datetime.datetime.strptime(m.group(2), '%Y-%m-%d %H:%M:%S')

    return True


def test_run_all(logger_):
    logger_.print('Running all tests...')
    assert test_append_file(logger_.deeper('append_file'))
    assert test_log(logger_.deeper('log'))
    logger_.print('All tests complete!')
    return True
