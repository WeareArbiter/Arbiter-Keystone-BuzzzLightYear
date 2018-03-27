from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from bs4 import BeautifulSoup
import math
import pandas as pd
import requests
import re

from stockapi.models import (
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    RecentKospiOHLCV,
    RecentKosdaqOHLCV,
    Info,
    )

from defacto.models import DefactoTicker


class Scrape_WebData(self):
    '''
    - description: scrape KOSPI & KOSDAQ stock data from web page
    - ticker(daum), OHLCV(naver), Info(naver)
    '''
    def scrape_ticker(self):
        ticker_list = []
        defact_list = []
        page = 1
        date = datetime.now().strftime('%Y%m%d')
        exists = Ticker.objects.filter(date=date).exists()
        if exists:
            print('Tickers already updated for {}'.format(date))
        while not exists:
            url = 'http://finance.daum.net/quote/volume.daum?stype=P&page={}'.format(str(page))
            market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
            length = len(table)
            if length==0:
                page=1
                while 1:
                    url = 'http://finance.daum.net/quote/volume.daum?stype=Q&page={}'.format(str(page))
                    r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
                    soup = BeautifulSoup(r.text, 'html.parser')
                    table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
                    if len(table)==0:
                        # data saves here
                        Ticker.objects.bulk_create(ticker_list)
                        DefactoTicker.objects.bulk_create(defact_list)
                        success = True
                        return success
                    for i in range(len(table)):
                        code = table[i].find('a').attrs['href'][-6:]
                        name = table[i].text.split("\n")[2]
                        market_type = market_dic['Q']
                        ticker_inst = Ticker(date=date,
                                             name=name,
                                             code=code,
                                             market_type=market_type)
                        ticker_inst2 = DefactoTicker(date=date,
                                             name=name,
                                             code=code,
                                             market_type=market_type)
                        ticker_list.append(ticker_inst)
                        defact_list.append(ticker_inst2)
                    page = page + 1
            for i in range(len(table)):
                code = table[i].find('a').attrs['href'][-6:]
                name = table[i].text.split("\n")[2]
                market_type = market_dic['P']
                ticker_inst = Ticker(date=date,
                                     name=name,
                                     code=code,
                                     market_type=market_type)
                ticker_inst2 = DefactoTicker(date=date,
                                     name=name,
                                     code=code,
                                     market_type=market_type)
                ticker_list.append(ticker_inst)
                defact_list.append(ticker_inst2)
            page = page + 1

    def scrape_ohlcv(self, market):
        upd_num = 0
        recent_update_date = OHLCV.objects.filter(code='900100').order_by('date').last().date
        today_date = datetime.datetime.now().strftime('%Y%m%d')
        market_ohlcv = {'kospi':KospiOHLCV, 'kosdaq':KosdaqOHLCV}
        if recent_update_date != today_date:
            tickers = Ticker.objects.filter(market_type=market)
            for ticker in tickers:
                code = ticker.id
                if market_ohlcv[market].objects.filter(code=code).filter(date=today_date).exists():
                    print('{} {} already updated. Skipping...'.format(str(upd_num), code))
                    upd_num += 1
                    continue
                else:
                    url = "http://finance.naver.com/item/sise_day.nhn?code=" + code
                    print('{} {}'.format(str(upd_num), url))
                    df = pd.read_html(url, thousands='')
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
                                data = market_ohlcv[market](code=code,
                                                            date=date,
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
