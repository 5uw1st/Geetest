# coding:utf-8
import json
import re
import time
import uuid
from base64 import b64encode
from collections import defaultdict
from hashlib import md5
from urllib.parse import urlparse

import requests

from geetest.tools.ruokuai import RClient, RUOKUAI_CONFIG

SESSION_DICT = defaultdict(dict)

default_headers = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def get_uid():
    return str(uuid.uuid1())


def get_timestamp():
    return int(time.time() * 1000)


def base64_encode(content):
    if isinstance(content, str):
        content = content.encode()
    return b64encode(content).decode()


def to_json(json_str):
    json_str = re.sub(r'^.*?\(\{', '{', json_str)
    json_str = re.sub(r'\}\)[^\)]*?$', '}', json_str)
    try:
        return json.loads(json_str)
    except:
        return {}


def get_md5(text):
    if isinstance(text, str):
        text = text.encode()
    return md5(text).hexdigest()


rc = RClient(**RUOKUAI_CONFIG)


def do_recognition(image, im_type=None, timeout=60):
    return rc.rk_create(im=image, im_type=im_type, timeout=timeout)


def report_error(im_id):
    return rc.rk_report_error(im_id=im_id)


def download(url, method="GET", data=None, headers=None, params=None, get_json=True, cookies=None, get_bytes=False,
             proxies=None):
    host = urlparse(url).netloc
    if method.upper() == "GET":
        request = requests.get
    else:
        request = requests.post
    headers = headers or default_headers
    if cookies:
        SESSION_DICT.get(host, {}).pop("__jsl_clearance", "")
        cookies.update(SESSION_DICT.get(host))
    else:
        # cookies = SESSION_DICT.get(host)
        pass
    response = request(url, data=data, headers=headers, params=params, cookies=cookies, proxies=proxies)
    if get_json:
        result = response.json()
    elif get_bytes:
        result = response.content
    else:
        result = response.text
    new_cookies = response.cookies.get_dict()
    new_cookies.pop("HttpOnly", "")
    new_cookies.update(cookies or {})
    SESSION_DICT[host].update(new_cookies)
    return result


if __name__ == '__main__':
    r = get_md5("123456")
    print(r)
