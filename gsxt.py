# coding:utf-8

import re
import datetime
import execjs
import random
import operator
from geetest.tools.js_crack import JavascriptCrack
from geetest.tools.utils import download, get_timestamp, to_json, get_md5
from geetest.geetest_utils import generate_aes_key, rsa_encrypt, get_Q0o, hb_encrypt, m5_encrypt, hb_trace_encrypt, \
    read_file_content, j5_encrypt, hb_slide_trace_encrypt, hb_click_trace_encrypt
from PIL import Image
from io import BytesIO


class GsxtCrack(object):
    urls = {
        "index": "http://www.gsxt.gov.cn/index.html",
        "captcha": "http://www.gsxt.gov.cn/SearchItemCaptcha?t={0}",
        "custom_image": "http://www.gsxt.gov.cn/corp-query-custom-geetest-image.gif?v={0}",
        "validate_input": "http://www.gsxt.gov.cn/corp-query-geetest-validate-input.html?token={0}",
        "get_type": "http://api.geetest.com/gettype.php",
        "get_param": "http://api.geetest.com/get.php",
        "verify": "http://api.geetest.com/ajax.php",
        "refresh": "http://api.geetest.com/refresh.php",
        "resources_host": "http://resources.geetest.com",
    }

    def __init__(self, logger=None):
        self.logger = logger
        self.gt = ""
        self.challenge = ""
        self.token = ""
        self.offline = False
        self.new_captcha = False
        self.__aes_key = ""
        self._type_info = {}
        self._param_info = {}
        self._geetest_params = {}
        self.__ctx = execjs.compile(read_file_content(filename="custom.js"))
        self.__slide_ctx = execjs.compile(read_file_content(filename="custom_slide.js"))
        self.__click_ctx = execjs.compile(read_file_content(filename="custom_click.js"))
        self.verify_type = {
            "click": {"name": "click", "func": self.do_click_verify},
            "slide": {"name": "slide3", "func": self.do_slide_verify},
        }
        self._search_button_pos = (1065, 115)
        self._click_box = {
            "left": 800.15625,
            "top": 375.40625,
            "width": 304.640625,
            "height": 304.640625,
            "submit": (250, 335)
        }
        self._click_points = []

    def get_request_params_info(self, extra_info):
        info = {
            "gt": self.gt,
            "challenge": self.challenge,
            "lang": "zh-cn",
            "pt": "0",
            "callback": "geetest_{0}".format(get_timestamp())
        }
        info.update(extra_info or {})
        return info

    def get_token(self):
        now = datetime.datetime.now()
        ver = now.minute + now.second
        image_url = self.urls["custom_image"].format(ver)
        img_result = download(image_url)
        content = "".join([chr(i) for i in img_result])
        code = content.replace("\n}", ";\nreturn location_info;\n}")
        ctx = execjs.compile(code)

        location_info = ctx.eval("location_info")
        url = self.urls["validate_input"].format(location_info)
        token_result = download(url)
        content = "".join([chr(i) for i in token_result])
        value = re.search(r"value:\s*(\d+)", content).group(1)
        token = ctx.call("check_browser", {"value": int(value)})
        return token

    @staticmethod
    def get_cookies(js_code):
        instance = JavascriptCrack(js_code)
        cookies_str = instance.cookies
        k_v = cookies_str.split(";", 1)[0].split("=")
        return {k_v[0]: k_v[1]}

    def get_type_info(self):
        type_info = self.fetch(self.urls["get_type"])
        return type_info.get("data", {})

    def get_geetest_params(self):
        self.__aes_key = generate_aes_key()
        encrypt_key_msg = rsa_encrypt(ctx=self.__ctx, message=self.__aes_key)
        info = {
            "gt": self.gt, "challenge": self.challenge,
            "offline": self.offline, "product": "bind", "width": "300px", "protocol": "http://",
            "ww": True, "cc": 8,
            "i": self._get_i_param()
        }
        info.update(self._type_info)
        encrypt_msg = get_Q0o(ctx=self.__ctx, message=info, aes_key=self.__aes_key)
        w = encrypt_msg + encrypt_key_msg
        params_info = self.fetch(self.urls["get_param"], extra_params={"w": w})
        return params_info.get("data", {})

    def do_first_verify(self):
        start_time = get_timestamp()
        trace_list = self._generate_trace(vtype="first")
        P0o = hb_trace_encrypt(ctx=self.__ctx, trace_list=trace_list)
        S0o = hb_trace_encrypt(ctx=self.__ctx, trace_list=[])
        magic_msg = self._get_i_param(sep="magic data")
        info = {
            "lang": "zh-cn",
            "type": "fullpage",
            "tt": m5_encrypt(ctx=self.__ctx, message=P0o, arr=self._geetest_params.get("c"),
                             mstr=self._geetest_params.get("s")),
            "light": "INPUT_0",
            "s": get_md5(text=hb_encrypt(ctx=self.__ctx, message=S0o)),  # md5(D8[B5Y.c78(1283)](S0o))
            "h": get_md5(text=hb_encrypt(ctx=self.__ctx, message=magic_msg)),
            "hh": get_md5(text=magic_msg),  # md5(i)
            "hi": get_md5(text=self._get_i_param(sep="!!")),  # md5(i)
            "ep": self.get_ep_param(),
        }
        end_time = get_timestamp()
        passtime = end_time - start_time
        info.update({"passtime": passtime, "rp": get_md5("".join([self.gt, self.challenge, str(passtime)]))})
        encrypt_msg = get_Q0o(ctx=self.__ctx, message=info, aes_key=self.__aes_key)
        ret_info = self.fetch(self.urls["verify"], extra_params={"w": encrypt_msg})
        print(ret_info)
        return ret_info.get("data", {})

    def do_click_verify(self):
        start_time = get_timestamp()
        img_url = self.urls["resources_host"] + self._geetest_params["pic"]
        print(img_url)
        click_img = self.fetch(url=img_url, get_json=False, get_bytes=True)
        point_list = self._get_coordinate(vtype="click", image_info={"type": "click", "image": click_img})
        a = self.__get_a_param(point_list=point_list)
        trace_list = self._generate_trace(vtype="click")
        P0o = hb_click_trace_encrypt(ctx=self.__click_ctx, trace_list=trace_list)
        info = {
            "lang": "zh-cn",
            "tt": m5_encrypt(ctx=self.__ctx, message=P0o, arr=self._geetest_params.get("c"),
                             mstr=self._geetest_params.get("s")),
            "pic": self._geetest_params.get("pic"),
            "a": a,
            "ep": self.get_ep_param(vtype="click"),
        }
        end_time = get_timestamp()
        passtime = end_time - start_time
        info.update({"passtime": passtime, "rp": get_md5("".join([self.gt, self.challenge[:32], str(passtime)]))})
        aes_key = generate_aes_key()
        encrypt_key_msg = rsa_encrypt(ctx=self.__ctx, message=aes_key)
        encrypt_msg = get_Q0o(ctx=self.__ctx, message=info, aes_key=aes_key)
        ret_info = self.fetch(self.urls["verify"], extra_params={"w": encrypt_msg + encrypt_key_msg})
        return ret_info

    def do_slide_verify(self):
        start_time = get_timestamp()
        trace_list = self._generate_trace(vtype="slide")
        P0o = hb_slide_trace_encrypt(ctx=self.__slide_ctx, trace_list=trace_list)
        J72 = "64"  # last point x
        info = {
            "lang": "zh-cn",
            "aa": m5_encrypt(ctx=self.__ctx, message=P0o, arr=self._geetest_params.get("c"),
                             mstr=self._geetest_params.get("s")),
            "imgload": random.randint(90, 150),
            "userresponse": j5_encrypt(ctx=self.__slide_ctx, vint=int(J72), vstr=self.challenge),
            "ep": self.get_ep_param(vtype="slide"),
        }
        end_time = get_timestamp()
        passtime = end_time - start_time
        info.update({"passtime": passtime, "rp": get_md5("".join([self.gt, self.challenge[:32], str(passtime)]))})
        aes_key = generate_aes_key()
        encrypt_key_msg = rsa_encrypt(ctx=self.__ctx, message=aes_key)
        encrypt_msg = get_Q0o(ctx=self.__ctx, message=info, aes_key=aes_key)
        ret_info = self.fetch(self.urls["verify"], extra_params={"w": encrypt_msg + encrypt_key_msg})
        return ret_info

    def get_next_params(self, verify_type="click"):
        vtype = self.verify_type.get(verify_type, {}).get("name")
        params = {
            "is_next": True,
            "type": vtype,
            "https": False,
            "protocol": "http://",
            "offline": False,
            "product": "embed",
            "api_server": "api.geetest.com",
            "width": "100%",
        }
        params_info = self.fetch(self.urls["get_param"], extra_params=params)
        return params_info.get("data", {})

    def refresh_pic(self, verify_type="click"):
        pic_info = self.fetch(self.urls["refresh"], extra_params={"type": verify_type})
        return pic_info.get("data", {})

    def _get_coordinate(self, vtype, image_info):
        if vtype == "click":
            fp = BytesIO(image_info.get("image"))
            im = Image.open(fp=fp)
            im.show()
            points_str = input("Input point position>>>")
            return list(map(lambda p: tuple(p.split("_")), points_str.split(",")))
        elif vtype == "slide":
            return []
        else:
            return []

    def _generate_trace(self, vtype="first"):
        if vtype == "first":
            search_button_pos = tuple(map(lambda t: random.randint(t - 2, t + 2), self._search_button_pos))
            random_pos = (random.randint(100, 800), random.randint(100, 400))
            trace_list = self._generate_trace_between_two_point(random_pos, search_button_pos)
        elif vtype == "slide":
            trace_list = []
        elif vtype == "click":
            trace_list = []
        else:
            trace_list = []
        return trace_list

    def _generate_trace_between_two_point(self, point_a, point_b, radio=10):
        x1, y1 = point_a
        x2, y2 = point_b
        dx, dy = x2 - x1, y2 - y1
        abs_x, abs_y = operator.abs(dx), operator.abs(dy)
        slope = dy / dx
        get_ty = lambda tx: (tx - x1) * slope + y1
        ox, oy = tuple(map(lambda t: operator.add if t > 0 else operator.sub, (dx, dy)))
        base_step_x = abs_x // radio
        step_x_rng = base_step_x // 2

        get_val = lambda x, y: random.randint(int(x) - y, int(x) + y)

        sx = 0
        lx = x1
        trace_list = []
        while True:
            step_x = get_val(base_step_x, step_x_rng)
            tx = ox(lx, step_x)
            ty = get_ty(tx)
            ts = int(get_timestamp())
            x = get_val(tx, 5)
            y = get_val(ty, 5)
            trace_list.append([x, y, ts])

            sx += step_x
            lx = x

            if abs_x - sx <= base_step_x:
                break
        return trace_list

    def get_point_info(self, point, ptime, etype="move"):
        if etype not in ["focus", "blur"]:
            _event = "{0}{1}".format("pointer", etype)
            point_info = [etype, point[0], point[1], int(ptime), _event]
        else:
            point_info = [etype, int(ptime)]
        return point_info

    def __get_a_param(self, point_list):
        self._click_points = list(map(lambda p: (int(p[0]) + self._click_box["left"],
                                                 int(p[1]) + self._click_box["top"]), point_list))
        ratio_list = list(map(lambda p: "{x}_{y}".format(x=int(p[0] / self._click_box["width"] * 10000),
                                                         y=int(p[1] / self._click_box["height"] * 10000)), point_list))
        return "_".join(ratio_list)

    def get_ep_param(self, vtype="first"):
        base_info = {
            "f": get_md5("".join([self.gt, self.challenge])),
            "te": False,  # touchEvent
            "me": True,  # mouseEvent
            "tm": self._generate_tm()
        }
        if vtype == "first":
            # tm < fp < lp < ts
            ep_info = {
                "v": "8.6.1",
                "ip": "10.8.10.128",
                "de": False,  # deviceorientation
                "ven": "Intel Open Source Technology Center",
                "ren": "Mesa DRI Intel(R) Sandybridge Mobile ",
                "ac": "f930496cb2084fa8e08a507beb9e3871",  # md5(window.AudioContext)
                "pu": False,  # puppet
                "ph": False,  # phantom
                "ni": False,  # nightmare
                "se": False,  # selenium
                "fp": ["move", random.randint(750, 850), random.randint(300, 400), get_timestamp(), "pointermove"],
                "lp": ["up", random.randint(800, 1200), random.randint(250, 450),
                       get_timestamp() + random.randint(500, 1500), "pointerup"],
                "em": {
                    "ph": 0,
                    "cp": 0,
                    "ek": "11",
                    "wd": 0,
                    "nt": 0,
                    "si": 0,
                    "sc": 0
                },
                "by": -1,
                "ts": get_timestamp(),
            }
        elif vtype == "slide":
            ep_info = {"v": "7.4.3"}
        elif vtype == "click":
            ca = []  # TODO
            ep_info = {"v": "2.6.4", "ca": ca}
        else:
            ep_info = {}
        ep_info.update(base_info)
        return ep_info

    @staticmethod
    def _generate_tm():
        current_ts = get_timestamp()
        return {
            "a": current_ts,
            "b": current_ts + random.randint(90, 100),
            "c": current_ts + random.randint(90, 100),
            "d": 0,
            "e": 0,
            "f": current_ts + random.randint(1, 5),
            "g": current_ts + random.randint(1, 5),
            "h": current_ts + random.randint(1, 5),
            "i": current_ts + random.randint(1, 5),
            "j": current_ts + random.randint(1, 5),
            "k": 0,
            "l": current_ts + random.randint(1, 5),
            "m": current_ts + random.randint(90, 100),
            "n": current_ts + random.randint(95, 105),
            "o": current_ts + random.randint(95, 105),
            "p": current_ts + random.randint(420, 430),
            "q": current_ts + random.randint(420, 430),
            "r": current_ts + random.randint(455, 460),
            "s": current_ts + random.randint(535, 545),
            "t": current_ts + random.randint(535, 545),
            "u": current_ts + random.randint(535, 545)
        }

    def _get_i_param(self, sep="!!"):
        i_str = "3668!!17548!!CSS1Compat!!50!!-1!!-1!!-1!!-1!!3!!-1!!-1!!-1!!9!!9!!-1!!9!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!9!!-1!!4!!-1!!-1!!1600!!0!!1600!!0!!1920!!353!!1920!!1080!!zh-CN!!zh-CN,zh!!-1!!1!!24!!Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36!!1!!1!!1920!!1080!!1920!!1080!!1!!1!!1!!-1!!Linux x86_64!!0!!-8!!04f7eb201d3cc0991ab472b909027874!!2e2d74424f3cc8b7d88f16655f148d75!!internal-pdf-viewer,mhjfbmdgcfjbbpaeojofohoefgiehjai,internal-nacl-plugin!!0!!-1!!0!!8!!Arial,Courier,CourierNew,Helvetica,Times,TimesNewRoman!!1542365354985!!3,177,0,0,0,0,0,2,10715,6,3,3,8,307,307,438,613,613,613,-1!!-1!!-1!!61!!6!!-1!!-1!!14!!false!!false"
        i_list = i_str.split("!!")
        i_list[64] = str(get_timestamp())
        return sep.join(i_list)

    def fetch(self, url, extra_params=None, params=None, data=None, get_json=True, cookies=None, get_bytes=False):
        params = params or self.get_request_params_info(extra_info=extra_params)
        result = download(url, data=data, params=params, get_json=False, cookies=cookies, get_bytes=get_bytes)
        if get_json:
            return to_json(json_str=result)
        else:
            return result

    def start(self):
        source = self.fetch(self.urls["index"], get_json=False)
        cookies = self.get_cookies(js_code=source)
        captcha_url = self.urls["captcha"].format(get_timestamp())
        challenge_info = self.fetch(captcha_url, cookies=cookies)
        self.gt = challenge_info.get("gt")
        self.challenge = challenge_info.get("challenge")
        self.offline = not bool(challenge_info.get("success"))
        if self.offline:
            return get_md5(text=self.challenge)
        self.new_captcha = challenge_info.get("new_captcha", False)
        # self.token = self.get_token()
        self._type_info = self.get_type_info()
        self._geetest_params = self.get_geetest_params()
        verify_ret = self.do_first_verify()
        if "validate" in verify_ret.keys():
            return verify_ret.get("validate", "").split("|")[0]
        else:
            verify_type = verify_ret.get("result")
            self._geetest_params = self.get_next_params(verify_type=verify_type)
            verify_func = self.verify_type[verify_type]["func"]
            vret = verify_func()
            if vret.get("status") == "error":
                pass
            else:
                return vret.get("data", {}).get("validate", "").split("|")[0]


if __name__ == '__main__':
    t = GsxtCrack()
    # point_a = (0, 200)
    # point_b = (100,200)
    # print(t._generate_trace_between_two_point(point_a, point_b))
    t.start()
