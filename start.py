#!/usr/bin/env python
# coding=UTF-8
import sys
import os
import getopt

from src.sign import BaiduAutoSign


def usage() -> None:
    print('Usage:')
    print('  start.py -h --help')
    print('  start.py -s --set-cookies')
    print('  start.py -t --test')
    print()
    print('https://github.com/chandelures/TiebaAutoSign.git')
    print()


def test() -> None:
    os.system('python -m unittest')


def main(argv) -> None:
    try:
        opts, _ = getopt.getopt(
            argv, "-h-t-s", ['help', 'test', 'set-cookies'])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)
    for opt, _ in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-t', '--test'):
            test()
        return

    auto_sign = BaiduAutoSign()
    auto_sign.run()


if __name__ == '__main__':
    main(sys.argv[1:])
