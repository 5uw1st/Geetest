# coding:utf-8

import operator
import random
import time
from math import inf

from matplotlib import pyplot as plt

from geetest.tools.utils import get_timestamp


def get_range(base, rng=3):
    return random.randint(base - rng, base + rng)


def get_x_y_relate(point_a, point_b, rp_x=0.24, rp_y=0.36):
    """
    获取x/y函数关系(二次函数)-->利用三点式
    :param point_a: 起始点
    :param point_b: 结束点
    :param rp_x: 偏离起始点x轴比例
    :param rp_y: 偏离起始点y轴比例
    :return:
    """
    x1, y1 = point_a
    x2, y2 = point_b
    x3, y3 = get_third_point(point_a, point_b, rp_x=rp_x, rp_y=rp_y)
    b = ((x2 ** 2 - x3 ** 2) * (y1 - y2) - (x1 ** 2 - x2 ** 2) * (y2 - y3)) / (
            (x2 ** 2 - x3 ** 2) * (x1 - x2) - (x1 ** 2 - x2 ** 2) * (x2 - x3))
    a = (y1 - y2 - b * (x1 - x2)) / (x1 ** 2 - x2 ** 2)
    c = y1 - x1 ** 2 * a - b * x1
    get_y = lambda x: x ** 2 * a + b * x + c
    return get_y


