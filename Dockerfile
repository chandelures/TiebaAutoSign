FROM python:3.8-alpine

RUN mkdir /sign

WORKDIR /sign

ADD requirements.txt /sign/

RUN apk update \
 && apk add --no-cache gcc musl-dev libxslt-dev \
 && pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /sign/