#! /usr/bin/env python
# -*- coding: utf-89 -*-
import random
import urllib2
import time
import urlparse
from datetime import datetime, timedelta
import socket

from define import *

from chap_one.throttle import Throttle

class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 opener=None, cache=None):
        """
        页面下载器初始化
        :param delay:
        :param user_agent:
        :param proxies:
        :param num_retries:
        :param cache:
        """

        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache and re-download
                    result = None
            if result is None:
                # result was not loaded from cache so still need to download
                self.throttle.wait(url)
                proxy = random.choice(self.proxies) if self.proxies else None
                headers = {'User-agent': self.user_agent}
                result = self.download(url, headers, proxy, self.num_retries)
                if self.cache:
                    # save result to cache
                    self.cache[url] = result
        return result

    def download(self, url, headers, proxy, num_retries, data=None):
        print 'Downloading: %s' % url
        request = urllib2.Request(url, data, headers or {})
        opener = self.opner or urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print "Download error:", str(e)
            html = ''
            if hasattr(e, 'code'):
                if num_retries > 0 and 500 < e.code < 600:
                    return self.download(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html':html, 'code': code}



