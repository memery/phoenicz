import os
import os.path
import unittest

import admin
import testlib

class IsAdminTest(unittest.TestCase):

    @classmethod
    def setUpClass(AdminTest):
        try:
            os.remove('admins.json.tempbackupfortest')
        except:
            pass
        if os.path.exists('admins.json'):
            os.rename('admins.json', 'admins.json.tempbackupfortest')

    @classmethod
    def tearDownClass(AdminTest):
        try:
            os.remove('admins.json')
        except:
            pass
        if os.path.exists('admins.json.tempbackupfortest'):
            os.rename('admins.json.tempbackupfortest', 'admins.json')

    def setUp(self):
        self.flog = testlib.FakeLogger()

    def set_admins_file(self, data):
        with open('admins.json', 'w', encoding='utf-8') as f:
            f.write(data)

    def assert_fail_and_log(self):
        self.assertFalse(admin.is_admin('test', log=self.flog.log))
        self.assertTrue(self.flog.logged)

    def test_is_admin_valid_user(self):
        nick = 'testnick!blablabla.324.324.890'
        self.set_admins_file('["{}"]'.format(nick))
        self.assertTrue(admin.is_admin(nick, log=self.flog.log))
        self.assertFalse(self.flog.logged)

    def test_is_admin_empty_user(self):
        nick = 'testnick!blablabla.324.324.890'
        self.set_admins_file('["{}"]'.format(nick))
        self.assertTrue(admin.is_admin(nick, log=self.flog.log))
        self.assertFalse(self.flog.logged)

    def test_is_admin_invalid_user(self):
        self.set_admins_file('["blah"]')
        self.assertFalse(admin.is_admin('', log=self.flog.log))
        self.assertFalse(self.flog.logged)

    def test_is_admin_invalid_json_file(self):
        self.set_admins_file('][""{{{.')
        self.assert_fail_and_log()

    def test_is_admin_empty_file(self):
        self.set_admins_file('')
        self.assert_fail_and_log()

    def test_is_admin_empty_json_list(self):
        self.set_admins_file('[]')
        self.assertFalse(admin.is_admin('lol', log=self.flog))
        self.assertFalse(self.flog.logged)

    def test_is_admin_no_file(self):
        try:
            os.remove('admins.json')
        except:
            pass
        self.assert_fail_and_log()


class AdminCommandsTest(unittest.TestCase):

    def setUp(self):
        self.flog = testlib.FakeLogger()

    def generic_admin_command_test(self, command):
        test = lambda cmd: self.assertTrue(admin.parse_admin_command(cmd, 'testbot', log=self.flog.log))
        test('testbot: {}'.format(command))
        test('testbot, {}'.format(command))
        test('testbot:    {}'.format(command))
        self.assertFalse(self.flog.logged)

    def test_reload(self):
        self.generic_admin_command_test('reload')

    def test_restart(self):
        self.generic_admin_command_test('restart')

    def test_quit(self):
        self.generic_admin_command_test('quit')

    def generic_assert_failure(self, text):
        self.assertIsNone(admin.parse_admin_command(text, 'testbot', log=self.flog.log))
        self.assertFalse(self.flog.logged)

    def test_invalid_command(self):
        self.generic_assert_failure('testbot: imma KIL U')
        self.generic_assert_failure('testbot, imma KIL U')
        self.generic_assert_failure('testbot:    imma KIL U')

    def test_invalid_string(self):
        self.generic_assert_failure('imma let you finish')
        self.generic_assert_failure('testbot you are terrible')

    def test_invalid_nick(self):
        self.generic_assert_failure('testbot2: imma KIL U')
        self.generic_assert_failure('testbot2, imma KIL U')
        self.generic_assert_failure('testbot2:    imma KIL U')

    def test_empty_nick(self):
        self.assertIsNone(admin.parse_admin_command('blah blah blah', '', log=self.flog.log))
        self.assertTrue(self.flog.logged)
