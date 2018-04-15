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

from stockapi.models import Info
from gobble.Crawler import Crawler


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

from stockapi.models import Ticker, Info
from gobble.Crawler import Crawler

class InfoCrawler(Crawler):

    def __init__(self):
        super().__init__()

    def scrape_info(self, tickers):
        A = time.time()
        success = False
        data_list=[]
        for ticker in tickers :
            code = ticker[i]
            industry_url = self.wisefn_url.format(ticker.code)
            req = self.request_get(industry_url, self.user_agent)
            soup = self.html_parser(req)
            tmp = self.soup_findall(soup, 'td', {'class':'cmp-table-cell td0101'})
            if ticker.market_type not in ['ETF', 'ETN']:
                tmp = self.soup_findall(tmp[0], 'dt', {'class':'line-left'})[1].text.replace(' ','').split(':')
                market_type = ticker.market_type
                industry = tmp[1]
                info_url = self.info_url.format(ticker.code)
                req1 = self.request_get(info_url, self.user_agent)
                soup1 = self.soup_findall(req1)
                todayinfo = self.soup_findall(soup1, 'dl', {'class':'blind'})
                stockinfo = pd.read_html(info_url, thousands='')
                price = self.soup_findall(todayinfo[0], 'dd').text.split(' ')[1].replace(',','')
                if len(stockinfo[1]) == 5:
                    face_val = stockinfo[1].iloc[3,1].replace(' ','').replace(',','').replace('원','').split('l')[0]
                    stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                    foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                    foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                    foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                    #per, eps
                    per_td = self.soup_findall(soup1,'table',{'class':'per_table'})
                    td =  self.soup_findall(per_td[0],'em')
                    per_table = []
                    for t in td:
                        a = t.text
                        per_table.append(a)
                    per = 0 if per_table[0] == "N/A" else per_table[0].replace(',','')
                    eps = 0 if per_table[1] == "N/A" else per_table[1].replace(',','')
                    yield_ret = 0 if per_table[8] == "N/A" else per_table[8]
                    bps = 0 if per_table[7] == "N/A" else per_table[7].replace(',','')
                    pbr = 0 if bps == 0 else round(int(price)/int(bps),2)
                    print(code,stockinfo[5].iloc[0,1])
                    try:
                        math.isnan(float(stockinfo[5].iloc[0,1].replace('배','').replace(',','')))
                        industry_per = float(stockinfo[5].iloc[0,1].replace('배','').replace(',',''))
                    except AttributeError:
                        industry_per = 0
                    print(code,industry_per)
                    market_cap = int(price)*int(stock_nums) #시가총액
                elif len(stockinfo[1]) == 4:
                    face_val = 0
                    stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                    foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                    foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                    foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                    #per, eps
                    per_td = self.soup_findall(soup1,'table',{'class':'per_table'})
                    td =  self.soup_findall(per_td[0],'em')
                    per_table = []
                    for t in td:
                        a = t.text
                        per_table.append(a)
                    per = per_table[0]
                    eps = per_table[1].replace(',','')
                    yield_ret = 0 if per_table[8] == "N/A" else per_table[8]
                    bps = 0 if per_table[7] == "N/A" else per_table[7].replace(',','')
                    pbr = 0 if bps == 0 else round(int(price)/int(bps),2)
                    try:
                        math.isnan(float(stockinfo[5].iloc[0,1].replace('배','').replace(',','')))
                        industry_per = float(stockinfo[5].iloc[0,1].replace('배','').replace(',',''))
                    except AttributeError:
                        industry_per = 0
                    print(code,industry_per)
                    market_cap = int(price)*int(stock_nums)
                else:
                    face_val = 0
                    stock_nums = stockinfo[1].iloc[1,1].replace(',','')#상장주식수
                    foreign_limit = 0
                    foreign_possession = 0
                    foreign_ratio = 0
                    per = 0
                    eps = 0
                    pbr = 0
                    bps = 0
                    industry_per = 0
                    yield_ret = 0
                    market_cap = int(price)*int(stock_nums)
                tmp_json = Info(date=date,
                                code=code,
                                market_type=market_type,
                                industry=industry,
                                price=price,
                                face_val=face_val,
                                stock_nums=stock_nums,
                                market_cap=market_cap,
                                foreign_limit=foreign_limit,
                                foreign_possession=foreign_possession,
                                foreign_ratio=foreign_ratio,
                                per=per,
                                eps=eps,
                                bps=bps,
                                pbr=pbr,
                                industry_per=industry_per,
                                yield_ret=yield_ret)
                data_list.append(tmp_json)
            else:
                info_url = self.info_url.format(ticker.code)
                req1 = self.request_get(info_url, self.user_agent)
                soup1 = self.soup_findall(req1)
                todayinfo = self.soup_findall(soup1, 'dl', {'class':'blind'})
                stockinfo = pd.read_html(info_url, thousands='')
                price = self.soup_findall(todayinfo[0], 'dd').text.split(' ')[1].replace(',','')
                market_type = 'KOSPI'
                industry = ticker.market_type
                stock_nums = stockinfo[1].iloc[1,1].replace(',','')#상장주식수
                face_val = 0
                market_cap = int(price)*int(stock_nums) #시가총액
                foreign_limit = 0
                foreign_possession = 0
                foreign_ratio = 0
                per = 0
                eps = 0
                pbr = 0
                bps = 0
                industry_per = 0
                yield_ret = 0
                tmp_json = Info(date=date,
                                code=code,
                                market_type=market_type,
                                industry=industry,
                                price=price,
                                face_val=face_val,
                                stock_nums=stock_nums,
                                market_cap=market_cap,
                                foreign_limit=foreign_limit,
                                foreign_possession=foreign_possession,
                                foreign_ratio=foreign_ratio,
                                per=per,
                                eps=eps,
                                bps=bps,
                                pbr=pbr,
                                industry_per=industry_per,
                                yield_ret=yield_ret)
                data_list.append(tmp_json)
        success = True
        Info.objects.bulk_create(data_list)
        B = time.time()
        return success, "Data request complete", B-A
