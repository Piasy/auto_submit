#!/usr/bin/python
#-*- coding: utf-8 -*-

import Image
import subprocess

import util
import errors

import HTMLParser 
import urlparse 
import urllib 
import urllib2 
import cookielib 
import string 
import re
import time

tesseract_exe_name = 'tesseract' # Name of executable to be called at command line
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
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
        call_tesseract(scratch_image_name, scratch_text_name_root)
        text = util.retrieve_text(scratch_text_name_root)
    finally:
        if cleanup:
            util.perform_cleanup(scratch_image_name, scratch_text_name_root)
    return text
     
def login(usr, pwd):
    ret = 0
    try:
        cj = cookielib.LWPCookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        urllib2.install_opener(opener) 
        #urllib2.urlopen('http://58.68.147.133/EXAMSF/public/index.jsp')
        imagesrc ='http://58.68.147.133/EXAMSF/public/frame/validateCode.jsp?temp=hxt3ufqh'
        data = urllib2.urlopen(imagesrc).read()  
        f = file('login.jpg',"wb")  
        f.write(data)  
        f.close() 
        im = Image.open('login.jpg')
        text = image_to_string(im)
        text = text.replace('\n', '')
        text = text.replace(' ', '')
        print 'login code= ' + text
        posturl = 'http://58.68.147.133/EXAMSF/public/manage/login.action'
        postData = (('examineeVo.identity', usr), ('examineeVo.password', pwd), ('inputValidateCode', text))
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData) 
        response = urllib2.urlopen(request)
        content = response.read()
        #print 'resp= ' + content
        
        #if (content.find('right.location.href =hreftmp;') == -1):
        #    ret = 0
        if len(content) > 0:
            ret = 1
    except Exception,ex:  
            print Exception,":",ex  
    return ret

def get_token(content):
    token = re.findall('<input type="hidden" name="token" value="([^"]*)">' , content)
    return token[0]


def try_pic():
    while login('431226199407145460', 'SHERRY714') == 0:
        print 'fail in login'   
    print 'Login success'
    eee = 1
    while eee == 1:
        try:
            #urllib2.urlopen('http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=main')
            #print 'open ok 1'
            #content = urllib2.urlopen('http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=bxSearch&p_xnxq=2013-2014-3&tokenPriFlag=bx').read()
            #print 'open ok 2'
            #token=get_token(content)
            #print 'token = ' + token

            posturl = 'http://58.68.147.133/EXAMSF/public/updateAjaxSelectGroup.action'
            imagesrc ='http://58.68.147.133/EXAMSF/public/frame/validateCode.jsp'
            data = urllib2.urlopen(imagesrc).read()  
            f = file('select.jpg',"wb")  
            f.write(data)  
            f.close() 
            im = Image.open('select.jpg')
            text = image_to_string(im)
            text = text.replace('\n', '')
            text = text.replace(' ', '')
            print 'select code= ' + text
            postData = (('examPlaceGroupExamineeVo.examPlaceGroupVo.id', '200'), ('validateCode', text))
            #postData = (('examPlaceGroupExamineeVo.examPlaceGroupVo.id', '200'), ('token', token), ('p_xnxq', '2013-2014-3'), ('tokenPriFlag', 'bx'), ('p_bxk_id', '2013-2014-3;40240595;1;'))
            postData = urllib.urlencode(postData)
            request = urllib2.Request(posturl, postData)
            #print 'open ok 3'
            response = urllib2.urlopen(request).read()
            print response
            #print 'open ok 4'
            #result = re.findall('showMsg\\("([^"]+)"\\)' , response)
            #print 'open ok 5'
            #try:
            #    print result[0]
            #except:
            #    print response
            #print 'open ok 6'
            #if response.find('课余量已无,不能再选') == -1:
            #    eee = 0
            time.sleep(2)
        except Exception,ex:  
            print Exception,":",ex  
        
    if response.find('成功') == -1:
        return 0
    else:
        return 1



if __name__=='__main__':
    
    while True:
        k = try_pic()
        if k == 1:
            break
