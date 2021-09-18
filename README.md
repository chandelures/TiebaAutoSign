# TiebaAutoSign

本项目可以实现帖吧每日自动签到的功能

## 使用

### 配置环境

```shell
$ virtualenv venv

$ source venv/bin/activate

(venv)$ pip install -r requirements.txt
```

### 配置 cookies

在项目的根目录创建名为 cookies.json 的文件, 并填入 BDUSS 和 STOKEN 两个 cookie 的键值, 例如:

```json
{
  "BDUSS": "****",
  "STOKEN": "****"
}
```

### 测试脚本是否可以正常运行

```shell
(venv) $ ./start.py -t
```

### 开始每日签到

```shell
(venv)$ screen -S tiebasign
(venv)$ python start.py
```

脚本保持时刻运行的状态。
