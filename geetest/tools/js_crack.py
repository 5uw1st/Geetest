# -*- coding: utf8 -*-

import os
import re
import time

import execjs


class JavascriptCrack(object):
    replace_map = {
        r'(\};if.*\})': '};',
        r'(setTimeout.*?\));': '',
        r'(createElement.*.href)': """'http://www.gsxt.gov.cn/'""",
        r'document.': '',
        # r'\((window.*?)\)': '(undefined)',  # maybe need modify
        r'window\[.*?\]': 'undefined',
        r'window\.[_\w]+': 'undefined'
    }

    def __init__(self, source, timeout=3):
        self.source = source
        tmp = re.findall(r'x=\"(.*)\".replace', self.source)[0]
        self.func_name = None
        self.x = re.sub(r'@*$', "", tmp).split("@")
        self.y = re.findall(r'y=\"(.*)\",', self.source)[0]
        self.z = 0
        self.cookies = ""
        self.ctx = None
        self.code = None
        self.timeout = timeout
        self.generate_javascript()

    def generate_javascript(self):

        def calculate(x, y=99):
            a, b, c = 0, 0, 0
            x = list(x)
            while x and (ord(str(x[0])) - 77.5):
                a = x.pop(0)
                b = ord(str(a)) - 77.5
                if abs(b) < 13:
                    c = b + 48.5 + y * c
                else:
                    c = int(str(a), 36) + y * c
            return c

        matched = re.findall(r'\w', self.y)

        z = calculate(sorted(matched, key=lambda x: calculate(x)).pop())

        def replace(y):
            index = int(calculate(y.group(0), self.z) - 1)
            if index >= len(self.x):
                result = '_' + y.group(0)
            else:
                result = self.x[index] or '_' + y.group(0)
            return result

        self.z = int(z)
        st = time.time()
        while self.z:
            try:
                self.z += 1
                self.code = re.sub(r'\b\w+\b', replace, self.y)
                self.format_code()
                self.ctx = execjs.compile(self.code)
            except Exception as e:
                pass
            else:
                try:
                    self.cookies = self.ctx.call(self.func_name)
                except:
                    pass
                else:
                    break
            finally:
                et = time.time()
                if et - st > self.timeout:
                    raise TimeoutError

    def format_code(self):
        for k, v in self.replace_map.items():
            self.code = re.sub(k, v, self.code)
        self.code = str(self.code).replace("\\\\", '\\')
        self.code = self.code.replace(r"'\d+'", r"'\\d+'")
        self.code = self.code[:-2] + ';return cookie' + self.code[-2:]
        self.func_name = re.findall(r'var (.*?)=', self.code)[0]


