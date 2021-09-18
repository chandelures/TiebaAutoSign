import requests
import os
import json

from src.logger import init_logger
from conf import config


class BaiduLogin(object):
    login_url = "http://tieba.baidu.com/dc/common/tbs"
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                      'ebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }
    cookies_path = config.cookies_path

    def __init__(self, verbose=True):
        self.session = requests.Session()
        self.logger = init_logger()
        self.is_login = False

        self.verbose = verbose

    def get_cookies(self):
        if not os.path.exists(config.cookies_path):
            if self.verbose:
                self.logger.warning("读取cookies失败，请重新配置cookies")
            return {}

        with open(self.cookies_path) as f:
            cookies = json.load(f)

        return cookies

    def add_header(self):
        self.session.headers = self.headers

    def add_cookies(self):
        cookies = self.get_cookies()
        for key, val in cookies.items():
            requests.utils.add_dict_to_cookiejar(
                self.session.cookies, {key: val})

    def is_successful(self):
        return self.is_login

    def login(self):
        self.add_header()
        self.add_cookies()

        res = self.session.get(
            self.login_url, headers=self.headers)

        if res.json().get('is_login'):
            self.is_login = True
            self.logger.info('登录成功')
            return True
        else:
            self.logger.warning("登陆失败")
            return False

    def get_session(self):
        return self.session

    def close(self):
        self.session.close()
        self.is_login = False
