
import test_main
import test_irc
import test_ircparser
import test_common
import test_logger
import test_statekeeper


class FakeLogger:
    def __init__(self):
        self.logged = False
        self.logged_list = []

    def log(self, x, y):
        self.logged = True

    def log_to_list(self, x, y):
        self.logged_list.append(True)

    def reset(self):
        self.logged = False
        self.logged_list = []

class Logger:
    def __init__(self, next, previous=[]):
        self.hierarchy = previous + [next]

    def print(self, msg):
        print('[{}]: {}'.format('/'.join(self.hierarchy), msg))

    def deeper(self, next):
        print('[{}]: Testing {}...'.format('/'.join(self.hierarchy), next))
        return Logger(next, previous=self.hierarchy)


# Try to run tests in order of dependence: since irc.py depends
# on ircparser, run the tests for ircparser first. (This hopefully
# eliminates the problem where there's an error in ircparser
# and instead of ircparser failing its tests, irc crashes with
# some weird error.)
def test_run_all():
    print('Running all tests...')
    assert test_main.test_run_all(Logger('main'))
    assert test_ircparser.test_run_all(Logger('ircparser'))
    assert test_common.test_run_all(Logger('common'))
    assert test_statekeeper.test_run_all(Logger('statekeeper'))
    assert test_irc.test_run_all(Logger('irc'))
    assert test_logger.test_run_all(Logger('logger'))
    print('All tests complete!')
    return True

if __name__ == '__main__':
    assert test_run_all()

