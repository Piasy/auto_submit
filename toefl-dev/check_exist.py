#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import sgmllib, sys, os, string
import urllib, json
import re, urllib


class MyHTMLParser(sgmllib.SGMLParser):
    wanted = False
    field = "NONE"
    inner_html = ""
    post_param = {}
    freeSeats = []
    #count = 0


    def handle_data(self, data):
        #handle inner html in the current field
        if self.wanted:
            if self.field == "TD":
                self.inner_html += data.strip()

    def start_tr(self, attrs):
        #get in the td field
        self.wanted = True
        self.field = "TR"

    def end_tr(self):
        #get out the td field
        self.wanted = False
        self.field = "NONE"
        key = "有名额"
        if self.inner_html.find(key.decode('UTF-8').encode("GBK")) != -1:
            #print "inner_html = " + self.inner_html
            #print self.post_param
            self.freeSeats.append(self.post_param)
        self.inner_html = ""
        self.post_param = {}
        #if self.count > 9:
        #    quit()
        #self.count += 1

    def start_td(self, attrs):
        self.field = "TD"

    def end_td(self):
        self.field = "NONE"

    def start_input(self, attrs):
        self.field = "INPUT"
        if self.wanted:
            _name = "name"
            _value = "value"
            for name, value in attrs:
                if name == "name":
                    _name = value
                    break
            for name, value in attrs:
                if _name == "siteadmin" and name == "value":
                    _value = value
                    break
                elif _name == "Submit" and name == "onclick":
                    onclick = value
                    pattern = re.compile(r'(.*\')(.*)(\'.*)')
                    res = re.findall(pattern, onclick)
                    if res:
                        _value = res[0][1]
                    break
            if _name != "name" and _value != "value":
                if _name == "siteadmin":
                    self.post_param[_name] = _value
                elif _name == "Submit":
                    self.post_param["__act"] = _value

    def end_input(self):
        self.field = "NONE"

def check_existed(html, wanted):
    """@html: input html page; @wanted: wanted seats, json array"""
    parser = MyHTMLParser()
    parser.feed(html)
    print parser.freeSeats
    matched = []
    for seat in parser.freeSeats:
        for one in wanted:
            if seat["siteadmin"] == one["siteadmin"]:
                matched.append(seat)
    return matched

if __name__ == "__main__":
    html = open('data/seatPost2.htm').read()
    wanted = json.loads(open("config/wanted.config").read())
    matched = check_existed(html, wanted)
    print matched
    #print len(check_existed(html, wanted))
    #for one in matched:
    #    print urllib.urlencode((('__act', one["__act"]), ('siteadmin', one["siteadmin"]))) + "&Submit=%D7%A2%B2%E1"