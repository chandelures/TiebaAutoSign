# coding=UTF-8
import sys
import getopt
from tiebaautosign import TiebaAutoSign


def main(argv):
    cookies_file_path = ''
    try:
        opts, args = getopt.getopt(argv, "-h-t:-c:", ['help', 'test', 'cookies_file='])
    except getopt.GetoptError:
        print('start.py -c <cookies_file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('start.py -c <cookies_file_path>')
            sys.exit()
        if opt in ('-t', '--test'):
            if cookies_file_path:
                tieba_auto_sign = TiebaAutoSign(cookies_file_path)
            else:
                tieba_auto_sign = TiebaAutoSign()
            tieba_auto_sign.test()
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
