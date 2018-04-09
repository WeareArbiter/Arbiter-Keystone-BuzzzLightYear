from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import math
import os
import pandas as pd
from random import randint
import requests
import re
import time

from stockapi.models import Ticker
from gobble.Crawler import Crawler


class OhlcvCrawler(Crawler):

    def __init__(self):
        super().__init__()

    def scrape_ohlcv(self):
        upd_num = 0
        ticker = Ticker.objects.lasts()
        recent_update_date = ticker.kd_ohlcv.date
        market_ohlcv = {'KOSPI':KospiOHLCV, 'KOSPDAQ':KosdaqOHLCV, 'ETF':KospiOHLCV}
        for market in ['KOSPI', 'KOSDAQ', 'ETF']:
            if recent_update_date != self.today_date:
                tickers = Ticker.objects.filter(market_type=market).filter(state=True)
                for ticker in tickers:
                    code = ticker
                    if market_ohlcv[market].objects.filter(code=code).filter(date=self.today_date).exists():
                        print('{} {} already updated. Skipping...'.format(str(upd_num), code))
                        upd_num += 1
                        continue
                    else:
                        print('{} {}'.format(str(upd_num), url))
                        df = pd.read_html(self.ohlcv_url.format(ticker.code), thousands='')
                        df = df[0]
                        ohlcv_list = []
                        index = 1
                        while index:
                            try:
                                date = str(df.ix[index][0].replace(".", ""))
                                if date == recent_update_date:
                                    break
                                else:
                                    open_price = int(df.ix[index][3].replace(",", ""))
                                    high_price = int(df.ix[index][4].replace(",", ""))
                                    low_price = int(df.ix[index][5].replace(",", ""))
                                    close_price = int(df.ix[index][1].replace(",", ""))
                                    volume = int(df.ix[index][6].replace(",", ""))
                                    data = market_ohlcv[market](date=date,
                                                                code=code,
                                                                open_price=open_price,
                                                                high_price=high_price,
                                                                low_price=low_price,
                                                                close_price=close_price,
                                                                volume=volume,)
                                    ohlcv_list.append(data)
                                    print(str(upd_num)+ ' added ' + code + ' data')
                                    index += 1
                            except:
                                break
                        market_ohlcv[market].objects.bulk_create(ohlcv_list)
                        upd_num += 1
