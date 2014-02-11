import common, re

def test_read_config(logger):
    # Try to read a non-existent config. Config is vital
    # so this should blow up.
    logger.print('Trying to read non-existent config...')
    try: common.read_config('')
    except: pass
    else: return False

    return True

def test_error_info(logger):
    logger.print('Testing with non-exception argument...')
    formstr = "Error in error_info: {} is type {}, not an exception"
    assert common.error_info(None) == formstr.format('None', 'NoneType')

    logger.print('Testing with bad exception argument...')
    template = "[Exception] Test - Error when getting stacktrace: 'NoneType' object has no attribute '__context__'"
    assert common.error_info(Exception('Test')) == template

    logger.print('Testing with functioning exception argument...')
    rx = re.compile(r'^\[Exception\] Test - test_common\.py:\d+ in test_error_info$')
    try:
        raise Exception('Test')
    except Exception as e:
        errortext = common.error_info(e)
    assert rx.match(errortext) is not None
    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_read_config(logger.deeper('read_config'))
    assert test_error_info(logger.deeper('error_info'))
    logger.print('All tests complete!')
    return True


