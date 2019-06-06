# coding:utf-8

import os
import re
import execjs
import json

BASE_PATH = os.path.dirname(__file__)

DATA_PATH = os.path.join(BASE_PATH, "data")
JS_PATH = os.path.join(BASE_PATH, "js")

file_path_dict = {
    "txt": DATA_PATH,
    "js": JS_PATH
}


def _get_file_path(filename):
    file_type = filename.rsplit(".", 1)[-1]
    return os.path.join(file_path_dict.get(file_type), filename)


def read_file_content(filename):
    file_path = _get_file_path(filename)
    with open(file_path, "r") as f:
        return f.read()


def save_file(filename, content):
    file_path = _get_file_path(filename)
    with open(file_path, "w") as f:
        f.write(content)


def _format_code(pattern, keywords, js_code):
    key_dict = {str(index): keyword for index, keyword in enumerate(keywords)}

    def replace(x):
        ii = x.group(1)
        ret = key_dict[ii]
        return "'{0}'".format(ret)

    ret_js = pattern.sub(replace, js_code)
    return ret_js


def _get_keywords(filename):
    text = read_file_content(filename)
    split_str = "###"
    return text.split(split_str)


def _save_keywords(keywords, save_file_name):
    file_path = _get_file_path(filename=save_file_name)
    with open(file_path, "w") as f:
        for index, key in enumerate(keywords):
            line = "{0} ==> {1}\n".format(index, key)
            f.write(line)


def format_fullpage_code():
    pattern = re.compile(r'B5Y\.[ec]78\((\d+)\)')
    keywords = _get_keywords(filename="fullpage_keywords_str.txt")
    fullpage_code = read_file_content(filename="fullpage.js")
    fmt_code = _format_code(pattern=pattern, keywords=keywords, js_code=fullpage_code)
    save_file(filename="fullpage_format.js", content=fmt_code)


def format_slide_code():
    # vars = ["n45", "W0U", "u45", "u45"]
    vars = ["u5M", "p5M", "k0q", "R0q"]
    pattern_str = "(?:g0q|J0q)\.(?:{0})\((\d+)\)".format("|".join(vars))
    pattern = re.compile(pattern_str)
    keywords = _get_keywords(filename="slide_keywords_str_7.4.3.txt")
    _save_keywords(keywords, save_file_name="slide_keywords_7.4.3.txt")
    slide_code = read_file_content(filename="slide_7.4.3.js")
    fmt_code = _format_code(pattern=pattern, keywords=keywords, js_code=slide_code)
    save_file(filename="slide_format_7.4.3.js", content=fmt_code)


def format_click_code():
    # vars = ["x45", "p45", "C7B", "h7B"]
    # pattern_str = "(?:F45|n45)\.(?:{0})\((\d+)\)".format("|".join(vars))
    vars = ["b8m", "t3p", "t3p", "R8m"]
    pattern_str = "(?:w3p|c3p)\.(?:{0})\((\d+)\)".format("|".join(vars))
    pattern = re.compile(pattern_str)
    keywords = _get_keywords(filename="click_keywords_str_2.6.4.txt")
    _save_keywords(keywords, save_file_name="click_keywords_2.6.4.txt")
    click_code = read_file_content(filename="click_2.6.4.js")
    fmt_code = _format_code(pattern=pattern, keywords=keywords, js_code=click_code)
    save_file(filename="click_format_2.6.4.js", content=fmt_code)


def get_y5Y():
    from collections import defaultdict

    def tree():
        return defaultdict(tree)

    G5Y = 39
    o5Y = 12
    T5Y = 2
    H5Y = tree()
    b5Y = 0
    t5Y = 0
    a5Y = 0
    count = 0
    while T5Y != 10:
        count += 1
        if T5Y == 12:
            a5Y += 1
            T5Y = 8
            continue
        elif T5Y == 2:
            T5Y = 1
            continue
        elif T5Y == 4:
            i4 = (b5Y + o5Y) % G5Y
            H5Y[i4] = tree()
            T5Y = 3
            continue
        elif T5Y == 6:
            T5Y = 14 if t5Y >= 0 else 12
            continue
        elif T5Y == 13:
            t5Y -= 1
            T5Y = 6
            continue
        elif T5Y == 14:
            i14 = (t5Y + o5Y * a5Y) % G5Y
            H5Y[a5Y][i14] = H5Y[t5Y]
            T5Y = 13
            continue
        elif T5Y == 1:
            b5Y = 0
            T5Y = 5
            continue
        elif T5Y == 11:
            return H5Y, count
        elif T5Y == 9:
            a5Y = 0
            T5Y = 8
            continue
        elif T5Y == 5:
            T5Y = 4 if b5Y < G5Y else 9
            continue
        elif T5Y == 7:
            t5Y = G5Y - 1
            T5Y = 6
            continue
        elif T5Y == 3:
            b5Y += 1
            T5Y = 5
            continue
        elif T5Y == 8:
            T5Y = 7 if a5Y < G5Y else 11
            continue


