# TiebaAutoSign

本项目可以实现帖吧每日自动签到的功能

## 使用

### 配置环境

```shell
$ virtualenv venv

$ source venv/bin/activate

(venv)$ pip install -r requirements.txt
```

### 设置cookies

```shell
(venv)$ python start.py --set-cookies
```

### 开始每日签到

```shell
(venv)$ screen -S tiebasign
(venv)$ python start.py
```