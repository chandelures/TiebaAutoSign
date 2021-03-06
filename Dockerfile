FROM python:3.8-alpine

RUN mkdir /sign \
 && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

WORKDIR /sign

ADD requirements.txt /sign/

RUN apk update \
 && apk add --no-cache gcc musl-dev libxslt-dev tzdata \
 && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && apk del gcc musl-dev tzdata

ADD . /sign/