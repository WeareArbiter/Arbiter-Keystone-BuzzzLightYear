import os
from gobble.Kiwoom import Kiwoom
from gobble.processtracker import ProcessTracker, timeit

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime
import pandas as pd
import os, sys, glob
import time


start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbiter.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.db.models import Q
from stockapi.models import (
    Ticker,
    KospiBuy,
    KosdaqBuy,
    ETFBuy,
    KospiShort,
    KosdaqShort)

TR_REQ_TIME_INTERVAL = 4.8

week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
tmp_today = datetime.today()
w = tmp_today.weekday()
if week[w] == 'sat':
    TODAY = tmp_today - timedelta(days=1)
    TODAY = TODAY.strftime('%Y%m%d')
elif week[w] == 'sun':
    TODAY = tmp_today - timedelta(days=2)
    TODAY = TODAY.strftime('%Y%m%d')
else:
    TODAY = tmp_today.strftime('%Y%m%d')
print(TODAY)

buy_dict = {'KOSPI':KospiBuy , 'KOSDAQ':KosdaqBuy, 'ETF':ETFBuy}
short_dict = {'KOSPI':KospiShort , 'KOSDAQ':KosdaqShort}

class Gobble(ProcessTracker):
    @timeit
    def __init__(self):
        super().__init__() # initialize ProcessTracker
        self.starting()
        self.app = QApplication(["kiwoom.py"])
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

    def set_tasks(self, market_type=None):
        if market_type == None:
            self.tickers = Ticker.objects.all()
            # code = [code[0].zfill(6) for code in tickers.values_list('code')]
        elif market_type == 'kospi':
            self.tickers = Ticker.objects.filter(Q(market_type='KOSPI')|Q(market_type='ETN'))
            # code = [code[0].zfill(6) for code in tickers.values_list('code')]
        elif market_type == 'kosdaq':
            self.tickers = Ticker.objects.filter(market_type='KOSDAQ')
            # code = [code[0].zfill(6) for code in tickers.values_list('code')]
        elif market_type == 'etf':
            self.tickers = Ticker.objects.filter(market_type='ETF')
            # code = [code[0].zfill(6) for code in tickers.values_list('code')]
        elif market_type == 'kospi-etf':
            self.tickers = Ticker.objects.filter(Q(market_type='KOSPI')|Q(market_type='ETF'))
            # code = [code[0].zfill(6) for code in tickers.values_list('code')]

    def _get_total_stock_num(self):
        tickers_len = len(list(self.tickers))
        return tickers_len

    def _buysell_skip_codes(self):
        global TODAY
        kp_tickers = KospiBuy.objects.filter(date=TODAY).values_list('code')
        kd_tickers = KosdaqBuy.objects.filter(date=TODAY).values_list('code')
        etf_tickers = ETFBuy.objects.filter(date=TODAY).values_list('code')
        kospi_list = [code[0].zfill(6) for code in kp_tickers]
        kosdaq_list = [code[0].zfill(6) for code in kd_tickers]
        etf_list = [code[0].zfill(6) for code in etf_tickers]
        return kospi_list + kosdaq_list + etf_list

    def req_buysell(self, start, market=None):
        done_list = self._buysell_skip_codes()
        total_stock_num = self._get_total_stock_num() - len(done_list)
        code_looped = 0
        total_time = 0
        market_type = market

        for ticker in self.tickers:
            if ticker.code in done_list:
                continue
            ts = time.time()
            name = ticker.name
            code = ticker.code
            try:
                self._initialize_buysell_data(ticker, start)
            except:
                print(code + ", " + name + " buysell save skipped due to error")
            te = time.time()
            time_took = te - ts
            total_time += time_took
            code_looped += 1
            avg_time_took = total_time/code_looped
            stocks_left = total_stock_num - code_looped
            time_left = avg_time_took * stocks_left
            print(str(stocks_left) + " stocks left to save")
            print(str(time_left) + " seconds left to finish whole request")
            print("---------------------------------------------------")

    def _initialize_buysell_data(self, ticker, start):
        global TR_REQ_TIME_INTERVAL
        global market_dict

        kiwoom = self.kiwoom
        ticker_code = ticker.code
        name = ticker.name
        time.sleep(TR_REQ_TIME_INTERVAL)
        print(ticker_code + ": " + name + " buysell data initializing")
        kiwoom.prepare_data()
        print("update data dict created")
        market = ticker.market_type

        # opt10059 TR 요청
        kiwoom.set_input_value("일자", time.strftime('%Y%m%d'))
        kiwoom.set_input_value("종목코드", ticker_code)
        kiwoom.set_input_value("금액수량구분", 2)
        kiwoom.set_input_value("매매구분", 1)
        kiwoom.set_input_value("단위구분", 1)
        kiwoom.comm_rq_data("opt10059_req", "opt10059", 0, "0101")
        time.sleep(TR_REQ_TIME_INTERVAL)

        print("first request sent in successfully")
        print("BUY data saved, ready for DB")
        buy_list = []
        tmp_buy = kiwoom.data[kiwoom.data['date']>=int(start)]
        for i in range(len(tmp_buy)):
            row = tmp_buy.ix[i]
            date = row['date']
            individual = row['individual']
            foreign_retail = row['foreign_retail']
            institution = row['institution']
            financial = row['financial']
            insurance = row['insurance']
            trust = row['trust']
            etc_finance = row['etc_finance']
            bank = row['bank']
            pension = row['pension']
            private = row['private']
            nation = row['nation']
            etc_corporate = row['etc_corporate']
            buy_inst = buy_dict[market](date = date,
                                        code = ticker,
                                        individual = individual,
                                        foreign_retail = foreign_retail,
                                        institution = institution,
                                        financial = financial,
                                        insurance = insurance,
                                        trust = trust,
                                        etc_finance = etc_finance,
                                        bank = bank,
                                        pension = pension,
                                        private = private,
                                        nation = nation,
                                        etc_corporate = etc_corporate,)
            buy_list.append(buy_inst)
        market_dict[market].objects.bulk_create(buy_list)
        print(ticker_code + ": " + name + " buy data successfully saved")


    def req_short(self, start):
        done_list = self._short_skip_codes()
        total_stock_num = self._get_total_stock_num() - len(done_list)
        code_looped = 0
        total_time = 0

        for ticker in self.tickers:
            if ticker.code in done_list:
                continue
            ts = time.time()
            name = ticker.name
            code = ticker.code
            try:
                self._initialize_short_data(code , start)
            except:
                print(code + ", " + name + " short save skipped due to error")
            te = time.time()
            time_took = te - ts
            total_time += time_took
            code_looped += 1
            avg_time_took = total_time/code_looped
            stocks_left = total_stock_num - code_looped
            time_left = avg_time_took * stocks_left
            print(str(stocks_left) + " stocks left to save")
            print(str(time_left) + " seconds left to finish whole request")
            print("---------------------------------------------------")


    def _initialize_short_data(self, code, start):
        global TR_REQ_TIME_INTERVAL

        kiwoom = self.kiwoom
        ticker_code = ticker.code
        name = ticker.name
        time.sleep(TR_REQ_TIME_INTERVAL)
        print(code + ": " + name + " short data initializing")
        kiwoom.prepare_data()
        print("update data dict created")

        # opt10014 TR 요청
        kiwoom.set_input_value("종목코드", ticker_code)
        kiwoom.set_input_value("시간구분 ", 0)
        kiwoom.set_input_value("시작일자", time.strftime('%Y%m%d'))
        kiwoom.set_input_value("종료일자", time.strftime('%Y%m%d'))
        kiwoom.comm_rq_data("opt10014_req", "opt10014", 0, "0101")
        time.sleep(TR_REQ_TIME_INTERVAL)
        print("first request sent in successfully")
        print("short data saved, ready for DB")
        length = kiwoom.data.shape[0]
        short_list = []
        tmp_short = kiwoom.data[kiwoom.data['date']>=int(start)]
        if len(tmp_short) == 0:
            pass
        else:
            for i in range(len(tmp_short)):
                row = tmp_short.ix[i]
                date = row['date']
                short = row['short']
                short_proportion = row['short_proportion']
                short_total_price = row['short_total_price']
                short_average_price = row['short_average_price']
                short_inst = short_dict[market](date=date,
                                                code=code,
                                                short=short,
                                                short_proportion=short_proportion,
                                                short_total_price=short_total_price,
                                                short_average_price=short_average_price,)
                short_list.append(short_inst)
            short_dict[market].bulk_create(short_list)
        print(code + ": " + name + " short data successfully saved")
