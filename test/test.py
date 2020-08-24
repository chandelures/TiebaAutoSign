#!venv/bin/python
import unittest
from src.auto_sign import AutoSign


class AutoSignTest(unittest.TestCase):
    def setUp(self):
        self.autoSign = AutoSign()

    def test_is_login(self):
        is_login = self.autoSign.is_login()
        self.assertEqual(is_login, True)


if __name__ == "__main__":
    unittest.main()
