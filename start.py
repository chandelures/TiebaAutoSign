#!venv/bin/python
# coding=UTF-8
import sys
import os
import getopt
import json

from conf import config
from src.sign import BaiduAutoSign


def usage():
    print('Usage:')
    print('  start.py -h --help')
    print('  start.py -s --set-cookies')
    print('  start.py -t --test')
    print()
    print('https://github.com/chandelures/TiebaAutoSign.git')
    print()


def main(argv):
    try:
        opts, _ = getopt.getopt(
            argv, "-h-t-s", ['help', 'test', 'set-cookies'])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)
    for opt, _ in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        if opt in ('-t', '--test'):
            os.system('python -m unittest')
            sys.exit()
        if opt in ('-s', '--set-cookies'):
            BDUSS = input("BDUSS: ")
            STOKEN = input("STOKEN: ")
            cookies = {
                "BDUSS": BDUSS,
                "STOKEN": STOKEN
            }
            with open(config.cookies_path, "w") as f:
                f.write(json.dumps(cookies, indent=4))
            sys.exit()

    auto_sign = BaiduAutoSign()
    auto_sign.run()


if __name__ == '__main__':
    main(sys.argv[1:])