if __name__ == '__main__':
    # source = """var x="rOm9XFMtA3QKV7nYsPGT4lifyWwkq5vcjH2IdxUoCbhERLaz81DNB6@qW@@@Array@a@@toLowerCase@while@try@split@25@@if@innerHTML@@@Tue@1537865484@d@@@3@@pathname@attachEvent@onreadystatechange@challenge@else@GMT@var@Path@@@Sep@2BTm@@match@@@@new@@captcha@2B@0xFF@join@JgSe0upZ@09@1500@@length@substr@search@parseInt@5@1@@function@2Q@@reverse@@24@https@fromCharCode@toString@cookie@e@8@@@@@@for@uz@addEventListener@firstChild@createElement@@156@return@2@div@51@D@@chars@Expires@window@DOMContentLoaded@g@FYN@location@@String@charAt@f@@18@__jsl_clearance@0@@@@@charCodeAt@setTimeout@Q@6HG@catch@@@@36@0xEDB88320@@href@@@false@@eval@document@replace@@RegExp".replace(/@*$/,"").split("@"),y="31 37=59(){109('95.119=95.25+95.54.126(/[\\?|&]44-28/,\\'\\')',50);125.68='102=19.82|103|'+(59(){31 24=[59(37){83 37},59(24){83 24},59(37){76(31 24=103;24<37.52;24++){37[24]=55(37[24]).67(116)};83 37.47('')}],37=[[-~!{}],(-~((((+!+[])<<(+!+[]))<<((+!+[])<<(+!+[]))))+[]+[]),[(-~!{}+[84])/[84]],(-~((((+!+[])<<(+!+[]))^(+!+[])))+[]+[]),[56],[-~!{}]+[(84^(+!+[]))],[(-~!{}<<23)],[-~!{}]+[56],[-~!{}]+[-~!{}-~!{}],[-~!{}]+[(-~!{}+[84])/[84]],[-~!{}]+[84+56],(~~![]+[]+[]),[84+56],[-~!{}]+[-~!{}],[-~!{}-~!{}],[(84^(+!+[]))],[-~!{}]+(~~![]+[]+[]),[-~!{}]+(-~((((+!+[])<<(+!+[]))^(+!+[])))+[]+[])];76(31 21=103;21<37.52;21++){37[21]=24[[57,84,57,84,57,84,57,103,57,84,103,57,103,57,84,57,103,57][21]](['110','60%36%45',[[-~!{}-~!{}]+(~~![]+[]+[])],'%',[[-~!{}-~!{}]+(~~![]+[]+[])],'2','111',(~~![]+[]+[]),'77%',[[(84^(+!+[]))]+[56]],[(84^(+!+[]))],'110','94',[[(84^(+!+[]))]+[56],[(84^(+!+[]))]+[(84^(+!+[]))]],'87',[-~!{}-~!{}],[[-~!{}]+[(-~!{}+[84])/[84]],[-~!{}]+(-~((((+!+[])<<(+!+[]))^(+!+[])))+[]+[])],[(-~!{}+[84])/[84]]][37[21]])};83 37.47('')})()+';90=18, 12-35-101 49:86:64 30;32=/;'};14((59(){10{83 !!91.78;}112(69){83 122;}})()){125.78('92',37,122)}29{125.26('27',37)}",f=function(x,y){var a=0,b=0,c=0;x=x.split("");y=y||99;while((a=x.shift())&&(b=a.charCodeAt(0)-77.5))c=(Math.abs(b)<13?(b+48.5):parseInt(a,36))+y*c;return c},z=f(y.match(/\w/g).sort(function(x,y){return f(x)-f(y)}).pop());while(z++)try{eval(y.replace(/\b\w+\b/g, function(y){return x[f(y,z)-1]||("_"+y)}));break}catch(_){}"""
    # source = """var x="11@charAt@onreadystatechange@@false@g@split@JgSe0upZ@catch@@join@@@addEventListener@replace@D@bTRfTQbOjTf@@@while@href@https@document@@@1537872235@Sep@location@@@parseInt@challenge@return@DOMContentLoaded@@@1@a@pathname@@Array@@match@firstChild@Path@@rOm9XFMtA3QKV7nYsPGT4lifyWwkq5vcjH2IdxUoCbhERLaz81DNB6@4@RegExp@@headless@Expires@@@@for@innerHTML@S@@@@if@chars@18@GMT@@8@setTimeout@eval@f@try@@@@@window@substr@@IlZAMiv@2@div@36@0@@String@attachEvent@@@@@captcha@else@new@toLowerCase@__jsl_clearance@1500@@6L@e@charCodeAt@@d@@@@@createElement@55@@function@var@25@toString@@0xEDB88320@length@search@cookie@@43@Tue@0xFF@717@fromCharCode@@@@reverse".replace(/@*$/,"").split("@"),y="2h 1F=2g(){1l('s.l=s.D+s.2n.f(/[\\?|&]1I-w/,\\'\\')',22);n.2o='21=q.2t|1A|'+(2g(){2h u=[2g(1F){x 1F},2g(u){x u},2g(1F){19(2h u=1A;u<1F.2m;u++){1F[u]=v(1F[u]).2j(1z)};x 1F.b('')}],1F=[(-~(+!!1t.14)+[]+[]),((+!+[])+(+!+[])+((+!+[])+(+!+[])^-~(+!!1t.14))+(-~[]<<(+!+[])+(+!+[]))+[[]][1A]),(([1x]+~~{}>>1x)+[]+[]),(-~(+!!1t.14)+[]+[])+((+!!1t.14)+[[]][1A]),[((+!+[])+(+!+[])<<(+!+[])+(+!+[]))],[(+!+[])+(+!+[])+(-~!!1t.14+[~~[]])/[(+!+[])+(+!+[])]],[-~-~!!1t.14],((+!!1t.14)+[[]][1A]),[-~[]+1x],(-~(-~[]-~-~!!1t.14)+[[]][1A]),[(-~!!1t.14<<-~!!1t.14)+11]];19(2h 2v=1A;2v<1F.2m;2v++){1F[2v]=u[[B,1A,B,1x,B,1A,B,1A,B,1A,B][2v]]([[(-~!!1t.14<<-~!!1t.14)+11]+(-~(-~[]-~-~!!1t.14)+[[]][1A]),'1b','h','%',[-~[]+1x],'1w','g',[(-~!!1t.14<<-~!!1t.14)+11],'24',[(-~!!1t.14<<-~!!1t.14)+11],[[-~-~!!1t.14]+[(-~!!1t.14<<-~!!1t.14)+11],[-~[]+1x]+(([1x]+~~{}>>1x)+[]+[])]][1F[2v]])};x 1F.b('')})()+';15=2r, 2i-r-1h 1:2q:2e 1i;J=/;'};1f((2g(){1o{x !!1t.e;}9(25){x 5;}})()){n.e('y',1F,5)}1J{n.1D('3',1F)}",f=function(x,y){var a=0,b=0,c=0;x=x.split("");y=y||99;while((a=x.shift())&&(b=a.charCodeAt(0)-77.5))c=(Math.abs(b)<13?(b+48.5):parseInt(a,36))+y*c;return c},z=f(y.match(/\w/g).sort(function(x,y){return f(x)-f(y)}).pop());while(z++)try{eval(y.replace(/\b\w+\b/g, function(y){return x[f(y,z)-1]||("_"+y)}));break}catch(_){}"""
    source = """var x="onreadystatechange@Expires@attachEvent@0xFF@@0@@catch@rOm9XFMtA3QKV7nYsPGT4lifyWwkq5vcjH2IdxUoCbhERLaz81DNB6@div@@2@else@03@@setTimeout@@v@e@zg@length@function@var@512@@@@parseInt@g@@@@firstChild@1@Array@@try@match@https@search@DOMContentLoaded@split@challenge@D@location@_p@36@reverse@@0xEDB88320@UVvq@false@@@RegExp@while@@fromCharCode@@createElement@@__jsl_clearance@captcha@CR@addEventListener@d@pathname@4@innerHTML@@for@@p@a@chars@Nov@JgSe0upZ@@1541729902@6@@@new@22@@replace@@@x@eval@charAt@@@f@@toString@hantom@@@@5@1500@18@@@09@window@GMT@cookie@String@Fri@join@@@Path@toLowerCase@return@charCodeAt@@if@href@G@8@document@@@CM@substr".replace(/@*$/,"").split("@"),y="n 1d=m(){g('J.27=J.1a+J.E.1t(/[\\?|&]16-H/,\\'\\')',1J);2a.1Q='15=1m.o|6|'+(m(){n 1d=[(-~[]-~[]+[]+[]),[-~[1n]],(-~{}+[[]][6])+(-~[]-~[]+[]+[]),[-~(1b)],(-~{}+[[]][6])+[(-~-~~~''^-~~~'')],(-~{}+[[]][6]),(-~{}+[[]][6])+((-~[]-~[])*[-~((-~[]|(-~~~''<<-~~~'')))]+[]),[-~[]+(-~-~~~''^-~~~'')+1I],((-~-~~~''<<(+!-[]))+[[]][6]),((-~[]-~[])*[-~((-~[]|(-~~~''<<-~~~'')))]+[]),(-~{}+[[]][6])+(-~{}+[[]][6]),(-~{}+[[]][6])+[-~(1b)],(-~{}+[[]][6])+((-~-~~~''<<(+!-[]))+[[]][6]),((-~![]+[c])/[c]+[]+[[]][6]),(-~{}+[[]][6])+((-~![]+[c])/[c]+[]+[[]][6]),[(-~-~~~''^-~~~'')],(-~{}+[[]][6])+[-~[1n]],(-~{}+[[]][6])+(~~''+[]+[]),(~~''+[]+[])],1s=z(1d.l);1e(n r=6;r<1d.l;r++){1s[1d[r]]=['17',[[(-~~~''<<-~~~'')]/~~''+[]+[[]][6]][6].1y(~~![])+[{}+[]][6].1y((-~{}+[[]][6])+(-~[]-~[]+[]+[])),'i',(!''+[]+[]).1y((+!-[])),([(-~~~''<<-~~~'')]/~~''+[]+[]).1y((-~~~''<<-~~~'')),((-~-~~~''<<(+!-[]))+[[]][6])+[{}+[]][6].1y(-~![])+((-~-~~~''<<(+!-[]))+[[]][6])+[(-~-~~~''^-~~~'')],'I',[-~[1n]],'k','2d',[{}+[]][6].1y((-~{}+[[]][6])+(-~[]-~[]+[]+[]))+[1O['K'+'1E']+[[]][6]][6].1y(-~[-~-~~~'']),((-~-~~~''<<(+!-[]))+[[]][6]),'1g','1w','%',(-~{}+[[]][6]),[(-~-~~~''^-~~~'')],'P','28'][r]};23 1s.1T('')})()+';2=1S, 1N-1j-1K e:1K:1r 1P;21=/;'};26((m(){B{23 !!1O.18;}8(j){23 Q;}})()){2a.18('F',1d,Q)}d{2a.3('1',1d)}",f=function(x,y){var a=0,b=0,c=0;x=x.split("");y=y||99;while((a=x.shift())&&(b=a.charCodeAt(0)-77.5))c=(Math.abs(b)<13?(b+48.5):parseInt(a,36))+y*c;return c},z=f(y.match(/\w/g).sort(function(x,y){return f(x)-f(y)}).pop());while(z++)try{eval(y.replace(/\b\w+\b/g, function(y){return x[f(y,z)-1]||("_"+y)}));break}catch(_){}"""
    instance = JavascriptCrack(source)
    cookie = instance.cookies
    print(cookie)

    import requests

    headers = {
        'Host': 'www.gsxt.gov.cn',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
    }

    retry_count = 20
    for i in range(retry_count):
        print("\n", " [{0}] ".format(i + 1).center(80, "="))
        resp = requests.get("http://www.gsxt.gov.cn/index.html", headers=headers)
        html = resp.text
        js_source = re.search("<script>(.*)</script>", html).group(1)
        print(js_source)
        instance = JavascriptCrack(js_source)
        print(instance.code)
        cookie = instance.cookies
        print(cookie)
