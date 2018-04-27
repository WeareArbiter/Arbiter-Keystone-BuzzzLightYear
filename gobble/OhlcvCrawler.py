from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import math
import os
import pandas as pd
from random import randint
import requests
import re
import time

from stockapi.models import (
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    )
from gobble.Crawler import Crawler


class OhlcvCrawler(Crawler):

    def __init__(self):
        super().__init__()

    def scrape_daily_ohlcv(self):
        A = time.time()
        success = False
        data_list = []
        market_ohlcv = {'KOSPI':KospiOHLCV, 'KOSDAQ':KosdaqOHLCV, 'ETF': KospiOHLCV, 'ETN':KospiOHLCV}
        last_ticker = Ticker.objects.filter(market_type='KOSDAQ').filter(state=True).order_by('code').last()
        ohlcv_url = self.ohlcv_url.format(last_ticker.code)
        df = pd.read_html(ohlcv_url, thousands='')
        last_date = str(df[0].ix[1][0].replace(",",""))
        exist_ohlcv = KosdaqOHLCV.objects.filter(date=last_date).exists()
        if exist_ohlcv:
            pass
        else:
            for market in ['KOSPI', 'ETF', 'ETN','KOSDAQ']:
                upt_n = 0
                tickers = Ticker.objects.filter(market_type=market).filter(state=True).order_by('code')
                #holiday check
                market_check_ticker = Ticker.objects.filter(market_type=market).filter(state=True).order_by('code').last()
                try:
                    last_update_date = market_ohlcv[market].objects.filter(code=market_check_ticker).order_by('date').last().date
                except AttributeError:
                    last_update_date = 0
                for ticker in tickers:
                    upt_n += 1
                    ohlcv_url = self.ohlcv_url.format(ticker.code)
                    df = pd.read_html(ohlcv_url, thousands='')
                    code = ticker
                    for i in range(1,df[0].shape[0]):
                        date = df[0].ix[i][0]
                        if type(date) == float:
                            continue
                        date = str(date).replace(".","")
                        if date == last_update_date:
                            break
                        print(date)
                        open_price = df[0].ix[i][3].replace(",","")  #시가
                        close_price = df[0].ix[i][1].replace(",","") #현재가, 종가
                        high_price = df[0].ix[i][4].replace(",","")  #고가
                        low_price = df[0].ix[i][5].replace(",","") #저가
                        volume = df[0].ix[i][6].replace(",","")
                        ohlcv_inst = market_ohlcv[market](date=date,
                                                         code=code,
                                                         open_price=open_price,
                                                         close_price=close_price,
                                                         high_price=high_price,
                                                         low_price=low_price,
                                                         volume=volume)
                        data_list.append(ohlcv_inst)
                    print(str(upt_n)+'/'+str(len(tickers)), ticker.name, 'complete')
            market_ohlcv[market].objects.bulk_create(data_list)
            success = True
            B = time.time()
            return success, "Data request complete", B-A
