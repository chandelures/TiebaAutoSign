from lxml import etree
import time
from apscheduler.schedulers.blocking import BlockingScheduler

from src.login import BaiduLogin
from src.logger import init_logger
from conf import config


class BaiduAutoSign:
    tbs_url = "http://tieba.baidu.com/dc/common/tbs"
    mylike_url = "http://tieba.baidu.com/f/like/mylike"
    sign_url = "http://tieba.baidu.com/sign/add"

    sign_time_space = 3
    hour = config.hour

    def __init__(self, verbose=True):
        """进行初始化"""
        self.verbose = verbose
        self.scheduler = BlockingScheduler(timezone=config.timezone)
        self.logger = init_logger()
        self.loginer = BaiduLogin()

    def init_loginer(self):
        if not self.loginer.is_successful():
            self.loginer.login()

    def close_loginer(self):
        self.loginer.close()

    def get_tbs(self, session):
        """获取登陆时所需的参数tbs"""
        res = session.post(self.tbs_url)
        tbs = res.json().get('tbs', '')
        if not tbs:
            self.logger.warning('获取tbs失败')
        return tbs

    def get_followed_forums(self, session):
        """获取关注的贴吧

        Returns:
            关注贴吧名称的列表
        """
        pn = 1
        while True:
            params = {
                'pn': pn
            }
            res = session.get(self.mylike_url, params=params)
            html = etree.HTML(res.content)
            forums_in_one_page = html.xpath('//tr/td[1]/a/text()')
            if forums_in_one_page:
                for forum in forums_in_one_page:
                    yield forum
                pn = pn+1
            else:
                break

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

        if not self.verbose:
            return
        data = res.json()

        if data.get("no"):
            self.logger.warning(forum + "吧 >> " + data.get("error"))
        else:
            self.logger.info(forum + "吧签到成功")

    def run_per_day(self):
        """单日签到关注过的贴吧"""
        if not self.loginer.is_successful():
            self.init_loginer()

        session = self.loginer.get_session()

        self.logger.info('开始进行每日签到')
        tbs = self.get_tbs(session)

        for followed_forum in self.get_followed_forums(session):
            time.sleep(self.sign_time_space)
            self.sign(session, followed_forum, tbs)

        self.close_loginer()

    def run(self):
        """实现每日计划签到"""
        self.scheduler.add_job(self.run_per_day, 'cron', hour=self.hour)
        self.scheduler.start()
