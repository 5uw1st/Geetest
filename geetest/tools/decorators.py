# coding:utf-8

import json
from functools import wraps

from flask import request, make_response, current_app

from geetest.exceptions import ResultTypeError, UnknownError, CustomError


def parse_request(is_api=True):
    def _handle(func):
        @wraps(func)
        def __handle():
            code, msg, data = -1, "{0}{1}{2}", {}
            func_name = func.__name__
            current_app.logger.info(">>>Start handle api:{}".format(func_name))
            msg_base = func.__doc__.split("\n")[1].strip() or "处理"
            try:
                data = func(request) or {}
                if not isinstance(data, dict):
                    raise ResultTypeError
                code = data.pop("code", 0)
                msg = data.pop("msg", msg.format(msg_base, "成功", ""))
            except Exception as e:
                data = {}
                code = e.code if hasattr(e, "code") else code
                error = ", Error: {0}".format(e.msg if hasattr(e, "msg") else str(e))
                msg = msg.format(msg_base, "失败", error)
                current_app.logger.exception("===>>>Handle api {0} error:{0}".format(func_name, msg))
            finally:
                if is_api:
                    result = {
                        "code": code,
                        "msg": msg,
                        "data": data
                    }
                    response = make_response(json.dumps(result))
                    response.headers["Content-Type"] = "application/json;charset=utf-8"
                else:
                    response = make_response(data)
                return response

        return __handle

    return _handle


def catch_exception(func):
    def _handle(self, *args, **kwargs):
        func_name = func.__name__
        try:
            self.logger.debug("===>Handle func:{0}, challenge:{1}".format(func_name, self.challenge))
            result = func(self, *args, **kwargs)
        except CustomError as e:
            self.logger.exception("===>>>Handle error, func:{0},code:{1},msg:{2}".format(func_name, e.code, e.msg))
            raise e
        except Exception as e:
            self.logger.exception("===>>>Handle error, func:{0}".format(func_name))
            raise UnknownError(extra_msg=str(e))
        else:
            return result

    return _handle
