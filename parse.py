# encoding: utf-8

import urllib2
import time
import signal

PROXY_FILE = 'proxy.txt'
PROXY_LIST = ['', ]
PROXY_INDEX = 1

GOOD_PROXY = []
fok = None

def signal_handler(signal, frame):
    import os
    os._exit(0)

def fetch(url):
    global GOOD_PROXY
    global PROXY_INDEX
    while True:
        try:
            proxy = urllib2.ProxyHandler({
                        'http': PROXY_LIST[PROXY_INDEX]
                    }) if PROXY_INDEX > 0 else None
            opener = urllib2.build_opener(proxy) if (
                        proxy != None) else urllib2.build_opener()
            urllib2.install_opener(opener)

            t = urllib2.urlopen(url, timeout=4).read()
            GOOD_PROXY += [PROXY_LIST[PROXY_INDEX],]
            fok.write(PROXY_LIST[PROXY_INDEX] + '\n')
            fok.flush()
            print PROXY_LIST[PROXY_INDEX], " .. OK"
        except:
            print PROXY_LIST[PROXY_INDEX], " .. BAD"
            if (PROXY_INDEX >= len(PROXY_LIST)):
                return None
        PROXY_INDEX = (PROXY_INDEX + 1)

def load_proxy_list():
    global PROXY_LIST
    f = open(PROXY_FILE)
    for line in f.readlines():
        PROXY_LIST += [line.strip(), ]
    f.close()


if __name__ == '__main__':
    global fok
    fok = open('proxy_ok.txt', 'w')
    signal.signal(signal.SIGINT, signal_handler)
    load_proxy_list()
    while True:
        if fetch('http://www.baidu.com') == None:
            break
    fok.close()
