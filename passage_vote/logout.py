#!/usr/bin/python  
#coding=utf-8  
  
import urllib  
import urllib2  

posturl = "http://net.tsinghua.edu.cn/cgi-bin/do_logout"
req = urllib2.Request(posturl)
req.add_header("Host" , "net.tsinghua.edu.cn")
req.add_header("Connection" , "keep-alive")
#req.add_header("Content-Length" , "76")
#req.add_header("Cache-Control" , "max-age=0")
req.add_header("Accept" , "*/*")
req.add_header("Origin" , "http://net.tsinghua.edu.cn")
req.add_header("User-Agent" , "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")
req.add_header("Content-Type" , "application/x-www-form-urlencoded")
#req.add_header("Referer" , "http://net.tsinghua.edu.cn/wired/")
req.add_header("Accept-Encoding" , "gzip,deflate,sdch")
req.add_header("Accept-Language" , "zh-CN,zh;q=0.8")
req.add_header("Cookie" , "tunet=xjl11%0Ax422622l%40")
data = {}
data = urllib.urlencode(data)
#enable cookie
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
response = opener.open(req, data)
rdata = response.read()
print rdata



