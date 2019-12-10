# coding=utf-8  
import json
import re
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
import sys
import getopt


class TiebaAutoSign:
    def __init__(self, cookies_file_path):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = Chrome(options=options)
        self.driver.implicitly_wait(20)
        self.driver.delete_all_cookies()
        self.tieba_url = "https://tieba.baidu.com/"
        self.cookies_file_path = cookies_file_path
        self.sign_url = 'https://tieba.baidu.com/sign/add'

    def add_cookies(self):
        self.driver.get(self.tieba_url)
        with open(self.cookies_file_path, "r") as fp:
            list_cookies = json.loads(fp.readline())
            for cookie in list_cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                self.driver.add_cookie(cookie)

    def get_forum_name_list(self):
        self.add_cookies()
        self.driver.get(self.tieba_url)
        content = self.driver.page_source
        pattern = re.compile(r"\"user_id\"[^}]*\"is_sign\":0")
        forum_info_list = pattern.findall(content)
        forum_name_list = []
        for forum_info in forum_info_list:
            json_item = json.loads('{' + forum_info + '}')
            forum_name = json_item['forum_name']
            forum_name_list.append(forum_name)
        return forum_name_list

    def auto_sign(self):
        success = 0
        for forum_name in self.get_forum_name_list():
            sign_data = {
                'ie': 'utf-8',
                'kw': forum_name,
                'tbs': '6868ce0283f2fb151561865643'
            }
            sign_res = self.driver.request('POST', self.sign_url, data=sign_data)
            if eval(sign_res.text)["no"] == 0:
                print("{}吧签到成功！".format(forum_name))
                success = success + 1
        print('共签到成功{}个贴吧。'.format(success))
        self.driver.close()
        self.driver.quit()


def main(argv):
    cookies_file_path = ''
    try:
        opts, args = getopt.getopt(argv, "hc:")
    except getopt.GetoptError:
        print('start.py -c <cookies_file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('start.py -c <cookies_file_path>')
            sys.exit()
        elif opt == '-c':
            cookies_file_path = arg
        else:
            print('start.py -c <cookies_file_path>')
            sys.exit()
    print('cookies_file_path:' + cookies_file_path)
    tieba_auto_sign = TiebaAutoSign(cookies_file_path)
    tieba_auto_sign.auto_sign()


if __name__ == '__main__':
    main(sys.argv[1:])
