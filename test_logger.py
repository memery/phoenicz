import os, re, datetime
import logger

def test_error_info(logger_):
    logger_.print('Testing with non-exception argument...')
    assert logger.error_info(None) == None

    logger_.print('Testing with bad exception argument...')
    template = "[Exception] Test - Error when getting stacktrace: 'NoneType' object has no attribute '__context__'"
    assert logger.error_info(Exception('Test')) == template

    logger_.print('Testing with functioning exception argument...')
    rx = re.compile(r'^\[Exception\] Test - test_logger\.py:\d+ in test_error_info$')
    try:
        raise Exception('Test')
    except Exception as e:
        errortext = logger.error_info(e)
    assert rx.match(errortext) is not None
    return True

def test_append_file(logger_):
    logger.append_file('test.txt', 'testdata')    

    logger_.print('Reading appended data and verifying it\'s correct')
    with open('test.txt', 'r') as f:
        lines = f.readlines()

    assert lines[-1].strip('\n') == 'testdata'

    os.remove('test.txt')

    return True

def test_log(logger_):
    re_log = re.compile('(.+) \[(.+)\]: (.+)')

    logger_.print('Testing log output format...')

    ret = logger.log('error', 'error1')

    assert ret['filename'] == 'log/error.log'

    m = re.search(re_log, ret['msg'])

    assert m.group(1) == __name__
    assert m.group(3) == 'error1'


    logger_.print('Testing with None-type message...')

    ret = logger.log('error', None)

    m = re.search(re_log, ret['msg'])

    assert m.group(1) == __name__
    assert m.group(3) == 'None'

    logger_.print('Testing date and time format...')
    datetime.datetime.strptime(m.group(2), '%Y-%m-%d %H:%M:%S')

    return True


def test_run_all(logger_):
    logger_.print('Running all tests...')
    assert test_error_info(logger_.deeper('error_info'))
    assert test_append_file(logger_.deeper('append_file'))
    assert test_log(logger_.deeper('log'))
    logger_.print('All tests complete!')
    return True
