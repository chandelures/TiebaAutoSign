FROM python:3.8

RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && apt-get update \
    && apt-get -y install google-chrome-stable \
    && apt-get -y install npm \
    && npm install -y chromedriver -g \
    && mkdir /sign

WORKDIR /sign

ADD requirements.txt /sign/

RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /sign/

