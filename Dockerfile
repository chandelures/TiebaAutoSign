FROM python:3.8-alpine

RUN mkdir /sign \
 && echo "http://mirrors.aliyun.com/alpine/v3.8/main/" > /etc/apk/repositories \
 && echo "http://mirrors.aliyun.com/alpine/v3.8/community/" >> /etc/apk/repositories

WORKDIR /sign

ADD requirements.txt /sign/

RUN apk update \
 && apk add --no-cache gcc musl-dev libxslt-dev bash \
 && pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /sign/