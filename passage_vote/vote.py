#!/usr/bin/python  
#coding=utf-8  

from HTMLParser import HTMLParser
import re
import os
import sys
import time
import urllib  
import urllib2 
import cookielib

def on_login():
	posturl = "http://net.tsinghua.edu.cn/cgi-bin/do_login"
	req = urllib2.Request(posturl)
	req.add_header("Host" , "net.tsinghua.edu.cn")
	req.add_header("Connection" , "keep-alive")
	#req.add_header("Content-Length" , "76")
	#req.add_header("Cache-Control" , "max-age=0")
	req.add_header("Accept" , "*/*")
	req.add_header("Origin" , "http://net.tsinghua.edu.cn")
	req.add_header("User-Agent" , "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")
	req.add_header("Content-Type" , "application/x-www-form-urlencoded")
	req.add_header("Referer" , "http://net.tsinghua.edu.cn/wired/")
	req.add_header("Accept-Encoding" , "gzip,deflate,sdch")
	req.add_header("Accept-Language" , "zh-CN,zh;q=0.8")
	req.add_header("Cookie" , "tunet=xjl11%0Ax422622l%40")
	data = {'username':'xjl11', 'password':'eb6b8981845cb17d9e9dac7d003b5075', 'drop':'0', 'type':'1', 'n':'100'}
	data = urllib.urlencode(data)
	#enable cookie
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(req, data)
	rdata = response.read()
	return rdata.find('0')
	
def on_logout():
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
	return rdata.find('ok')
	
def on_dovote(values):
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
	cookie = '%s%s%s' %('ASP.NET_SessionId=', values[2], '; AJSTAT_ok_pages=1; AJSTAT_ok_times=1')
	#print cookie
	req.add_header("Cookie" , cookie)
	validCode = raw_input("please type in the valid code:\n")
	#print validCode
	validCode = validCode.decode('gb2312').encode('utf-8')
	data = {'__VIEWSTATE':values[0], '__EVENTVALIDATION':values[1], 'tbVN':validCode, 'Button1':'支 持', 'textbox6':''}
	#print data
	data = urllib.urlencode(data)
	#enable cookie
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(req, data)
	rdata = response.read()
	return rdata.find("投票成功")

