
import test_irc
import test_common

def test_run_all():
    print('Running all tests...')
    assert test_irc.test_run_all()
    assert test_common.test_run_all()
    print('All tests complete!')
    return True

if __name__ == '__main__':
    assert test_run_all()

