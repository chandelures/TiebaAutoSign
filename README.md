# TiebaAutoSign

Sign up in [Baidu Tieba](https://tieba.baidu.com/) automatically.

## Usage

### Enviroment Set up

```shell
$ python -m venv venv

$ source venv/bin/activate

(venv)$ pip install -r requirements.txt
```

### Add cookies

First, you should get two cookies named "BDUSS" and "STOKEN" from the browser.

```shell
(venv)$ python start.py --set-cookies
```

### Start Sign up

```shell
(venv)$ python start.py
```