def _do_rsa_encrypt(msg, n, e):
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    pubkey = RSA.construct((n, e))
    cipher = PKCS1_v1_5.new(pubkey)
    ct = cipher.encrypt(msg.encode())
    return ct.hex()


def _do_aes_encrypt(msg, key, iv):
    from pkcs7 import PKCS7Encoder
    from Crypto.Cipher import AES
    msg = PKCS7Encoder().encode(msg)
    cipher = AES.new(key, AES.MODE_CBC, iv[:16])
    return cipher.encrypt(msg.encode())


d8_code = read_file_content(filename="custom.js")
exec_obj = execjs.compile(d8_code)


def ce_encrypt(ctx, bytes_input):
    array_input = [bytes_input[i] for i in range(len(bytes_input))]
    return ctx.call("ce_encrypt", array_input)


def hb_encrypt(ctx, message):
    return ctx.call("hb_encrypt", message)


def m5_encrypt(ctx, message, arr, mstr):
    arr = list(map(lambda x: int(x), arr))
    return ctx.call("m5_encrypt", message, arr, mstr)


def hb_trace_encrypt(ctx, trace_list):
    return ctx.call("hb_trace_encrypt", trace_list)


slide_exec_obj = execjs.compile(read_file_content(filename="custom_slide.js"))


def hb_slide_trace_encrypt(ctx, trace_list):
    return ctx.call("hb_slide_trace_encrypt", trace_list)


def j5_encrypt(ctx, vint, vstr):
    return ctx.call("j5_encrypt", vint, vstr)


click_exec_obj = execjs.compile(read_file_content(filename="custom_click.js"))


def hb_click_trace_encrypt(ctx, trace_list):
    tmp = ctx.call("Kb", trace_list)
    return ctx.call("Lb", tmp)


def generate_aes_key():
    import random

    def ge():
        x = int(65536 * (1 + random.random())) | 0
        return hex(x)[-4:]

    return "".join([ge(), ge(), ge(), ge()])


def rsa_encrypt(ctx, message=None):
    if isinstance(message, dict):
        message = json.dumps(message)
    return ctx.call("rsa_encrypt", message)


def aes_encrypt(message=None, aes_key=None):
    aes_key = aes_key or "bc2f316d485dc638"
    iv = "0000000000000000"
    message = message or '{"gt":"62756445cd524543f5a16418cd920ffd","challenge":"eea8219f0f2d4b394b8dcdd89bbf659c","offline":false,"product":"bind","width":"300px","protocol":"http://","click":"/static/js/click.2.6.4.js","voice":"/static/js/voice.1.1.4.js","beeline":"/static/js/beeline.1.0.1.js","geetest":"/static/js/geetest.6.0.9.js","static_servers":["static.geetest.com/","dn-staticdown.qbox.me/"],"slide":"/static/js/slide.7.4.3.js","fullpage":"/static/js/fullpage.8.6.1.js","aspect_radio":{"slide":103,"click":128,"voice":128,"pencil":128,"beeline":50},"pencil":"/static/js/pencil.1.0.1.js","type":"fullpage","cc":8,"ww":true,"i":"3668!!17548!!CSS1Compat!!50!!-1!!-1!!-1!!-1!!3!!-1!!-1!!-1!!9!!9!!-1!!9!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!9!!-1!!4!!-1!!-1!!1600!!0!!1600!!0!!1920!!287!!1920!!1080!!zh-CN!!zh-CN,zh!!-1!!1!!24!!Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36!!1!!1!!1920!!1080!!1920!!1080!!1!!1!!1!!-1!!Linux x86_64!!0!!-8!!04f7eb201d3cc0991ab472b909027874!!2e2d74424f3cc8b7d88f16655f148d75!!internal-pdf-viewer,mhjfbmdgcfjbbpaeojofohoefgiehjai,internal-nacl-plugin!!0!!-1!!0!!8!!Arial,Courier,CourierNew,Helvetica,Times,TimesNewRoman!!1542593800616!!2,3782,0,0,0,0,0,3,82,6,3,3,11,239,239,330,335,335,335,-1!!-1!!-1!!61!!6!!-1!!-1!!14!!false!!false"}'
    return _do_aes_encrypt(message, aes_key, iv)


