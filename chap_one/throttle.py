#! /usr/bin/env python
#-*- coding=utf-8 -*-

import urlparse
import datetime
import time


class Throttle:
    """Add a delay between downloads for each domain"""
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domain = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domain.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
        if sleep_secs > 0 :
            # domain has been accessed recenty
            # so need to sleep
            time.sleep(sleep_secs)
        # update the last assessed time
        self.domain[domain] = datetime.datetime.now()