import requests
import os
import json

from src.logger import init_logger
from conf import config


class BaiduLogin(object):
    test_login_url = "http://tieba.baidu.com/f/like/mylike"
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                      'ebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }
    cookies_path = config.cookies_path

    def __init__(self, verbose=True) -> None:
        self.session = requests.Session()
        self.logger = init_logger()
        self.is_login = False

        self.verbose = verbose

        self.add_header()
        self.add_cookies()

    def get_cookies(self) -> dict:
        if not os.path.exists(config.cookies_path):
            if self.verbose:
                self.logger.warning("读取cookies失败，请重新配置cookies")
            return {}

        with open(self.cookies_path) as f:
            cookies = json.load(f)

        return cookies

    def add_header(self) -> None:
        self.session.headers = self.headers

    def add_cookies(self) -> None:
        cookies = self.get_cookies()
        for key, val in cookies.items():
            requests.utils.add_dict_to_cookiejar(
                self.session.cookies, {key: val})

    def is_successful(self) -> bool:
        return self.is_login

    def login(self) -> None:
        res = self.session.get(self.test_login_url, allow_redirects=False)

        if res.status_code == 200:
            self.is_login = True
            if self.verbose:
                self.logger.info('登录成功')
        else:
            self.is_login = False
            if self.verbose:
                self.logger.warning("登陆失败")

    def get_session(self) -> requests.Session:
        return self.session

    def close(self) -> None:
        self.session.close()
        self.is_login = False
