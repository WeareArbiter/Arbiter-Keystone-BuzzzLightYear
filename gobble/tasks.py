from __future__ import absolute_import, unicode_literals
from celery.decorators import task

import random, time
from datetime import datetime

from stockapi.models import Ticker
from gobble.TickerCrawler import TickerCrawler
from tracker.models import ProjectState

@task(name="scrape_stock_ticker")
def scrape_stock_ticker():
    try:
        start = time.time()
        tc = TickerCrawler()
        tc.scrape_ticker()
        end = time.time()

        # log process result
        today_date = datetime.today().strftime('%Y%m%d')
        ticker_count = Ticker.objects.all().count()
        log = ProjectState(date=today_date,
                           task_name='TICKERS',
                           status=1,
                           log='finished scraping tickers. Total ticker count: {}'.format(ticker_count),
                           time=end-start)
        log.save()

    except:
        # log process error
        today_date = datetime.today().strftime('%Y%m%d')
        log = ProjectState(date=today_date,
                           task_name='TICKERS',
                           status=0,
                           log='error scraping tickers, check again',
                           time=0)
        log.save()


@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)
