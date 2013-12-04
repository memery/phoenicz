
import common

def test_read_config(logger):
    # Try to read a non-existent config. Config is vital
    # so this should blow up.
    logger.print('Trying to read non-existent config...')
    try: common.read_config('')
    except: pass
    else: raise AssertionError('Should not be able to read non-existent config')

    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_read_config(logger.deeper('read_config'))
    logger.print('All tests complete!')
    return True


