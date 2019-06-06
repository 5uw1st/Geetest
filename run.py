# coding:utf-8

from geetest import create_app
from geetest.api import geetest_bp

app = create_app(logger_name="geetest")

app.register_blueprint(geetest_bp, url_prefix='/geetest/api/v1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
