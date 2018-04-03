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

from stockapi.models import (
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    RecentKospiOHLCV,
    RecentKosdaqOHLCV,
    Info,
    )


class Crawler(object):
    '''
    - description: scrape KOSPI & KOSDAQ stock data from web page
    - ticker(daum), OHLCV(naver), Info(naver)
    '''
    def __init__(self):
        self.ticker_url = 'http://finance.daum.net/quote/volume.daum?stype={}&page={}'
        self.ohlcv_url = 'http://finance.naver.com/item/sise_day.nhn?code={}'
        self.info_url = 'http://finance.naver.com/item/coinfo.nhn?code={}'
        self.wisefn_url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cn=&cmp_cd={}'
        # etf_etn_checker
        self.etf_etn_url = 'https://comp.wisereport.co.kr/ETF/lookup.aspx'
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        self.market_dic = {'P':'KOSPI', 'Q':'KOSDAQ', 'E':'ETF', 'N':'ETN'}
        # today
        self.today_date = datetime.today().strftime('%Y%m%d')
        print("Crawler is ready ")

    def request_get(self, url, user_agent):
        self.req = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        return self.req

    def html_parser(self, req):
        self.soup = BeautifulSoup(req.text, 'html.parser')
        return self.soup

    def soup_findall(self, soup, tags, class_dict=None):
        # print(soup)
        self.source = soup.findAll(tags, class_dict)
        return self.source

    def etf_etn_checker(self, category=None):
        df1 = pd.read_html(self.etf_etn_url)
        df1 = df1[0]
        df1.columns = ['ETN/ETF','code','name']
        if category == 'etf':
            self.code_list = df1[df1['ETN/ETF'] == 'ETF']['code'].tolist()
            self.code_list = [str(code).zfill(6) for code in self.code_list]
        elif category == 'etn':
            self.code_list = df1[df1['ETN/ETF'] == 'ETN']['code'].tolist()
            self.code_list = [str(code).zfill(6) for code in self.code_list]
        else:
            self.code_list = df1['code'].tolist()
            self.code_list = [str(code).zfill(6) for code in self.code_list]
        return self.code_list

    def exist_code(self):
        code_value = Ticker.objects.all().values_list('code')
        if len(code_value) == 0:
            self.exists = []
        else:
            self.exists = [code[0] for code in code_value]
        return self.exists
