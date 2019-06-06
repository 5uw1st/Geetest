# coding:utf-8


class CustomError(Exception):
    code = 1001
    msg = "处理失败"

    def __init__(self, msg=None, extra_msg=None):
        if msg:
            self.msg = msg
        if extra_msg:
            self.msg += ", {0}".format(extra_msg)

    def __str__(self):
        return "{0}, code:{1}, msg: {2}".format(self.__class__.__name__, self.code, self.msg)


class LackRequestParam(CustomError):
    code = 2001
    msg = "缺少请求必要参数"


class ResultTypeError(CustomError):
    code = 3001
    msg = "返回结果类型错误"


class RecognitionError(CustomError):
    code = 4001
    msg = "若快识别失败"


class DownloadError(CustomError):
    code = 5001
    msg = "下载失败"


class VerifyError(CustomError):
    code = 6001
    msg = "校验失败"


class GetParamsError(CustomError):
    code = 7001
    msg = "获取相关参数失败"


class UnknownError(CustomError):
    code = 9001
    msg = "未知错误"
