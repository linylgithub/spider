#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import lxml.html
import lxml.cssselect

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name',
          'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')


def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
        return results


def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr', id='places_%s__row' % field).find('td', class_='w2p_fw').text
    return results


def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content()
    return results


if __name__ == '__main__':
    import time
    from chap_one.link_crawler3 import download

    NUM_ITERATIONS = 1000 # number of times to test each scraper
    html = download('http://example.webscraping.com/places/default/view/Aland-Islands-2',headers={'User-agent':'wswp'},
                 proxy=None, num_retries=1)
    for name, scraper in [('Regular expressions', re_scraper),('BeautifulSoup',bs_scraper),
                          ('Lxml', lxml_scraper)]:
        # record start time of space
        start = time.time()
        for i in range(NUM_ITERATIONS):
            if scraper == re_scraper:
                re.purge()
            result = scraper(html)
            # check scraped result is as expected
            assert (result['area'] == '1,580 square kilometres')
        # record end_time of scrape adn output the total
        end = time.time()
        print '%s: %.2f seconds' % (name, end - start)



