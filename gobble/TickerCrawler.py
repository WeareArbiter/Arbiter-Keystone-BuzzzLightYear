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

class TickerCrawler(Crawler):

    def __init__(self):
        super().__init__()

    def scrape_ticker(self):
        A = time.time()
        ticker_list = []
        page = 1
        etf = self.etf_etn_checker(category='etf')
        etn = self.etf_etn_checker(category='etn')
        exists = self.exist_code()
        while 1:
            req = self.request_get(self.ticker_url.format('P', page), self.user_agent)
            soup = self.html_parser(req)
            table = self.soup_findall(soup, 'tr', {'onmouseout':'highlight(this,false)'})
            length = len(table)
            if length == 0:
                page = 1
                while 1:
                    req = self.request_get(self.ticker_url.format('Q', page), self.user_agent)
                    soup = self.html_parser(req)
                    table = self.soup_findall(soup,'tr', {'onmouseout':'highlight(this,false)'})
                    if len(table) == 0:
                        # data saves here
                        print(len(ticker_list))
                        Ticker.objects.bulk_create(ticker_list)
                        success = True
                        B = time.time()
                        print(B - A)
                        return success, "Data request complete", B - A
                    for i in range(len(table)):
                        code = table[i].find('a').attrs['href'][-6:]
                        if code in exists:
                            continue
                        else:
                            name = table[i].text.split("\n")[2]
                            name = re.sub('[-=.#/?:$};,]', '', name)
                            market_type = self.market_dic['Q']
                            ticker_inst = Ticker(name=name,
                                                 code=code,
                                                 market_type=market_type)
                            if ticker_inst not in ticker_list:
                                ticker_list.append(ticker_inst)
                            else:
                                pass
                    page = page + 1
            for i in range(len(table)):
                code = table[i].find('a').attrs['href'][-6:]
                if code in exists:
                    continue
                else:
                    name = table[i].text.split("\n")[2]
                    name = re.sub('[-=.#/?:$};,]', '', name)
                    if code in etf:
                        market_type = self.market_dic['E']
                    elif code in etn:
                        market_type = self.market_dic['N']
                    else:
                        market_type = self.market_dic['P']
                    ticker_inst = Ticker(name=name,
                                         code=code,
                                         market_type=market_type)
                    if ticker_inst not in ticker_list:
                        ticker_list.append(ticker_inst)
                    else:
                        pass
            page = page + 1
