from HTMLParser import HTMLParser
import urllib  
import urllib2  
import os
import sys
import time
import re
 
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
	print rdata
	return rdata.find('ok')
	
if __name__ == "__main__":
	on_logout()
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
						break
	else:
		os.popen('ipconfig /release')
		os.system('netsh wlan disconnect')