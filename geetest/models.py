# coding:utf-8


from datetime import datetime

from geetest import mongodb as db


class RecognizeInfo(db.Document):
    """
    若快识别信息
    """
    image = db.StringField(required=True)  # 原始图片base64 encode
    md5 = db.StringField()  # 图片hash值
    im_type = db.IntField()  # 图片类型
    result = db.StringField()  # 识别结果
    record_id = db.StringField()  # 结果ID
    create_time = db.DateTimeField(default=datetime.now())
    update_time = db.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'geetest.RecognizeInfo',
        'ordering': ['-update_time'],
        'strict': False,
    }


class TraceInfo(db.Document):
    """
    验证的轨迹信息
    """
    fid = db.StringField()  # 用于确定本次校验流程的唯一ID
    trace_type = db.StringField()  # 轨迹类型 点选click或者滑块slide
    image = db.StringField()
    point_list = db.ListField()  # 点集 [x_y, ...]
    params = db.DictField()  # 生成轨迹参数
    trace_list = db.ListField()  # 轨迹 [(x,y,ts)...]
    result = db.StringField()  # 验证结果
    create_time = db.DateTimeField(default=datetime.now())
    update_time = db.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'geetest.TraceInfo',
        'ordering': ['-update_time'],
        'strict': False,
    }
