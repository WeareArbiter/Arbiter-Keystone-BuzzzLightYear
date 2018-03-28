from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from bs4 import BeautifulSoup
from datetime import datetime
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


class Scrape_WebData(object):
    '''
    - description: scrape KOSPI & KOSDAQ stock data from web page
    - ticker(daum), OHLCV(naver), Info(naver)
    '''
    def scrape_ticker(self):
        ticker_list = []
        page = 1
        exists = Ticker.objects.all().exists()
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
                        name = re.sub('[-=.#/?:$};,]', '', name)
                        market_type = market_dic['Q']
                        ticker_inst = Ticker(name=name,
                                             code=code,
                                             market_type=market_type,)
                        ticker_list.append(ticker_inst)
                    page = page + 1
            for i in range(len(table)):
                code = table[i].find('a').attrs['href'][-6:]
                name = table[i].text.split("\n")[2]
                name = re.sub('[-=.#/?:$};,]', '', name)
                market_type = market_dic['P']
                ticker_inst = Ticker(name=name,
                                     code=code,
                                     market_type=market_type,)
                ticker_list.append(ticker_inst)
            page = page + 1

    def scrape_ohlcv(self, market):
        upd_num = 0
        recent_update_date = KosdaqOHLCV.objects.filter(code='900100').order_by('date').last().date
        today_date = datetime.now().strftime('%Y%m%d')
        market_ohlcv = {'KOSPI':KospiOHLCV, 'KOSPDAQ':KosdaqOHLCV}
        if recent_update_date != today_date:
            tickers = Ticker.objects.filter(market_type=market).filter(state=True)
            for ticker in tickers:
                code = ticker
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

    def scrape_daily_ohlcv(self, market):
        success = False
        data_list = []
        date_time = datetime.now().strftime('%Y%m%d')
        tickers = Ticker.objects.filter(market_type=market).order_by('id')
        market_ohlcv = {'KOSPI':KospiOHLCV, 'KOSDAQ':KosdaqOHLCV}
        for i in range(len(tickers)):
            url = 'http://finance.naver.com/item/sise.nhn?code=' + tickers[i].code
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers=user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            name = soup.findAll('dt')[1].text
            df = pd.read_html(url, thousands='')
            name = name
            code = tickers[i]
            date = date_time
            open_price = df[1].iloc[3,3].replace(",","")  #시가
            close_price = df[1].iloc[0,1].replace(",","") #현재가, 종가
            high_price = df[1].iloc[4,3].replace(",","")  #고가
            low_price = df[1].iloc[5,3].replace(",","") #저가
            volume = df[1].iloc[3,1].replace(",","")
            ohlcv_inst = market_ohlcv[market](date=date,
                                              code=code,
                                              open_price=open_price,
                                              close_price=close_price,
                                              high_price=high_price,
                                              low_price=low_price,
                                              volume=volume)
            data_list.append(ohlcv_inst)
        market_ohlcv[market].objects.bulk_create(data_list)
        success = True
        return success, "Data request complete"
