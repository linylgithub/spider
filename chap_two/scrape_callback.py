#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import lxml.html


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w'))
        self.fields = ('url', 'area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code',
                       'currency_name','phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                if field == 'url':
                    row.append(url)
                else:
                    re_css = 'table > tr#places_{}__row > td.w2p_fw'.format(field)
                    value = tree.cssselect(re_css)
                    print '%s: %s' % (re_css, value)
                    if len(value) > 0:
                        row.append(value[0].text_content())
                    else:
                        row.append('')

            print row
            self.writer.writerow(row)
