import os, re, datetime, unittest
import logger


class LoggerTest(unittest.TestCase):

    @classmethod
    def tearDownClass(LoggerTest):
        try:
            os.remove('test.txt')
        except FileNotFoundError:
            pass

    def test_append_file(self):
        logger.append_file('test.txt', 'testdata')
        with open('test.txt', 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines[-1].strip('\n'), 'testdata')

    def test_log_filename(self):
        ret = logger.log('error', 'error1')
        self.assertEqual(ret['filename'], 'log/error.log')

    def generic_log_test(self, arg):
        ret = logger.log('error', arg)
        self.assertRegex(ret['msg'], r'^{} \[.+\]: {}$'.format(__name__, arg))

    def test_log_output_format(self):
        self.generic_log_test('error1')

    def test_log_output_format_with_none_argument(self):
        self.generic_log_test('None')

    def test_log_output_format_with_empty_string_argument(self):
        self.generic_log_test('')

    def test_log_output_format_timestamp(self):
        ret = logger.log('error', 'test')
        m = re.search(r'^.+ \[(.+)\]: .*$', ret['msg'])
        try:
            datetime.datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.fail('Timestamp format validation failed')

    def test_error_info_non_exception_argument(self):
        self.assertIsNone(logger.error_info(None))

    def test_error_info_bad_exception_argument(self):
        template = "[Exception] Test - Error when getting stacktrace: 'NoneType' object has no attribute '__context__'"
        self.assertEqual(logger.error_info(Exception('Test')), template)

    def test_error_info_correct_exception_argument(self):
        try:
            raise Exception('Test')
        except Exception as e:
            errortext = logger.error_info(e)
        self.assertRegex(errortext, r'^\[Exception\] Test - \S+?\.py:\d+ in \S+$')
