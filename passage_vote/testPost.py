#!/usr/bin/python  
#coding=utf-8  
  
import urllib  
import urllib2  

posturl = "http://www.bschaowen.com/mwsx.aspx?nid=1540"
req = urllib2.Request(posturl)
req.add_header("Host" , "www.bschaowen.com")
req.add_header("Connection" , "keep-alive")
#req.add_header("Content-Length" , "465")
req.add_header("Cache-Control" , "max-age=0")
req.add_header("Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
req.add_header("Origin" , "http://www.bschaowen.com")
req.add_header("User-Agent" , "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")
req.add_header("Content-Type" , "application/x-www-form-urlencoded")
req.add_header("Referer" , "http://www.bschaowen.com/mwsx.aspx?nid=1540")
req.add_header("Accept-Encoding" , "gzip,deflate,sdch")
req.add_header("Accept-Language" , "zh-CN,zh;q=0.8")
req.add_header("Cookie" , "ASP.NET_SessionId=ptrcr22wfut0gi204d4oeqb4; AJSTAT_ok_pages=0; AJSTAT_ok_times=0")
data = {'__VIEWSTATE':'/wEPDwUJMTc5NjE1MjIzDxYCHgVPbGVEYgVfc2VsZWN0ICogZnJvbSBtaXJfc2FsZWl0ZW1fc29ydCB3aGVyZSBuZXdzaWQ9MTU4NiBhbmQgbnVtIDwgMSBvcmRlciBieSB6aiBkZXNjLCBjYXRlZ29yeWlkIGRlc2MWBAIDD2QWAgIGDw8WAh4LUmVjb3JkY291bnRmZGQCBA8PFgIeBFRleHQFBDc5ODFkZGREAaRvtRL7NtJ2s/GvU3qm8wBOUA==', '__EVENTVALIDATION':'/wEWBgKv7b+kDgLosfHEBwKM54rGBgK7q7GGCAKsysbGDwKOgbnmDxgR72LepxW4D7v/NqL9+XNEGOMM', 'tbVN':'严以确今', 'Button1':'支 持', 'textbox6':''}
data = urllib.urlencode(data)
#enable cookie
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
response = opener.open(req, data)
rdata = response.read()
print rdata



