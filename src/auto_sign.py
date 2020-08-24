import requests
from lxml import etree
import json
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

from conf import config


class AutoSign:

    def __init__(self):
        self.urls = config.urls
        self.cookies = json.load(open(config.cookies_path))
        self.headers = config.headers
        self.max_pages = config.max_pages

        self.hour = config.hour

        self.scheduler = BlockingScheduler()
        self.logger = self.__init_logger()

    @staticmethod
    def __init_logger():
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)
        return logger

    def is_login(self):
        r = requests.post(self.urls.get("tbs"), cookies=self.cookies, headers=self.headers)
        data = json.loads(r.text)
        return data.get("is_login")

    def get_tbs(self):
        r = requests.post(self.urls.get("tbs"), cookies=self.cookies, headers=self.headers)
        data = json.loads(r.text)
        return data.get("tbs")

    def get_followed_forums(self):
        followed_forums = []
        for pn in range(1, self.max_pages):
            params = {
                'pn': pn
            }
            r = requests.get(self.urls.get("mylike"), cookies=self.cookies, headers=self.headers, params=params)
            html = etree.HTML(r.content)
            forums_in_one_page = html.xpath('//tr/td[1]/a/text()')
            if forums_in_one_page:
                followed_forums.extend(forums_in_one_page)
            else:
                break
        return followed_forums

    def sign(self, forum, tbs):
        params = {
            'ie': 'utf-8',
            'kw': forum,
            'tbs': tbs
        }
        r = requests.post(self.urls.get("sign"), cookies=self.cookies, headers=self.headers, params=params)
        data = json.loads(r.text)
        if data.get("no"):
            self.logger.error(forum + " >> " + data.get("error"))
        else:
            self.logger.info(forum + "吧签到成功")

    def run_per_day(self):
        if self.is_login():

            self.logger.info("登录成功，开始进行每日自动签到任务")

            self.logger.info("正在获取关注贴吧列表...")
            tbs = self.get_tbs()
            followed_forums = self.get_followed_forums()
            self.logger.info("获取关注列表成功，开始签到...")

            for followed_forum in followed_forums:
                self.sign(followed_forum, tbs)

        else:
            self.logger.error("登录失败，请更换cookies重试")

    def run(self):
        self.scheduler.add_job(self.run_per_day, 'cron', hour=self.hour)
        self.scheduler.start()


if __name__ == "__main__":
    auto_sign = AutoSign()
    auto_sign.run()
