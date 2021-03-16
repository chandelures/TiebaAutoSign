import os

# 主目录
BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 存放cookies的位置
cookies_path = os.path.join(BASE_PATH, 'cookies.json')

# 时区设定
timezone = "Asia/Shanghai"

# 每天何时进行签到
hour = 23
