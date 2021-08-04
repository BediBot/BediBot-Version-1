import unittest
from commands import _email

class email_module_test(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_key_generation(self):
        key = _email.get_unique_key()
        assert len(key) == 10
