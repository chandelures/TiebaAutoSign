# coding=utf-8
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
import re
import logging


class TiebaAutoSign(object):
    """
    实现贴吧一键签到

    Attributes:
        cookies_file_path: 存放登陆所需cookies文件的路径
        driver：selenium.webdriver的一个实例化
        tieba_url: 百度贴吧主页URL
        sign_url: 百度贴吧签到URL
    """

    @staticmethod
    def init_driver():
        """初始化driver"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)
        driver.implicitly_wait(20)
        driver.delete_all_cookies()
        return driver

    @staticmethod
    def init_logger():
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s]-%(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)
        return logger

    def __init__(
            self,
            cookies_file_path="./cookies.txt",
            tieba_url="https://tieba.baidu.com/",
            sign_url='https://tieba.baidu.com/sign/add'):
        """初始化"""
        self.driver = self.init_driver()
        self.logger = self.init_logger()
        self.tieba_url = tieba_url
        self.cookies_file_path = cookies_file_path
        self.sign_url = sign_url

    def add_cookies(self):
        """为driver添加cookies"""
        self.driver.get(self.tieba_url)
        self.logger.info("开始读取cookies信息")
        try:
            with open(self.cookies_file_path, "r") as fp:
                list_cookies = json.loads(fp.readline())
                for cookie in list_cookies:
                    if 'expiry' in cookie:
                        del cookie['expiry']
                    self.driver.add_cookie(cookie)
        except FileNotFoundError:
            self.logger.warning("未发现cookies文件，请输入正确的路径")

    def get_forum_name_list(self):
        """获取用户关注且并未签到的贴吧列表"""
        if self.is_log_in():
            self.logger.info("开始获取关注且未签到的贴吧列表")
            forum_name_list = []
            content = self.driver.page_source
            pattern = re.compile(r"\"user_id\"[^}]*\"is_sign\":0")
            forum_info_list = pattern.findall(content)
            for forum_info in forum_info_list:
                json_item = json.loads('{' + forum_info + '}')
                forum_name = json_item['forum_name']
                forum_name_list.append(forum_name)
            return forum_name_list
        else:
            self.logger.warning("获取贴吧列表失败。")
            self.exit_driver()

    def exit_driver(self):
        """退出driver"""
        self.driver.close()
        self.driver.quit()

    def is_log_in(self):
        """判断是否成功登录"""
        self.add_cookies()
        self.driver.get(self.tieba_url)
        try:
            self.driver.find_element_by_id('my_tieba_mod')
            self.logger.info("登录成功。")
            return True
        except NoSuchElementException:
            self.logger.warning("登陆失败。")
            return False

    def auto_sign(self):
        """实现一键签到"""
        self.logger.info("开始进行一键签到......")
        success = 0
        for forum_name in self.get_forum_name_list():
            sign_data = {
                'ie': 'utf-8',
                'kw': forum_name,
                'tbs': '6868ce0283f2fb151561865643'
            }
            sign_res = self.driver.request(
                'POST', self.sign_url, data=sign_data)
            if eval(sign_res.text)["no"] == 0:
                self.logger.info("{}吧签到成功！".format(forum_name))
                success = success + 1
        self.logger.info('一键签到结束，共签到成功{}个贴吧。'.format(success))
        self.exit_driver()