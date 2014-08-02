#!/usr/bin/python
#-*- coding: utf-8 -*-

import Image, subprocess
import util, errors, check_exist
import urlparse, urllib, urllib2, cookielib
import string, re, time, random, json
import smtplib
from email.mime.text import MIMEText

tesseract_exe_name = 'tesseract' # Name of executable to be called at command line
scratch_image_name = "1.bmp" # This file must be .bmp or other Tesseract-compatible format
clear_image_name = "2.bmp"
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation

def call_tesseract(input_filename, output_filename):
    args = [tesseract_exe_name, input_filename, output_filename]
    proc = subprocess.Popen(args)
    retcode = proc.wait()
    if retcode!=0:
        errors.check_for_errors()

def image_to_string(im, cleanup = cleanup_scratch_flag):
    try:
        util.image_to_scratch(im, scratch_image_name)
        call_tesseract(clear_image_name, scratch_text_name_root)
        text = util.retrieve_text(scratch_text_name_root)
    finally:
        if cleanup:
            util.perform_cleanup(scratch_image_name, scratch_text_name_root)
    return text

def test_very_code():
    im = Image.open('login.jpg')
    text = image_to_string(im, True)
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    return text

def time_milis():
    return int(round(time.time() * 1000))
     
def login(usr, pwd):
    try:
        #get cookie
        do_get('http://toefl.etest.net.cn/cn')
        util.log('get cookie')
        time.sleep(8)

        #get verify code
        veri_code = ''
        while len(veri_code) != 4:
            #/cn/14066434759580.704481621278VerifyCode3.jpg
            #cookie will be expired if get old url...
            #data = urllib2.urlopen('http://toefl.etest.net.cn/cn/14066434759580.704481621278VerifyCode3.jpg').read()
            data = do_get('http://toefl.etest.net.cn/cn/' + str(time_milis()) + str(random.random()) + 'VerifyCode3.jpg')
            f = file('login.jpg',"wb")  
            f.write(data)  
            f.close() 
            im = Image.open('login.jpg')
            veri_code = image_to_string(im)
            veri_code = veri_code.replace('\n', '')
            veri_code = veri_code.replace(' ', '')
            util.log('login text: ' + veri_code)
            time.sleep(8)
        util.log('login verify code: ' + veri_code)
        time.sleep(8)

        posturl = 'http://toefl.etest.net.cn/cn/TOEFLAPP'
        postData = (('username', usr), ('__act', '__id.24.TOEFLAPP.appadp.actLogin'), ('password', pwd), \
                ('LoginCode', veri_code), ('submit.x', '0'), ('submit.y', '0'))
        postData = urllib.urlencode(postData)
        content = do_post(posturl, postData)
        util.log('login post')
        if (content.find('MyHome/?') != -1):
            return 1
        else:
            return 0
    except Exception,ex:
        util.log(str(Exception) + ":" + str(ex))
        if str(ex).find("504") != -1 or str(ex).find("10054") != -1 or str(ex).find("104") != -1:
            time.sleep(180)
        return 0

def do_get(url):
    key1 = "访问被限制"
    key2 = "访问被禁止"
    
    data = urllib2.urlopen(url).read()
    t1 = data.find(key1.decode('UTF-8').encode("GBK")) != -1
    t2 = data.find(key2.decode('UTF-8').encode("GBK")) != -1

    if t1:
        open('deny.html', 'w').write(data)
        if not t2:
            util.log("WAIT!!!")
            time.sleep(10)
        else:
            util.log("ACCESS FORBIDAN!!!")
            time.sleep(1800)

    """
    while True:
        if t1:
            open('deny.html', 'w').write(data)
            if not t2:
                print "WAIT!!!"
                time.sleep(10)
                data = urllib2.urlopen(url).read()
                t1 = data.find(key1.decode('UTF-8').encode("GBK")) != -1
                t2 = data.find(key2.decode('UTF-8').encode("GBK")) != -1
            else:
                print "ACCESS FORBIDAN!!!"
                time.sleep(1800)
                break
        else:
            break
    """
    return data

def do_post(url, post):
    key1 = "访问被限制"
    key2 = "访问被禁止"
    request = urllib2.Request(url, post)
    
    response = urllib2.urlopen(request)
    data = response.read()
    t1 = data.find(key1.decode('UTF-8').encode("GBK")) != -1
    t2 = data.find(key2.decode('UTF-8').encode("GBK")) != -1
    
    if t1:
        open('deny.html', 'w').write(data)
        if not t2:
            util.log("WAIT!!!")
            time.sleep(10)
        else:
            util.log("ACCESS FORBIDAN!!!")
            time.sleep(1800)

    """
    while True:
        if t1:
            open('deny.html', 'w').write(data)
            if not t2:
                print "WAIT!!!"
                time.sleep(10)
                response = urllib2.urlopen(request)
                data = response.read()
                t1 = data.find(key1.decode('UTF-8').encode("GBK")) != -1
                t2 = data.find(key2.decode('UTF-8').encode("GBK")) != -1
            else:
                print "ACCESS FORBIDAN!!!"
                time.sleep(1800)
                break
        else:
            break
    """
    return data