def on_getvalues():
	hp = MyHTMLParser()
	
	cookie = cookielib.CookieJar()
	posturl = "http://www.bschaowen.com/mwsx.aspx?nid=1540"
	req = urllib2.Request(posturl)
	req.add_header("Host" , "www.bschaowen.com")
	req.add_header("Connection" , "keep-alive")
	req.add_header("Cache-Control" , "max-age=0")
	req.add_header("Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.add_header("Origin" , "http://www.bschaowen.com")
	req.add_header("User-Agent" , "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")
	req.add_header("Content-Type" , "application/x-www-form-urlencoded")
	req.add_header("Referer" , "http://www.bschaowen.com/mwsx.aspx?nid=1540")
	req.add_header("Accept-Encoding" , "gzip,deflate,sdch")
	req.add_header("Accept-Language" , "zh-CN,zh;q=0.8")
	#req.add_header("Cookie" , "ASP.NET_SessionId=ptrcr22wfut0gi204d4oeqb4; AJSTAT_ok_pages=1; AJSTAT_ok_times=1")
	#enable cookie
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open(req)
	page = response.read()
	
	hp.feed(page)
	hp.close()
	
	for item in cookie:
		if item.name == 'ASP.NET_SessionId':
			print item.value
			hp.values[2] = item.value
	return hp.values
	
def on_getValidCode(sessionID):
	posturl = "http://www.bschaowen.com/images.aspx"
	req = urllib2.Request(posturl)
	req.add_header("Host" , "www.bschaowen.com")
	req.add_header("Connection" , "keep-alive")
	req.add_header("Cache-Control" , "max-age=0")
	req.add_header("Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.add_header("Origin" , "http://www.bschaowen.com")
	req.add_header("User-Agent" , "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")
	req.add_header("Content-Type" , "application/x-www-form-urlencoded")
	req.add_header("Referer" , "http://www.bschaowen.com/mwsx.aspx?nid=1540")
	req.add_header("Accept-Encoding" , "gzip,deflate,sdch")
	req.add_header("Accept-Language" , "zh-CN,zh;q=0.8")
	cookie = '%s%s%s' %('ASP.NET_SessionId=', sessionID, '; AJSTAT_ok_pages=1; AJSTAT_ok_times=1')
	#print cookie
	req.add_header("Cookie" , cookie)
	#enable cookie
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(req)
	imgData = response.read()
	
	with open('valid.gif', "wb") as gif:
		gif.write(imgData)
		gif.close()
	os.system('valid.gif')

	
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.values = []
 
    def handle_startendtag(self, tag, attrs):
        if tag == "input":
            if len(attrs) == 0: 
				pass
            else:
                for (variable, value)  in attrs:
                    if variable == "value":
                        self.values.append(value)

if __name__ == "__main__":
	os.system('chrome')
	time.sleep(1)
	print "welcome~~"
	os.system('chrome http://www.bschaowen.com/mwsx.aspx?nid=1540')
	print "verify session, sleep 8 sec..."
	time.sleep(4)
	print "wake up..."
	values = on_getvalues()
	if len(values) > 2:
		sessionID = values[2]
		on_getValidCode(sessionID)
		print on_dovote(values)
		on_logout()
	while True:
		os.system('chrome')
		#get old ip
		os.system('ipconfig > oldip.txt')
		oldIPFile = open('oldip.txt')
		ipStr = oldIPFile.read()
		oldIPFile.close()
		pattern = re.compile(r'(.*?)(Fi)(.*?)(IPv4)([^\d]*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*)', re.DOTALL)
		match = pattern.match(ipStr)
		oldIP = match.group(6)
		if match:
			print "Old IP: %s" %(oldIP)
		
		os.popen('ipconfig /release')
		time.sleep(5)
		os.system('netsh wlan disconnect')
		#print "sleep 20 sec after release..."
		#time.sleep(20)

		#get new ip
		os.system('ipconfig > newip.txt')
		newIPFile = open('newip.txt')
		ipStr = newIPFile.read()
		newIPFile.close()
		pattern = re.compile(r'(.*?)(Fi)(.*?)(IPv4)([^\d]*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*)', re.DOTALL)
		match = pattern.match(ipStr)
		newIP = match.group(6)
		if match:
			print "New IP: %s" %(newIP)
		if newIP[0:3] == '192':
			while True:
				os.system('netsh wlan connect name=Tsinghua')
				print "sleep 15 sec after connect..."
				time.sleep(15)
				print "wake up..."
				#get new ip
				os.system('ipconfig > newip.txt')
				newIPFile = open('newip.txt')
				ipStr = newIPFile.read()
				newIPFile.close()
				pattern = re.compile(r'(.*?)(Fi)(.*?)(IPv4)([^\d]*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*)', re.DOTALL)
				match = pattern.match(ipStr)
				newIP = match.group(6)
				if match:
					print "New IP: %s" %(newIP)
				if cmp(newIP[0:3], oldIP[0:3]) == 0:
					if newIP != oldIP:
						print "change ip success!"
						if on_login() >= 0:
							print "login success, keep going"
							os.system('chrome http://www.bschaowen.com/mwsx.aspx?nid=1540')
							print "verify session, sleep 8 sec..."
							time.sleep(4)
							print "wake up..."
							values = on_getvalues()
							if len(values) <= 2:
								continue
							sessionID = values[2]
							on_getValidCode(sessionID)
							result = on_dovote(values)
							print result
							while result == -1:
								os.system('chrome http://www.bschaowen.com/mwsx.aspx?nid=1540')
								print "verify session, sleep 8 sec..."
								time.sleep(4)
								print "wake up..."
								values = on_getvalues()
								if len(values) <= 2:
									continue
								sessionID = values[2]
								on_getValidCode(sessionID)
								result = on_dovote(values)
								print result							
							on_logout()
							break
						else:
							print "login fail, logout and try again..."
							on_logout()
							if on_login() >= 0:
								print "login success, keep going"
								os.system('chrome http://www.bschaowen.com/mwsx.aspx?nid=1540')
								print "verify session, sleep 8 sec..."
								time.sleep(4)
								print "wake up..."
								values = on_getvalues()
								if len(values) <= 2:
									continue
								sessionID = values[2]
								on_getValidCode(sessionID)
								result = on_dovote(values)
								print result
								while result == -1:
									os.system('chrome http://www.bschaowen.com/mwsx.aspx?nid=1540')
									print "verify session, sleep 8 sec..."
									time.sleep(4)
									print "wake up..."
									values = on_getvalues()
									if len(values) <= 2:
										continue
									sessionID = values[2]
									on_getValidCode(sessionID)
									result = on_dovote(values)
									print result							
								on_logout()
								break
							else:
								print "give up, restart..."
					else:
						
						os.popen('ipconfig /release')
						os.system('netsh wlan disconnect')
						#print "sleep 20 sec after release..."
						#time.sleep(20)
				else:
					os.system('netsh wlan disconnect')
					time.sleep(3)
		else:
			os.system('ipconfig /release')