def get_Q0o(ctx, message=None, aes_key=None):
    if isinstance(message, dict):
        message = json.dumps(message)
    bytes_input = aes_encrypt(message, aes_key)
    result = ce_encrypt(ctx=ctx, bytes_input=bytes_input)
    return result


def get_i_dict(value_str=None):
    key_list = ["textLength", "HTMLLength", "documentMode", "A", "ARTICLE", "ASIDE", "AUDIO", "BASE", "BUTTON",
                "CANVAS", "CODE", "IFRAME", "IMG", "INPUT", "LABEL", "LINK", "NAV", "OBJECT", "OL", "PICTURE", "PRE",
                "SECTION", "SELECT", "SOURCE", "SPAN", "STYLE", "TABLE", "TEXTAREA", "VIDEO", "screenLeft", "screenTop",
                "screenAvailLeft", "screenAvailTop", "innerWidth", "innerHeight", "outerWidth", "outerHeight",
                "browserLanguage", "browserLanguages", "systemLanguage", "devicePixelRatio", "colorDepth", "userAgent",
                "cookieEnabled", "netEnabled", "screenWidth", "screenHeight", "screenAvailWidth", "screenAvailHeight",
                "localStorageEnabled", "sessionStorageEnabled", "indexedDBEnabled", "CPUClass", "platform",
                "doNotTrack", "timezone", "canvas2DFP", "canvas3DFP", "plugins", "maxTouchPoints", "flashEnabled",
                "javaEnabled", "hardwareConcurrency", "jsFonts", "timestamp", "performanceTiming", "internalip",
                "mediaDevices", "DIV", "P", "UL", "LI", "SCRIPT", "deviceorientation", "touchEvent"]
    # value_list = value_str.split("!!")
    value_list = ["11506", "35862", "CSS1Compat", "122", "-1", "-1", "-1", "-1", "3", "-1", "-1", "-1", "2", "19", "-1",
                  "10", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "67", "3", "1", "-1", "-1", "1600", "0", "1600",
                  "0", "1920", "242", "1920", "1080", "zh-CN", "zh-CN,zh", "-1", "1", "24",
                  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36…ML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                  "1", "1", "1920", "1080", "1920", "1080", "1", "1", "1", "-1", "Linux x86_64", "0", "-8",
                  "04f7eb201d3cc0991ab472b909027874", "2e2d74424f3cc8b7d88f16655f148d75",
                  "internal-pdf-viewer,mhjfbmdgcfjbbpaeojofohoefgiehjai,internal-nacl-plugin", "0", "-1", "0", "8",
                  "Arial,Courier,CourierNew,Helvetica,Times,TimesNewRoman", "1542334693086",
                  "-1,-1,3,1,41,0,41,0,235,9,4,4,13,315,315,403,522,522,522,-1", "-1", "-1", "99", "2", "6", "58", "16",
                  "false", "false"]
    i_dict = dict(zip(key_list, value_list))
    for k, v in i_dict.items():
        i_dict[k] = v.split(",") if "," in v else v
    return i_dict


def get_performance_timing():
    d8_code = read_file_content(filename="custom.js")
    exec_obj = execjs.compile(d8_code)
    time_str = "navigationStart=1542347659930#unloadEventStart=1542347665305#unloadEventEnd=1542347665306#redirectStart=1542347659932#redirectEnd=1542347662682#fetchStart=1542347662682#domainLookupStart=1542347662682#domainLookupEnd=1542347662682#connectStart=1542347662682#connectEnd=1542347662682#secureConnectionStart=0#requestStart=1542347662684#responseStart=1542347665302#responseEnd=1542347665307#domLoading=1542347665311#domInteractive=1542347665666#domContentLoadedEventStart=1542347665667#domContentLoadedEventEnd=1542347665740#domComplete=1542347665753#loadEventStart=1542347665753#loadEventEnd=1542347665753"
    time_list = time_str.split("#")
    info = {}
    for t in time_list:
        k, v = t.split("=")
        info[k] = int(v)
    ret = exec_obj.call("getPerformanceTiming", info).replace("NaN", "-1")
    return ret


def format_js_code():
    # format_fullpage_code()
    # format_slide_code()
    format_click_code()
