FROM python:3.6
MAINTAINER liuli, liuli6@dianrong.com

ENV WORK_DIR=/opt/spider/geetest \
    LOG_PATH=/var/log/geetest

RUN mkdir -p ${WORK_DIR} ${LOG_PATH}

RUN curl --fail -sL -o setup-nodejs https://deb.nodesource.com/setup_8.x \
    && bash setup-nodejs

RUN apt-get install -y nodejs \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${WORK_DIR}

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . .
EXPOSE 9000
CMD ["sh", "-c", "python run.py"]