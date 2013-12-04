
import common

def test_read_config():
    # Try to read a non-existent config. Config is vital
    # so this should blow up.
    print('[common/read_config]: Trying to read non-existent config...')
    try: common.read_config('')
    except: pass
    else: raise AssertionError('Should not be able to read non-existent config')

    return True


def test_run_all():
    print('[common]: Running all tests...')
    assert test_read_config()
    print('[common]: All tests complete!')
    return True


