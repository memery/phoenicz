import statekeeper

import unittest


class StateKeeperTest(unittest.TestCase):

    def setUp(self):
        self.state = statekeeper.StateKeeper()
        self.key, self.value = 'test', 123

    def test_caller_id(self):
        self.assertEqual(self.state._caller_id(), __file__, 'Caller ID is incorrect')

    def test_set_get(self):
        self.state[self.key] = self.value
        self.assertEqual(self.state[self.key], self.value)

    def test_invalid_value(self):
        with self.assertRaises(KeyError):
            self.state['invalidkey']

    def test_delete_value(self):
        self.state[self.key] = self.value
        del self.state[self.key]
        self.assertTrue(self.key not in self.state)

    def test_in_operator(self):
        self.state[self.key] = self.value
        self.assertTrue(self.key in self.state)

    def test_shared_dict_set_get(self):
        self.state.shared[self.key] = self.value
        self.assertEqual(self.state.shared[self.key], self.value)

    def test_remove_shared(self):
        with self.assertRaises(AttributeError):
            self.state.shared = None
