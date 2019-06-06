#!/usr/bin/env bash

docker build -f deploy/Dockerfile . -t geetest:v1

docker run -d -it --name="geetest_api" --env FLASK_CONFIG="geetest.config.ProdConfig" --env MONGODB_URI="mongodb://10.8.10.128:27017/spider_db" -v $(pwd):/opt/spider/geetest/ -v /var/log/geetest:/var/log/geetest -p 9000:9000 geetest:v1
