# coding:utf-8

from flask import Blueprint, current_app

from geetest.exceptions import LackRequestParam
from geetest.gsxt import GsxtCrack
from geetest.tools.decorators import parse_request
from geetest.tools.utils import get_uid
from geetest.trace import generate_mouse_trace_between_two_point

geetest_bp = Blueprint("geetest_api", __name__)
gsxt_online = GsxtCrack(debug=False, use_proxy=True)
gsxt_test = GsxtCrack(debug=False, use_proxy=False)


@geetest_bp.route('/check_healthy', methods=['GET', 'POST'])
def check_healthy():
    return "ok"


@geetest_bp.route('/generate_trace', methods=['POST'])
@parse_request()
def generate_trace(request):
    """
    生成两点之间的鼠标轨迹
    :param request: 请求对象
    :return: list 轨迹列表 [(x,y,ts)...]
    """
    request_params = request.json
    start_point = request_params.get("start_point", ())
    if len(start_point) == 0:
        raise LackRequestParam(extra_msg="start_point")
    end_point = request_params.get("end_point", ())
    if len(end_point) == 0:
        raise LackRequestParam(extra_msg="end_point")
    current_app.logger.info(">>>start_point: {0}, end_point: {1}".format(start_point, end_point))
    start_time = request_params.get("start_time")
    rps = request_params.get("rps", [])
    dense_radio = request_params.get("dense_radio")
    time_rng = request_params.get("time_rng")
    trace_list = generate_mouse_trace_between_two_point(point_a=start_point, point_b=end_point, start_time=start_time,
                                                        time_rng=time_rng, dense_radio=dense_radio, rp=rps, show=False)
    return {"trace_list": trace_list, "tid": get_uid()}


@geetest_bp.route('/get_challenge', methods=['POST'])
@parse_request()
def get_challenge(request):
    """
    获取challenge参数
    :param request: 请求对象
    :return: dict 相关参数
    """
    gt, challenge, val = gsxt_test.get_challenge()
    return {"gt": gt, "challenge": challenge, "validate": val}


@geetest_bp.route('/validate', methods=['POST'])
@parse_request()
def validate(request):
    """
    校验
    :param request: 请求对象
    :return: dict 校验结果
    """
    request_params = request.json
    gt = request_params.get("gt", "")
    challenge = request_params.get("challenge", "")
    proxy = request_params.get("proxy")
    if not gt:
        raise LackRequestParam(extra_msg="gt")
    if not challenge:
        raise LackRequestParam(extra_msg="challenge")
    val = gsxt_online.do_validate(gt=gt, challenge=challenge, logger=current_app.logger, proxy=proxy)
    return {"validate": val}
