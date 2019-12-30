#!venv/bin/python
import unittest
from src.tiebaautosign import TiebaAutoSign
from src.get_cookies import BaiduLogin


class AutoSignTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tiebaAutoSign = TiebaAutoSign()
        self.baiduLogin = BaiduLogin()

    def test_is_log_in(self):
        is_log_in = self.tiebaAutoSign.is_log_in()
        self.assertEqual(is_log_in, True)


if __name__ == "__main__":
    unittest.main()
