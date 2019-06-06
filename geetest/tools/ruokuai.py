#!/usr/bin/env python
# coding:utf-8

from hashlib import md5

import requests

RUOKUAI_CONFIG = {
    'username': 'xxx',
    'password': 'xxx',
    'soft_id': 'xxx',
    'soft_key': 'xxx',
    'im_type': 1111
}


class RClient(object):

    def __init__(self, username, password, soft_id, soft_key, im_type):
        self.username = username
        self.__password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.__soft_key = soft_key
        self.im_type = im_type
        self.__base_params = {
            'username': self.username,
            'password': self.__password,
            'softid': self.soft_id,
            'softkey': self.__soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type=None, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        im_type = im_type or self.im_type
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.__base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.__base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    # {'Result': '264,266.158,55.55,157.91,256.290,142', 'Id': '1b75d8f6-b680-49f6-9fe4-e9b08bcb0a75'}
    rc = RClient(**RUOKUAI_CONFIG)
    im = open('../data/gsxt.jpg', 'rb').read()
    print(rc.rk_create(im))
