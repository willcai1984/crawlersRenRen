# -*- coding: utf-8 -*-
"""
    spider.spider.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
import http.cookiejar
import urllib.error
import urllib.parse
import urllib.request
from urllib.request import HTTPCookieProcessor, ProxyHandler


class Spider(object):
    def __init__(self, proxy=""):
        # 生成cookie池
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(HTTPCookieProcessor(self.cookie))
        if proxy:
            self.opener = urllib.request.build_opener(HTTPCookieProcessor(self.cookie), ProxyHandler({'http': proxy}))
        urllib.request.install_opener(self.opener)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    def __del__(self):
        self.opener.close()

    def get_content(self, url, data=''):
        if data:
            req = urllib.request.Request(url, data, headers=self.headers)
        else:
            req = urllib.request.Request(url, headers=self.headers)
        res = urllib.request.urlopen(req, timeout=10)
        content = res.read()
        return content
