#!venv/bin/python
# coding=UTF-8
import sys
import getopt
import json

from conf import config
from src.auto_sign import AutoSign


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "-h:-s", ['help', 'set_cookies'])
    except getopt.GetoptError:
        print('start.py -c <cookies_file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('\n')
            print('start.py -s --set_cookies')
            print('start.py -t --test')
            sys.exit()
        if opt in ('-s', '--set_cookies'):
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
