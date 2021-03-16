from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler

from src.login import BaiduLogin
from src.logger import init_logger
from conf import config


class AutoSign:
    tbs_url = "http://tieba.baidu.com/dc/common/tbs"
    mylike_url = "http://tieba.baidu.com/f/like/mylike"
    sign_url = "http://tieba.baidu.com/sign/add"
    headers = {
        'Host': 'tieba.baidu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                      'ebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }
    max_pages = 100
    hour = config.hour

    def __init__(self):
        """进行初始化"""
        self.scheduler = BlockingScheduler(timezone=config.timezone)
        self.logger = init_logger()

    def get_tbs(self, session):
        """获取登陆时所需的参数"""
        res = session.post(self.tbs_url)
        return res.json().get('tbs')

    def get_followed_forums(self, session):
        """获取关注的贴吧

        Returns:
            关注贴吧名称的列表
        """
        followed_forums = []
        for pn in range(1, self.max_pages):
            params = {
                'pn': pn
            }
            res = session.get(self.mylike_url, params=params)
            html = etree.HTML(res.content)
            forums_in_one_page = html.xpath('//tr/td[1]/a/text()')
            if forums_in_one_page:
                followed_forums.extend(forums_in_one_page)
            else:
                break

        return followed_forums

    def sign(self, session, forum, tbs):
        """对单个贴吧进行签到

        Args:
            forum: 需要进行签到的贴吧名称
            tbs: 签到时所需的参数
        """
        params = {
            'ie': 'utf-8',
            'kw': forum,
            'tbs': tbs
        }
        res = session.post(self.sign_url, params=params)
        data = res.json()
        if data.get("no"):
            self.logger.warning(forum + " >> " + data.get("error"))
        else:
            self.logger.info(forum + "吧签到成功")

    def run_per_day(self):
        """单日签到关注过的贴吧"""
        baidulogin = BaiduLogin()
        baidulogin.login()

        if not baidulogin.is_successful():
            return

        session = baidulogin.get_session()

        self.logger.info("正在获取关注贴吧列表...")
        tbs = self.get_tbs(session)
        followed_forums = self.get_followed_forums(session)
        self.logger.info("获取关注列表成功，开始签到...")

        for followed_forum in followed_forums:
            self.sign(session, followed_forum, tbs)

        baidulogin.close()

    def run(self):
        """实现每日计划签到"""
        self.scheduler.add_job(self.run_per_day, 'cron', hour=self.hour)
        self.scheduler.start()