def get_x_y_line_relate(point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b
    dx = x1 - x2
    dx = dx if dx != 0 else 1
    get_y = lambda x: (x - x2) / dx * (y1 - y2) + y2
    return get_y


def generate_beenline_trace_between_two_point(point_a, point_b, radio=0.1):
    x1, y1 = point_a
    x2, y2 = point_b
    dx, dy = x2 - x1, y2 - y1
    abs_x, abs_y = operator.abs(dx), operator.abs(dy)
    slope = dy / dx
    get_ty = lambda tx: (tx - x1) * slope + y1
    ox, oy = tuple(map(lambda t: operator.add if t > 0 else operator.sub, (dx, dy)))
    base_step_x = abs_x // radio or 5
    step_x_rng = base_step_x // 2 or 2

    get_val = lambda x, y: random.randint(int(x) - y, int(x) + y)

    sx = 0
    lx = x1
    trace_list = list()
    # first point
    trace_list.append([x1, y1, int(get_timestamp())])
    while True:
        time.sleep(random.randint(15, 40) / 1000)
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
    # last point
    trace_list.append([x2, y2, int(get_timestamp())])
    return trace_list


def generate_mouse_trace_between_two_point(point_a, point_b, rp=(), dense_radio=None, time_rng=None,
                                           start_time=None, show=False):
    """
    生成两点之间的鼠标移动轨迹
    :param point_a: (x1, y1) 起始点
    :param point_b: (x2, y2) 结束点
    :param rp: ((rp_x, rp_y)...) 调节参数集
    :param dense_radio: 点密集程度
    :param time_rng: 每个点耗时范围
    :param start_time: 开始时间
    :param show: 是否画出s/t, y/x 之间的关系图
    :return: [(x, y, ts)...]
    """
    dense_radio = dense_radio or 0.15
    time_rng = time_rng or (12, 28)
    if len(rp) == 0:
        rp_x_y_relate = (0.2, 0.4)
        rp_s_t_relate = []
    else:
        rp_x_y_relate, *rp_s_t_relate = rp
    rp_x, rp_y = rp_x_y_relate
    if operator.abs(point_a[0] - point_b[0]) <= 2 or operator.abs(point_a[1] - point_b[1]) <= 2:
        get_y = get_x_y_line_relate(point_a, point_b)
    else:
        get_y = get_x_y_relate(point_a, point_b, rp_x=rp_x, rp_y=rp_y)

    distance = calc_distance(point_a, point_b)
    point_num = get_range(round(distance * dense_radio), rng=2)
    ts = [random.randint(time_rng[0], time_rng[1]) for _ in range(point_num)]
    get_s = get_distance_time_relate(point_a, point_b, ts=ts, rp=rp_s_t_relate)

    if show:
        ii = 0
        for i in ts:
            ii += i
            plt.scatter(ii, get_s(ii), color="y")
        plt.show()

    xs = []
    ys = []
    rts = []
    start_time = start_time or int(get_timestamp())
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    x0, y0 = point_a
    lt = 0
    ls = 0
    opt = operator.add if point_b[0] - point_a[0] >= 0 else operator.sub
    for t in ts:
        lt += t
        s = get_s(lt) - ls
        x_y = lambda x, y: (x - x0) ** 2 + (y - y0) ** 2
        tv = s ** 2
        dx = point_b[0] - x0
        mx = min(operator.abs(dx), s)
        rng_x = (x0, opt(x0, mx)) if opt == operator.add else (opt(x0, mx), x0)
        nx, ny = calc_x_y(get_y=get_y, x_y=x_y, tv=tv, rng_x=rng_x, opt=opt)
        xs.append(round(nx))
        ys.append(round(ny))
        x0, y0 = (nx, ny)
        ls += s

        current_time = start_time + t
        rts.append(current_time)
        plt.scatter(nx, ny, color="b")
        start_time = current_time

    if show:
        plt.show()

    trace_list = list(zip(xs, ys, rts))
    return trace_list


def calc_x_y(get_y, x_y, tv, rng_x, opt, step=0.005):
    error, rx, ry = inf, 0, 0
    min_x, max_x = rng_x
    current_x = min_x if opt == operator.add else max_x
    while True:
        x = opt(current_x, step)
        y = get_y(x)

        ret = x_y(x=x, y=y)
        ce = operator.abs(ret - tv)

        if ce < error:
            rx = x
            ry = y
            error = ce

        if x >= max_x or x <= min_x:
            break

        current_x = x

    return rx, ry


def get_value(vals, get_max=True):
    rx = 0 if get_max else inf
    opt = operator.gt if get_max else operator.lt
    for val in vals:
        v = val.evalf()
        if v.is_real and v > 0 and opt(v, rx):
            rx = v
    return rx


def get_distance_time_relate(point_a, point_b, ts, rp_t=0.5, rp_s=0.5, bend_radio=1.5, rp=()):
    """
    获取距离时间关系函数
    :param point_a: 距离时间起始点
    :param point_b: 距离时间目标点
    :param ts: 移动时间列表
    :param rp_t: 时间转折点
    :param rp_s: 距离转折点
    :param bend_radio: 弯曲程度
    :param rp: 调节参数
    :return:
    """
    if len(rp) >= 2:
        rp_before, rp_after, *_ = rp
    elif len(rp) == 1:
        rp_before = rp
        rp_after = (0.2, 0.4)
    else:
        rp_before, rp_after = ((0.6, 0.3), (0.2, 0.4))
    distance = calc_distance(point_a, point_b)
    total_ts = sum(ts)
    total_dis = distance * bend_radio
    x3, y3 = total_ts * rp_t, total_dis * rp_s
    point_c = (x3, y3)
    before_relate = get_x_y_relate(point_a=(0, 0), point_b=point_c, rp_x=rp_before[0], rp_y=rp_before[1])
    after_relate = get_x_y_relate(point_a=point_c, point_b=(total_ts, total_dis), rp_x=rp_after[0], rp_y=rp_after[1])
    get_s = lambda t: before_relate(t) if t <= x3 else after_relate(t)
    return get_s


def get_third_point(point_a, point_b, rp_x=0.4, rp_y=0.5):
    x1, y1 = point_a
    x2, y2 = point_b
    dx, dy = x2 - x1, y2 - y1
    abs_dx, abs_dy = operator.abs(dx), operator.abs(dy)
    sep_x, sep_y = abs_dx * rp_x, abs_dy * rp_y
    opt = lambda x: operator.add if x > 0 else operator.sub
    opt_x, opt_y = opt(x=dx), opt(x=dy)
    x3, y3 = opt_x(x1, sep_x), opt_y(y1, sep_y)
    return x3, y3


def draw_trace(trace_list):
    pa = trace_list[0]
    pb = trace_list[-1]
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position('top')
    ax.plot((pa[1], pb[1]), (pa[2], pb[2]), color="r")
    for p in trace_list:
        if len(p) == 5:
            if p[0] in ["down", "up"]:
                ax.scatter(p[1], p[2], color="y")
            else:
                ax.scatter(p[1], p[2], color="b")
    plt.show()


def start_generate_trace(show=True):
    a = (0, 0)
    b = (200, 200)
    t = generate_mouse_trace_between_two_point(a, b, show=show)
    print(t)


def calc_distance(point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b
    dis = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return dis


def draw_distance_time_relate():
    # tl = '[["scroll",782,423,1543145000359,null],["move",779,166,1543145001766,"pointermove"],["move",773,162,1543145001784,"pointermove"],["move",767,159,1543145001801,"pointermove"],["move",763,157,1543145001817,"pointermove"],["move",760,154,1543145001834,"pointermove"],["move",756,151,1543145001851,"pointermove"],["move",751,148,1543145001868,"pointermove"],["move",747,146,1543145001884,"pointermove"],["move",744,145,1543145001901,"pointermove"],["move",741,143,1543145001920,"pointermove"],["move",738,142,1543145001935,"pointermove"],["move",735,141,1543145001951,"pointermove"],["move",732,140,1543145001969,"pointermove"],["move",730,138,1543145001985,"pointermove"],["move",729,138,1543145002002,"pointermove"],["move",728,138,1543145002018,"pointermove"],["move",729,138,1543145002070,"pointermove"],["move",738,136,1543145002086,"pointermove"],["move",749,134,1543145002103,"pointermove"],["move",762,130,1543145002120,"pointermove"],["move",771,127,1543145002136,"pointermove"],["move",779,123,1543145002153,"pointermove"],["move",783,121,1543145002169,"pointermove"],["move",785,120,1543145002185,"pointermove"],["move",786,118,1543145002202,"pointermove"],["move",787,120,1543145002287,"pointermove"],["move",789,126,1543145002303,"pointermove"],["move",790,136,1543145002320,"pointermove"],["move",793,147,1543145002336,"pointermove"],["move",794,160,1543145002354,"pointermove"],["move",795,166,1543145002367,"pointermove"],["move",785,304,1543145003429,"pointermove"],["move",784,301,1543145003442,"pointermove"],["move",783,296,1543145003459,"pointermove"],["move",780,289,1543145003475,"pointermove"],["move",776,281,1543145003492,"pointermove"],["move",765,267,1543145003510,"pointermove"],["move",753,259,1543145003526,"pointermove"],["move",741,251,1543145003543,"pointermove"],["move",728,245,1543145003560,"pointermove"],["move",715,240,1543145003577,"pointermove"],["move",703,236,1543145003594,"pointermove"],["move",695,233,1543145003614,"pointermove"],["move",694,232,1543145003627,"pointermove"],["move",692,231,1543145003645,"pointermove"],["move",690,229,1543145003661,"pointermove"],["move",689,227,1543145003679,"pointermove"],["move",688,223,1543145003695,"pointermove"],["move",689,220,1543145003711,"pointermove"],["move",690,219,1543145003727,"pointermove"],["move",692,217,1543145003744,"pointermove"],["move",694,215,1543145003761,"pointermove"],["move",696,212,1543145003777,"pointermove"],["move",698,210,1543145003794,"pointermove"],["move",698,208,1543145003811,"pointermove"],["move",699,206,1543145003827,"pointermove"],["move",699,205,1543145003845,"pointermove"],["move",699,204,1543145003861,"pointermove"],["move",699,202,1543145003877,"pointermove"],["move",699,201,1543145003895,"pointermove"],["move",699,200,1543145003912,"pointermove"],["focus",1543145004015],["focus",1543145004015],["down",699,200,1543145004022,"pointerdown"],["up",699,200,1543145004110,"pointerup"],["move",696,201,1543145004165,"pointermove"],["move",688,204,1543145004181,"pointermove"],["move",674,209,1543145004197,"pointermove"],["move",649,216,1543145004214,"pointermove"],["move",640,218,1543145004230,"pointermove"],["move",616,223,1543145004247,"pointermove"],["move",606,224,1543145004264,"pointermove"],["move",601,225,1543145004280,"pointermove"],["move",599,225,1543145004297,"pointermove"],["move",598,225,1543145004315,"pointermove"],["move",597,226,1543145004330,"pointermove"],["down",597,226,1543145004502,"pointerdown"],["up",597,226,1543145004606,"pointerup"],["move",596,225,1543145004635,"pointermove"],["move",596,224,1543145004649,"pointermove"],["move",596,222,1543145004666,"pointermove"],["move",597,217,1543145004683,"pointermove"],["move",609,200,1543145004716,"pointermove"],["move",614,188,1543145004733,"pointermove"],["move",618,170,1543145004749,"pointermove"],["move",618,163,1543145004767,"pointermove"],["move",618,156,1543145004783,"pointermove"],["move",618,151,1543145004799,"pointermove"],["move",618,146,1543145004816,"pointermove"],["move",618,140,1543145004833,"pointermove"],["move",617,135,1543145004850,"pointermove"],["move",615,131,1543145004866,"pointermove"],["move",614,127,1543145004883,"pointermove"],["move",613,123,1543145004900,"pointermove"],["move",612,116,1543145004917,"pointermove"],["move",610,111,1543145004933,"pointermove"],["move",608,108,1543145004949,"pointermove"],["move",607,104,1543145004967,"pointermove"],["move",606,100,1543145004983,"pointermove"],["move",605,98,1543145005000,"pointermove"],["move",605,96,1543145005017,"pointermove"],["move",605,94,1543145005034,"pointermove"],["move",605,93,1543145005050,"pointermove"],["move",605,92,1543145005067,"pointermove"],["move",605,91,1543145005086,"pointermove"],["down",605,91,1543145005102,"pointerdown"],["up",605,91,1543145005221,"pointerup"],["move",607,91,1543145005269,"pointermove"],["move",612,94,1543145005286,"pointermove"],["move",624,98,1543145005302,"pointermove"],["move",634,99,1543145005319,"pointermove"],["move",650,99,1543145005336,"pointermove"],["move",673,99,1543145005355,"pointermove"],["move",698,99,1543145005370,"pointermove"],["move",718,99,1543145005386,"pointermove"],["move",726,99,1543145005402,"pointermove"],["move",728,98,1543145005420,"pointermove"],["move",729,98,1543145005437,"pointermove"],["move",730,97,1543145005519,"pointermove"],["down",730,97,1543145005591,"pointerdown"],["up",730,97,1543145005709,"pointerup"],["move",730,100,1543145005804,"pointermove"],["move",729,102,1543145005823,"pointermove"],["move",728,104,1543145005838,"pointermove"],["move",727,106,1543145005856,"pointermove"],["move",727,107,1543145005889,"pointermove"],["move",727,109,1543145005905,"pointermove"],["move",727,111,1543145005923,"pointermove"],["move",727,112,1543145005938,"pointermove"],["move",726,114,1543145005955,"pointermove"],["move",726,116,1543145005989,"pointermove"],["move",727,119,1543145006005,"pointermove"],["move",729,124,1543145006022,"pointermove"],["move",731,130,1543145006039,"pointermove"],["move",733,135,1543145006054,"pointermove"],["move",734,139,1543145006072,"pointermove"],["move",736,143,1543145006089,"pointermove"],["move",738,148,1543145006105,"pointermove"],["move",742,155,1543145006123,"pointermove"],["move",750,168,1543145006139,"pointermove"],["move",759,183,1543145006156,"pointermove"],["move",767,197,1543145006172,"pointermove"],["move",778,215,1543145006189,"pointermove"],["move",781,223,1543145006205,"pointermove"],["move",784,230,1543145006224,"pointermove"],["move",788,241,1543145006239,"pointermove"],["move",793,254,1543145006257,"pointermove"],["move",799,268,1543145006273,"pointermove"],["move",803,280,1543145006290,"pointermove"],["move",804,289,1543145006307,"pointermove"],["move",805,293,1543145006323,"pointermove"],["move",805,297,1543145006340,"pointermove"],["move",806,304,1543145006357,"pointermove"],["blur",1543145007797],["scroll",806,300,1543145009029,null],["scroll",806,294,1543145009077,null],["scroll",806,276,1543145009137,null],["scroll",806,277,1543145009182,null],["scroll",806,280,1543145009222,null],["scroll",806,279,1543145009314,null],["scroll",806,282,1543145009360,null],["move",802,330,1543145009378,"pointermove"],["move",800,281,1543145009435,"pointermove"],["scroll",800,281,1543145009437,null],["move",798,272,1543145009446,"pointermove"],["move",798,267,1543145009457,"pointermove"],["move",795,258,1543145009473,"pointermove"],["move",791,251,1543145009499,"pointermove"],["move",791,250,1543145009508,"pointermove"],["move",791,249,1543145009523,"pointermove"],["move",790,249,1543145009582,"pointermove"],["move",789,249,1543145009622,"pointermove"],["move",789,250,1543145009694,"pointermove"],["move",789,251,1543145009707,"pointermove"],["move",789,254,1543145009723,"pointermove"],["move",789,256,1543145009741,"pointermove"],["move",789,259,1543145009757,"pointermove"],["move",788,263,1543145009773,"pointermove"],["move",788,265,1543145009790,"pointermove"],["move",787,267,1543145009807,"pointermove"],["move",787,268,1543145009824,"pointermove"],["move",787,269,1543145009841,"pointermove"],["move",787,271,1543145009857,"pointermove"],["move",787,274,1543145009874,"pointermove"],["move",786,278,1543145009891,"pointermove"],["move",785,282,1543145009908,"pointermove"],["move",785,285,1543145009924,"pointermove"],["move",785,289,1543145009941,"pointermove"],["move",785,296,1543145009958,"pointermove"],["move",785,299,1543145009975,"pointermove"],["move",785,302,1543145009991,"pointermove"],["move",785,304,1543145010008,"pointermove"],["move",784,308,1543145010025,"pointermove"],["move",784,310,1543145010042,"pointermove"],["move",784,314,1543145010058,"pointermove"],["move",784,317,1543145010075,"pointermove"],["move",784,320,1543145010090,"pointermove"],["move",783,321,1543145010109,"pointermove"],["move",783,322,1543145010542,"pointermove"],["move",782,323,1543145010622,"pointermove"],["move",782,324,1543145010630,"pointermove"],["focus",1543145010902],["down",782,324,1543145010903,"pointerdown"],["focus",1543145010905],["up",782,324,1543145011022,"pointerup"]]'
    tl = '[["move",1070,446,1542961354004,"pointermove"],["move",1070,432,1542961354012,"pointermove"],["move",1070,404,1542961354029,"pointermove"],["move",1065,383,1542961354046,"pointermove"],["move",1063,368,1542961354061,"pointermove"],["move",1057,350,1542961354079,"pointermove"],["move",1055,329,1542961354095,"pointermove"],["move",1055,309,1542961354112,"pointermove"],["move",1055,285,1542961354128,"pointermove"],["move",1055,275,1542961354145,"pointermove"],["move",1055,264,1542961354161,"pointermove"],["move",1055,254,1542961354178,"pointermove"],["move",1058,240,1542961354194,"pointermove"],["move",1064,224,1542961354212,"pointermove"],["move",1068,211,1542961354229,"pointermove"],["move",1068,203,1542961354246,"pointermove"],["move",1068,195,1542961354263,"pointermove"],["move",1068,190,1542961354278,"pointermove"],["move",1068,186,1542961354295,"pointermove"],["move",1068,184,1542961354312,"pointermove"],["move",1068,181,1542961354328,"pointermove"],["move",1068,176,1542961354345,"pointermove"],["move",1068,170,1542961354362,"pointermove"],["move",1070,164,1542961354378,"pointermove"],["move",1070,159,1542961354395,"pointermove"],["move",1070,156,1542961354412,"pointermove"],["move",1069,154,1542961354433,"pointermove"],["move",1069,152,1542961354449,"pointermove"],["move",1069,151,1542961354462,"pointermove"],["move",1069,145,1542961354478,"pointermove"],["move",1069,140,1542961354495,"pointermove"],["move",1069,135,1542961354512,"pointermove"],["move",1069,134,1542961354528,"pointermove"],["move",1068,131,1542961354545,"pointermove"],["move",1068,129,1542961354569,"pointermove"],["move",1068,126,1542961354585,"pointermove"],["move",1068,124,1542961354595,"pointermove"],["move",1068,120,1542961354612,"pointermove"],["move",1068,117,1542961354629,"pointermove"],["move",1067,115,1542961354645,"pointermove"],["focus",1542961354721],["down",1067,115,1542961354724,"pointerdown"],["focus",1542961354726],["up",1067,115,1542961354825,"pointerup"]]'
    # tl = tl.replace("null", "0")
    # tt = json.loads(tl)
    tt = [['move', 475, 497, 1543380257654, 'pointermove'], ['move', 476, 497, 1543380257668, 'pointermove'],
          ['move', 477, 498, 1543380257696, 'pointermove'], ['move', 479, 499, 1543380257711, 'pointermove'],
          ['move', 481, 499, 1543380257726, 'pointermove'], ['move', 483, 500, 1543380257741, 'pointermove'],
          ['move', 487, 502, 1543380257764, 'pointermove'], ['move', 490, 503, 1543380257779, 'pointermove'],
          ['move', 495, 505, 1543380257801, 'pointermove'], ['move', 499, 506, 1543380257814, 'pointermove'],
          ['move', 502, 508, 1543380257827, 'pointermove'], ['move', 507, 510, 1543380257843, 'pointermove'],
          ['move', 512, 511, 1543380257858, 'pointermove'], ['move', 521, 515, 1543380257882, 'pointermove'],
          ['move', 530, 518, 1543380257904, 'pointermove'], ['move', 540, 522, 1543380257927, 'pointermove'],
          ['move', 549, 525, 1543380257947, 'pointermove'], ['move', 563, 530, 1543380257974, 'pointermove'],
          ['move', 577, 534, 1543380257998, 'pointermove'], ['move', 584, 537, 1543380258011, 'pointermove'],
          ['move', 602, 543, 1543380258039, 'pointermove'], ['move', 618, 548, 1543380258063, 'pointermove'],
          ['move', 627, 550, 1543380258076, 'pointermove'], ['move', 639, 554, 1543380258093, 'pointermove'],
          ['move', 649, 557, 1543380258106, 'pointermove'], ['move', 662, 561, 1543380258124, 'pointermove'],
          ['move', 683, 567, 1543380258149, 'pointermove'], ['move', 703, 572, 1543380258173, 'pointermove'],
          ['move', 718, 576, 1543380258190, 'pointermove'], ['move', 731, 579, 1543380258204, 'pointermove'],
          ['move', 756, 585, 1543380258230, 'pointermove'], ['move', 781, 591, 1543380258255, 'pointermove'],
          ['move', 799, 595, 1543380258274, 'pointermove'], ['move', 810, 597, 1543380258286, 'pointermove'],
          ['move', 833, 602, 1543380258312, 'pointermove'], ['move', 849, 604, 1543380258330, 'pointermove'],
          ['move', 859, 606, 1543380258342, 'pointermove'], ['move', 877, 609, 1543380258364, 'pointermove'],
          ['move', 887, 611, 1543380258377, 'pointermove'], ['move', 897, 612, 1543380258389, 'pointermove'],
          ['move', 912, 615, 1543380258409, 'pointermove'], ['move', 921, 616, 1543380258422, 'pointermove'],
          ['move', 940, 618, 1543380258449, 'pointermove'], ['move', 954, 620, 1543380258469, 'pointermove'],
          ['move', 971, 622, 1543380258496, 'pointermove'], ['move', 987, 623, 1543380258522, 'pointermove'],
          ['move', 1000, 625, 1543380258545, 'pointermove'], ['move', 1007, 625, 1543380258558, 'pointermove'],
          ['move', 1014, 626, 1543380258572, 'pointermove'], ['move', 1022, 626, 1543380258588, 'pointermove'],
          ['move', 1034, 627, 1543380258614, 'pointermove'], ['move', 1045, 628, 1543380258640, 'pointermove'],
          ['move', 1050, 628, 1543380258653, 'pointermove'], ['move', 1059, 629, 1543380258678, 'pointermove'],
          ['move', 1065, 629, 1543380258694, 'pointermove'], ['move', 1070, 629, 1543380258709, 'pointermove'],
          ['move', 1077, 630, 1543380258736, 'pointermove'], ['move', 1082, 630, 1543380258756, 'pointermove'],
          ['move', 1087, 630, 1543380258775, 'pointermove'], ['move', 1090, 630, 1543380258789, 'pointermove'],
          ['move', 1092, 630, 1543380258802, 'pointermove'], ['move', 1095, 631, 1543380258821, 'pointermove'],
          ['move', 1097, 631, 1543380258837, 'pointermove'], ['move', 1098, 631, 1543380258849, 'pointermove'],
          ['move', 1100, 631, 1543380258874, 'pointermove'], ['focus', 1543380264677],
          ['down', 1100, 631, 1543380264677, 'pointerdown'], ['focus', 1543380264677],
          ['up', 1100, 631, 1543380264677, 'pointerup'], ['move', 889, 611, 1543380286023, 'pointermove'],
          ['move', 891, 610, 1543380286041, 'pointermove'], ['move', 896, 610, 1543380286059, 'pointermove'],
          ['move', 901, 609, 1543380286075, 'pointermove'], ['move', 915, 607, 1543380286103, 'pointermove'],
          ['move', 928, 605, 1543380286124, 'pointermove'], ['move', 938, 604, 1543380286137, 'pointermove'],
          ['move', 960, 601, 1543380286163, 'pointermove'], ['move', 977, 599, 1543380286181, 'pointermove'],
          ['move', 992, 598, 1543380286194, 'pointermove'], ['move', 1013, 596, 1543380286215, 'pointermove'],
          ['move', 1026, 595, 1543380286229, 'pointermove'], ['move', 1042, 594, 1543380286248, 'pointermove'],
          ['move', 1062, 593, 1543380286276, 'pointermove'], ['move', 1072, 593, 1543380286292, 'pointermove'],
          ['move', 1085, 593, 1543380286320, 'pointermove'], ['move', 1093, 592, 1543380286341, 'pointermove'],
          ['move', 1099, 592, 1543380286366, 'pointermove'], ['move', 1101, 592, 1543380286386, 'pointermove'],
          ['focus', 1543380286435], ['down', 1101, 592, 1543380286435, 'pointerdown'], ['focus', 1543380286435],
          ['up', 1101, 592, 1543380286435, 'pointerup'], ['move', 1031, 596, 1543380313410, 'pointermove'],
          ['move', 1033, 598, 1543380313437, 'pointermove'], ['move', 1035, 600, 1543380313454, 'pointermove'],
          ['move', 1041, 606, 1543380313482, 'pointermove'], ['move', 1048, 613, 1543380313509, 'pointermove'],
          ['move', 1053, 620, 1543380313528, 'pointermove'], ['move', 1063, 630, 1543380313555, 'pointermove'],
          ['move', 1071, 640, 1543380313576, 'pointermove'], ['move', 1078, 649, 1543380313592, 'pointermove'],
          ['move', 1088, 661, 1543380313613, 'pointermove'], ['move', 1101, 677, 1543380313639, 'pointermove'],
          ['move', 1112, 692, 1543380313659, 'pointermove'], ['move', 1124, 708, 1543380313681, 'pointermove'],
          ['move', 1133, 721, 1543380313699, 'pointermove'], ['move', 1140, 732, 1543380313715, 'pointermove'],
          ['move', 1146, 739, 1543380313727, 'pointermove'], ['move', 1151, 747, 1543380313739, 'pointermove'],
          ['move', 1160, 761, 1543380313764, 'pointermove'], ['move', 1169, 774, 1543380313791, 'pointermove'],
          ['move', 1176, 786, 1543380313817, 'pointermove'], ['move', 1179, 791, 1543380313831, 'pointermove'],
          ['move', 1185, 801, 1543380313858, 'pointermove'], ['move', 1189, 808, 1543380313884, 'pointermove'],
          ['move', 1193, 813, 1543380313911, 'pointermove'], ['move', 1194, 816, 1543380313931, 'pointermove'],
          ['move', 1196, 818, 1543380313958, 'pointermove'], ['focus', 1543380313842],
          ['down', 1196, 818, 1543380313842, 'pointerdown'], ['focus', 1543380313842],
          ['up', 1196, 818, 1543380313842, 'pointerup'], ['move', 878, 489, 1543380355260, 'pointermove'],
          ['move', 879, 490, 1543380355276, 'pointermove'], ['move', 880, 491, 1543380355288, 'pointermove'],
          ['move', 881, 494, 1543380355305, 'pointermove'], ['move', 884, 498, 1543380355327, 'pointermove'],
          ['move', 886, 502, 1543380355344, 'pointermove'], ['move', 889, 508, 1543380355363, 'pointermove'],
          ['move', 893, 515, 1543380355384, 'pointermove'], ['move', 897, 523, 1543380355403, 'pointermove'],
          ['move', 901, 529, 1543380355417, 'pointermove'], ['move', 908, 541, 1543380355442, 'pointermove'],
          ['move', 912, 548, 1543380355456, 'pointermove'], ['move', 921, 562, 1543380355481, 'pointermove'],
          ['move', 926, 569, 1543380355493, 'pointermove'], ['move', 934, 582, 1543380355513, 'pointermove'],
          ['move', 942, 594, 1543380355530, 'pointermove'], ['move', 956, 612, 1543380355556, 'pointermove'],
          ['move', 964, 623, 1543380355571, 'pointermove'], ['move', 973, 634, 1543380355585, 'pointermove'],
          ['move', 984, 648, 1543380355603, 'pointermove'], ['move', 996, 661, 1543380355619, 'pointermove'],
          ['move', 1007, 673, 1543380355635, 'pointermove'], ['move', 1018, 684, 1543380355651, 'pointermove'],
          ['move', 1036, 699, 1543380355677, 'pointermove'], ['move', 1048, 709, 1543380355695, 'pointermove'],
          ['move', 1057, 715, 1543380355708, 'pointermove'], ['move', 1074, 725, 1543380355733, 'pointermove'],
          ['move', 1091, 734, 1543380355760, 'pointermove'], ['move', 1098, 737, 1543380355772, 'pointermove'],
          ['move', 1110, 742, 1543380355792, 'pointermove'], ['move', 1124, 746, 1543380355819, 'pointermove'],
          ['move', 1137, 748, 1543380355845, 'pointermove'], ['move', 1144, 749, 1543380355860, 'pointermove'],
          ['move', 1154, 750, 1543380355886, 'pointermove'], ['move', 1158, 750, 1543380355898, 'pointermove'],
          ['move', 1163, 750, 1543380355912, 'pointermove'], ['move', 1166, 750, 1543380355924, 'pointermove'],
          ['move', 1172, 749, 1543380355949, 'pointermove'], ['move', 1175, 749, 1543380355969, 'pointermove'],
          ['move', 1178, 749, 1543380355991, 'pointermove'], ['move', 1179, 749, 1543380356004, 'pointermove'],
          ['focus', 1543380355832], ['down', 1179, 749, 1543380355832, 'pointerdown'], ['focus', 1543380355832],
          ['up', 1179, 749, 1543380355832, 'pointerup']]
    index = [0]
    tt = [p for p in tt if p[0] in ["move", "down", "up"]]
    for i, p in enumerate(tt):
        if p[0] == "down":
            index.append(i)
    index.append(-1)
    ts = [tt[index[i]:index[i + 1]] for i in range(len(index) - 1)][3]
    ts.pop(0)
    st = ts[0][3]
    s = 0
    pp = (ts[0][1], ts[0][2])
    pt = ts[0][3]
    mts = []
    ss = []
    for p in ts:
        mt = p[3] - st
        gt = p[3] - pt
        s += calc_distance(point_a=pp, point_b=(p[1], p[2]))
        plt.scatter(mt, s, color="b")
        plt.scatter(gt, 100, color="y")
        pp = (p[1], p[2])
        pt = p[3]
        mts.append(mt)
        ss.append(s)
    print(mts, ss, sep="\n")
    plt.show()


if __name__ == '__main__':
    start_generate_trace()
