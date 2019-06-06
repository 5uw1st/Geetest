Geetest校验服务：
===
1.项目介绍：
---
 - **背景**：个别爬虫项目中依赖geetest破解服务，为防止第三方服务不可以，故自研该破解服务，对外提供轨迹生成接口和校验接口。

2.项目依赖：
---
 - python3.6
 - mongodb
 - flask

3.日志目录：
---
    /var/log/geetest/

4.健康检查：
---
    /geetest/api/v1/check_healthy

5.部署：
---
1.Build Dockerfile：
```bash
docker build -f deploy/Dockerfile . -t geetest:v1
```
2.Run geetest api:
```bash
docker run -d -it --name="geetest_api" --env FLASK_CONFIG="geetest.config.ProdConfig" -v $(pwd):/opt/spider/geetest/ -v /var/log/geetest:/var/log/geetest -p 9000:9000 geetest:v1
```




