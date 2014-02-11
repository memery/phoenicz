import testlib
import main

import unittest

class StateKeeperTest(unittest.TestCase):

    def setUp(self):
        self.flog = testlib.FakeLogger()
        self.flog.logged = False
        self.settings = {'irc': {
                        'channel': '#channel',
                        'server': 'irc.example.org',
                        'port': 6667,
                        'ssl': True,
                        'reconnect_delay': 12,
        }}

    def assert_failed_to_validate(self, settings):
        self.assertFalse(main.valid_settings(settings, log=self.flog.log))
        self.assertTrue(self.flog.logged)

    def assert_validated(self, settings):
        self.assertTrue(main.valid_settings(settings, log=self.flog.log))
        self.assertFalse(self.flog.logged)

    def test_validate_broken_settings_empty_dict(self):
        self.assert_failed_to_validate({})

    def test_validate_broken_settings_empty_string(self):
        self.assert_failed_to_validate('')

    def test_validate_invalid_settings(self):
        self.settings['nick'] = 1
        self.assert_failed_to_validate(self.settings)

    def test_validate_incomplete_settings(self):
        self.assert_failed_to_validate(self.settings)

    def test_validate_valid_settings(self):
        self.settings['irc']['nick'] = 'nick'
        self.assert_validated(self.settings)

    def test_validate_extra_settings(self):
        self.settings['irc']['nick'] = 'nick'
        self.settings['irc']['lag'] = 'don\'t'
        self.assert_validated(self.settings)
