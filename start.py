#!venv/bin/python
# coding=UTF-8
import sys
import getopt
from src.tiebaautosign import TiebaAutoSign
from src.get_cookies import BaiduLogin


def main(argv):
    cookies_file_path = ''
    try:
        opts, args = getopt.getopt(argv, "-h-c:-g", ['help', 'cookies_file=', 'get_cookies'])
    except getopt.GetoptError:
        print('start.py -c <cookies_file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('start.py -c --cookies_file_path=')
            print('start.py -g --get_cookies')
            print('start.py -t --test')
            sys.exit()
        if opt in ('-g', '--get_cookies'):
            baiduLogin = BaiduLogin()
            baiduLogin.save_cookies()
            sys.exit()
        if opt in ('-c', '--cookies_file'):
            cookies_file_path = arg
    if cookies_file_path:
        tieba_auto_sign = TiebaAutoSign(cookies_file_path)
    else:
        tieba_auto_sign = TiebaAutoSign()
    tieba_auto_sign.auto_sign()


if __name__ == '__main__':
    main(sys.argv[1:])
