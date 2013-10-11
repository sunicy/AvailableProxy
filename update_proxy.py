# encoding: utf-8

import urllib2
import re

URL_BASE = "http://www.cnproxy.com/proxy%d.html"
PAGE_COUNT = 10

var_assign_pattern = re.compile('([a-zA-Z])="([0-9])";')
proxy_pattern = re.compile("<td>(\\d+\.\\d+\.\\d+\.\\d+)<SCRIPT.*?\":\"([a-z+]+)\)")
port_pattern = re.compile("\+([a-z])")

proxy_list = []

f = open("proxy.txt", "w")

for page in xrange(PAGE_COUNT):
    page += 1
    url = URL_BASE % page
    content = urllib2.urlopen(url).read().decode("gbk").encode("utf-8")
    #content = open("sample.txt", "r").read()
    var = dict((x, y) for x, y in var_assign_pattern.findall(content))
    for p in proxy_pattern.findall(content):
        proxy = p[0] + ":" + (
            "".join([var[i] for i in port_pattern.findall(p[1])]))
        proxy_list.append(proxy)
    print "Page.", page, " done."

f.write("\n".join(proxy_list) + "\n")
f.close()
    
