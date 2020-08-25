FROM python:3.8

RUN mkdir /sign

WORKDIR /sign

ADD requirements.txt /sign/

RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /sign/