import os

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

cookies_path = os.path.join(BASE_PATH, 'cookies.json')

headers = {
    'Host': 'tieba.baidu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                  'ebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}

urls = {
    "tbs": "http://tieba.baidu.com/dc/common/tbs",
    "mylike": "http://tieba.baidu.com/f/like/mylike",
    "sign": "http://tieba.baidu.com/sign/add"
}

hour = 23

max_pages = 100
