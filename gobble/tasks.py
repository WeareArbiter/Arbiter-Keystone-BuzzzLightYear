import random, time
from datetime import datetime

from celery.decorators import task

from stockapi.models import Ticker
from gobble.TickerCrawler import TickerCrawler
from tracker.models import ProjectState

@task(name="scrape_stock_ticker")
def scrape_stock_ticker():
    start = time.time()
    tc = TickerCrawler()
    tc.scrape_ticker()
    end = time.time()

    # log process result
    today_date = datetime.today().strftime('%Y%m%d')
    todays_tickers_count = Ticker.objects.filter(date=today_date).count()
    if todays_tickers_count != 0:
        log = ProjectState(date=today_date,
                           task_name='TICKERS',
                           status=1,
                           log='scraped {} tickers'.format(todays_tickers_count),
                           time=end-start)
    else:
        log = ProjectState(date=today_date,
                           task_name='TICKERS',
                           status=0,
                           log='error scraping tickers, no tickers',
                           time=end-start)

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
