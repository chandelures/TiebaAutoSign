#!venv/bin/python
import unittest
from src.sign import BaiduAutoSign


class AutoSignTest(unittest.TestCase):
    def setUp(self):
        self.baiduautosign = BaiduAutoSign(verbose=False)
        self.baiduautosign.init_loginer()

    def test_is_login(self):
        self.assertEqual(self.baiduautosign.loginer.is_login, True)

    def test_sign(self):
        tbs = self.baiduautosign.get_tbs()
        self.assertNotEqual(tbs, '')
        forums_iter = self.baiduautosign.get_followed_forums()

        forum = next(forums_iter)
        if forum:
            self.assertTrue(self.baiduautosign.sign(forum, tbs))

    def tearDown(self):
        self.baiduautosign.close_loginer()


if __name__ == "__main__":
    unittest.main()
