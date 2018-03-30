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
    KospiNet,
    KosdaqNet,
    ETFNet,
    )



class Scrape_WebData(object):
    '''
    - description: scrape KOSPI & KOSDAQ stock data from web page
    - ticker(daum), OHLCV(naver), Info(naver)
    '''
    def scrape_ticker(self):
        A=time.time()
        ticker_list = []
        page = 1
        exists = Ticker.objects.all().exists()
        if exists:
            print('Tickers already updated for {}'.format(date))
        while not exists:
            url = 'http://finance.daum.net/quote/volume.daum?stype=P&page={}'.format(str(page))
            market_dic = {'P':'KOSPI', 'Q':'KOSDAQ', 'E':'ETF'}
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
            length = len(table)
            etf = pd.read_csv('../etf_list.csv', header=None)
            etf = etf[0].tolist()
            etf = [str(e).zfill(6) for e in etf]
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
                        success = True
                        B = time.time()
                        return success, "Data request complete", B-A
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
                if code in etf:
                    market_type = market_dic['E']
                else:
                    market_type = market_dic['P']
                ticker_inst = Ticker(name=name,
                                     code=code,
                                     market_type=market_type,)
                ticker_list.append(ticker_inst)
            page = page + 1


    def scrape_ohlcv(self):
        upd_num = 0
        recent_update_date = self.ticker.kd_ohlcv.last().date
        today_date = datetime.now().strftime('%Y%m%d')
        market_ohlcv = {'KOSPI':KospiOHLCV, 'KOSPDAQ':KosdaqOHLCV, 'ETF':KospiOHLCV}
        for market in ['KOSPI', 'KOSDAQ', 'ETF']:
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

    def scrape_daily_ohlcv(self):
        A = time.time()
        success = False
        data_list = []
        date_time = datetime.now().strftime('%Y%m%d')
        market_ohlcv = {'KOSPI':KospiOHLCV, 'KOSDAQ':KosdaqOHLCV, 'ETF': KospiOHLCV}
        for market in ['KOSPI', 'KOSDAQ', 'ETF']:
            tickers = Ticker.objects.filter(market_type=market).order_by('id')
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
            B = time.time()
            return success, "Data request complete", B-A

    def scrape_info(self, ticker):
        A = time.time()
        success = False
        data_list=[]
        date = datetime.now().strftime('%Y%m%d')
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        for i in range(len(ticker)) :
            url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cn=&cmp_cd='+ ticker[i].code
            code = ticker[i]
            r = requests.get(url, headers=user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            tmp = soup.findAll('td',{'class':'cmp-table-cell td0101'})
            if len(tmp) != 0:
                tmp = tmp[0].findAll('dt',{'class':'line-left'})[1].text.replace(' ','').split(':')
                market_type = tmp[0]
                industry = tmp[1]
                url = 'http://finance.naver.com/item/coinfo.nhn?code='+ ticker[i].code
                r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
                soup = BeautifulSoup(r.text, 'html.parser')
                todayinfo = soup.findAll('dl',{'class':'blind'})
                stockinfo = pd.read_html(url, thousands='')
                price = todayinfo[0].findAll('dd')[3].text.split(' ')[1].replace(',','')
                if len(stockinfo[1]) == 5:
                    face_val = stockinfo[1].iloc[3,1].replace(' ','').replace(',','').replace('원','').split('l')[0]
                    stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                    foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                    foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                    foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                    #per, eps
                    per_td = soup.findAll('table',{'class':'per_table'})
                    td = per_td[0].findAll('em')
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
                    per_td = soup.findAll('table',{'class':'per_table'})
                    td = per_td[0].findAll('em')
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
                url = 'http://finance.naver.com/item/coinfo.nhn?code='+ ticker[i].code
                r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
                soup = BeautifulSoup(r.text, 'html.parser')
                market_type = "KOSPI"
                industry = "ETF"
                soup = BeautifulSoup(r.text, 'html.parser')
                todayinfo = soup.findAll('dl',{'class':'blind'})
                price = todayinfo[0].findAll('dd')[3].text.split(' ')[1].replace(',','')
                stockinfo = pd.read_html(url, thousands='')
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

    def scrape_shinhan_buysell(self):
        A = time.time()
        today = datetime.today().strftime('%Y%m%d')
        market_net = {'KOSPI':KospiNet, 'KOSDAQ':KosdaqNet, 'ETF':ETFNet}
        filename = {'KOSPI':'kospi', 'KOSDAQ':'kosdaq', 'ETF':'etf'}
        for market in ['KOSPI','KOSDAQ','ETF']:
            success=False
            csv_list = []
            data_list = []
            print(os.getcwd())
            f = open('./gobble/backup_csv/{}/buysell/{}-net.csv'.format(filename[market],today), 'a', encoding='utf-8', newline='')
            fieldnames = ['date','individual','foreign_retail','institution','finance',
                          'etc_finance','trust','bank', 'insurance','pension','etc_corporate']
            hd = csv.DictWriter(f,fieldnames=fieldnames)
            hd.writeheader()
            f.close()
            #     print(os.getcwd())
            #     f = open('.gobble/backup_csv/{}/buysell/{}-net.csv'.format(filename[market],today), 'w', encoding='utf-8', newline='')
            #     fieldnames = ['date','individual','foreign_retail','institution','finance',
            #                   'etc_finance','trust','bank', 'insurance','pension','etc_corporate']
            #     f.close()
            tickers = Ticker.objects.filter(market_type=market)
            for ticker in tickers:
                url = 'http://open.shinhaninvest.com/goodicyber/mk/1206.jsp?code=' + ticker.code
                user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
                r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.findAll('table', {'class':'content1'})
                tr = table[0].findAll('tr')
                tr[3].text.split('\n')
                code = ticker
                for i in range(2,len(tr)):
                    ticker_inst = {}
                    t = tr[i].text.split('\n')
                    date = t[1].replace('/','')
                    if date == today:
                        break
                    individual = int(t[2].replace(',',''))
                    foreign_retail = int(t[3].replace(',',''))
                    institution = int(t[4].replace(',',''))
                    finance = int(t[5].replace(',',''))
                    trust = int(t[6].replace(',',''))
                    bank = t[7].replace(',','')
                    etc_finance = t[8].replace(',','')
                    insurance = t[9].replace(',','')
                    pension = t[10].replace(',','')
                    etc_corporate = t[11].replace(',','')
                    ticker_inst = market_net[market](date=date,
                                                     code=code,
                                                     individual=individual,
                                                     foreign_retail=foreign_retail,
                                                     institution=institution,
                                                     finance=finance,
                                                     trust=trust,
                                                     bank=bank,
                                                     etc_finance=etc_finance,
                                                     insurance=insurance,
                                                     pension=pension,
                                                     etc_corporate=etc_corporate,)
                    data_list.append(ticker_inst)
                    row_list = [date,individual,foreign_retail,institution,finance,etc_finance,trust,bank,
                                insurance,pension,etc_corporate]
                    csv_list.append(row_list)
                time.sleep(randint(0,1)*10)
            market_net[market].objects.bulk_create(data_list)
            f = open('./gobble/backup_csv/{}/buysell/{}-net.csv'.format(filename[market],today), 'a', encoding='utf-8', newline='')
            wr = csv.writer(f)
            wr.writerows(csv_list)
            f.close()
            B=time.time()
            success = True
            print(success, "{} Data request complete".format(market), B-A)
        C=time.time()
        return success, "Data request complete", C-A
