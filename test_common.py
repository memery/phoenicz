import common, re, unittest

class CommonTest(unittest.TestCase):

    def test_read_config(self):
        # Try to read a non-existent config. Config is vital
        # so this should blow up.
        with self.assertRaises(Exception):
            common.read_config('')
