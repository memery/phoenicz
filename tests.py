
import test_irc
import test_common


class Logger:
    def __init__(self, next, previous=[]):
        self.hierarchy = previous + [next]

    def print(self, msg):
        print('[{}]: {}'.format('/'.join(self.hierarchy), msg))

    def deeper(self, next):
        return Logger(next, previous=self.hierarchy)


def test_run_all():
    print('Running all tests...')
    assert test_irc.test_run_all(Logger('irc'))
    assert test_common.test_run_all(Logger('common'))
    print('All tests complete!')
    return True

if __name__ == '__main__':
    assert test_run_all()

