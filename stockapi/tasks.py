from __future__ import absolute_import, unicode_literals
from celery.decorators import task

from gobble.TickerCrawler import TickerCrawler


@task(name='crawl_ticker')
def crawl_ticker():
    tc = TickerCrawler()
    tc.scrape_ticker()
