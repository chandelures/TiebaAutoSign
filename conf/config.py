import os

# 主目录
BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 存放cookies的位置
cookies_path = os.path.join(BASE_PATH, 'cookies.json')

# 登录时所需的headers
headers = {
    'Host': 'tieba.baidu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                  'ebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}

# 登录时所需的url地址
urls = {
    "tbs": "http://tieba.baidu.com/dc/common/tbs",
    "mylike": "http://tieba.baidu.com/f/like/mylike",
    "sign": "http://tieba.baidu.com/sign/add"
}

#时区设定
timezone = "Asia/Shanghai"
# 每天何时进行签到
hour = 23

# 获取关注贴吧的最大页数，每页20个贴吧
max_pages = 100