def get_seat_query_code():
    veri_code = ""
    html = do_get('http://toefl.etest.net.cn/cn/CityAdminTable')
    pattern = re.compile(r'(.*src=\")(.*)(\.VerifyCode2\.jpg)(\".*)')
    res = re.findall(pattern, html)
    if res:
        data = do_get('http://toefl.etest.net.cn' + res[0][1] + res[0][2])
        f = file('seatQuery.jpg',"wb")  
        f.write(data)  
        f.close() 
        im = Image.open('seatQuery.jpg')
        veri_code = image_to_string(im)
        veri_code = veri_code.replace('\n', '')
        veri_code = veri_code.replace(' ', '')
        util.log('seat text: ' + veri_code)
    else:
        util.log("bad seat query page")
        return "relogin"
    return veri_code

def try_pic():
    cj = cookielib.LWPCookieJar()
    cookie = urllib2.HTTPCookieProcessor(cj)
    #proxy option
    #proxy = urllib2.ProxyHandler({'http':'http://127.0.0.1:1080/'})
    #import socks
    #proxy = SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, 'localhost', 1080)
    #opener=urllib2.build_opener(proxy, cookie)
    opener=urllib2.build_opener(cookie)
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)
    conf = json.loads(open("config/login.config").read())
    while login(conf['username'], conf['password']) == 0:
        util.log('fail in login')
        time.sleep(8)
    util.log('Login success')

    html = ""
    key = "名额"
    while html.find(key.decode('UTF-8').encode("GBK")) == -1:
        try:
            util.log("query seat fail")
            veri_code = ""
            count = 0
            #print "outer count = ", count
            while len(veri_code) != 4:
                #print "inner count = ", count
                if count > 10:
                    return 0
                try:
                    veri_code = get_seat_query_code()
                    #print "return seat text:", veri_code
                except Exception,ex:
                    util.log(str(Exception) + ":" + str(ex) + ", " + str(count))
                    count += 1
                    if str(ex).find("504") != -1 or str(ex).find("10054") != -1 or str(ex).find("104") != -1:
                        time.sleep(180)
                        return 0
                if veri_code == "relogin":
                    return 0
                time.sleep(8)
            util.log("seat VerifyCode: " + veri_code)
            queryUrl = 'http://toefl.etest.net.cn/cn/SeatsQuery?afCalcResult=' + veri_code \
                    + json.loads(open("config/city_time.config").read())["partsurl"]
            html = do_get(queryUrl)
        except Exception,ex:
            util.log(str(Exception) + ":" + str(ex))
            if str(ex).find("504") != -1 or str(ex).find("10054") != -1 or str(ex).find("104") != -1:
                time.sleep(180)
                return 0

    matched = check_exist.check_existed(html, json.loads(open("config/wanted.config").read()))
    util.log("matched size: " + str(len(matched)))
    #TODO add post action, and surround with while loop
    try:
        if len(matched) != 0:
            for one in matched:
                send_email("xz4215@163.com", "TOEFL SEAT AVAILABLE", one["siteadmin"])
                send_email("thierryhenrytracy@163.com", "TOEFL SEAT AVAILABLE", one["siteadmin"])
                """
                postData = (('__act', one["__act"]), ('siteadmin', one["siteadmin"]))
                postData = urllib.urlencode(postData) + "&Submit=%D7%A2%B2%E1"
                request = urllib2.Request(posturl, postData) 
                response = urllib2.urlopen(request)
                content = response.read()
                print 'seat post'
                """
            return 1
    except Exception,ex:
        util.log(str(Exception) + ":" + str(ex))
        if str(ex).find("504") != -1 or str(ex).find("10054") != -1 or str(ex).find("104") != -1:
            time.sleep(180)
            return 0
    return 0

def send_email(addr, sub, cont):
    msg = MIMEText(cont)
    me = "lavlav@126.com"
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = addr

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP()
    s.connect('smtp.126.com')
    s.login('lavlav', '1qaz2wsx')
    s.sendmail(me, [addr], msg.as_string())
    s.quit()

if __name__=='__main__':
    while True:
        k = try_pic()
        if k == 1:
            break
