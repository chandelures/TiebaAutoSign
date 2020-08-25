#!venv/bin/python
# coding=UTF-8
import sys
import getopt
import json

from conf import config
from src.auto_sign import AutoSign


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "-ht:-s", ['help', 'test', 'set-cookies'])
    except getopt.GetoptError:
        print('start.py -h --help')
        print('start.py -s --setcookies')
        print('start.py -t --test')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('start.py -h --help')
            print('start.py -s --set-cookies')
            print('start.py -t --test')
            sys.exit()
        if opt in ('-t', '--test'):
            auto_sign = AutoSign()
            if auto_sign.is_login():
                print("登录成功，cookies可以正常使用")
            else:
                print("登陆失败，请重新更换cookies")
            sys.exit()
        if opt in ('-s', '--set-cookies'):
            BDUSS = input("BUDSS: ")
            STOKEN = input("STOKEN: ")
            cookies = {
                "BDUSS": BDUSS,
                "STOKEN": STOKEN
            }
            with open(config.cookies_path, "w") as f:
                f.write(json.dumps(cookies, indent=4))
            sys.exit()

    auto_sign = AutoSign()
    auto_sign.run()


if __name__ == '__main__':
    main(sys.argv[1:])
