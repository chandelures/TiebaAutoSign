#!venv/bin/python
import unittest
from src.login import BaiduLogin
from src.sign import AutoSign


class AutoSignTest(unittest.TestCase):
    def setUp(self):
        self.baiduLogin = BaiduLogin(verbose=False)

    def test_is_login(self):
        self.assertEqual(self.baiduLogin.login(), True)

    def tearDown(self):
        self.baiduLogin.close()


if __name__ == "__main__":
    unittest.main()
