import math, time
from datetime import datetime
import numpy as np
from numpy import *
import pandas as pd
import scipy.optimize

from stockapi.models import (
    Benchmark,
    Info,
    Ticker,
    OHLCV
    )


class PortfolioAlgorithm:

    def __init__(self, ratio_dict, filter_date=False):
        self.ratio_dict = ratio_dict
        recent_update_date = Benchmark.objects.filter(name='KOSPI').order_by('-date').first().date
        year = recent_update_date[:4]
        month = recent_update_date[4:6]
        if not filter_date:
            last_year = str(int(year) - 5)
            last_month = int(month) - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date
        else:
            self.filter_date = filter_date
        self.ohlcv_df = pd.DataFrame()
        self.settings = {
            'ticker_list': list(),
            'ohlcv_list': list()
        }
        self._start_df_setup() # fill in ticker_list and ohlcv_list
        self._retrieve_weights()
        self._create_ohlcv_df()
        self._calc_port_returns()

    def _start_df_setup(self):
        # setting ticker_list
        self.settings['ticker_list'] = [ticker for ticker in self.ratio_dict.keys() if ticker != 'cash']
        ticker_list = self.settings['ticker_list']
        # setting ohlcv_list
        init_qs = OHLCV.objects.filter(code__in=ticker_list)
        filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        ohlcv_qs = filtered_qs.values_list('code', 'date', 'close_price')
        ohlcv_list = []
        for ticker in ticker_list:
            ticker_ohlcv = [{'date': data[1], 'close_price': data[2]} for data in ohlcv_qs if data[0] == ticker]
            ohlcv_list.append(ticker_ohlcv)
        self.settings['ohlcv_list'] = ohlcv_list

    def _retrieve_weights(self):
        S = list()
        W = list()
        for key, val in self.ratio_dict.items():
            if key != 'cash':
                S.append(key)
                W.append(val['ratio'])
        W = pd.Series(W, index=S)
        self.W = W

    def _create_ohlcv_df(self):
        ticker_count = len(self.settings['ticker_list'])
        if ticker_count == 0:
            pass
        elif ticker_count == 1:
            ticker = self.settings['ticker_list'][0]
            ohlcv = self.settings['ohlcv_list'][0]
            self.ohlcv_df = self._create_df(ticker, ohlcv)
        else:
            for i in range(ticker_count):
                ticker = self.settings['ticker_list'][i]
                ohlcv = self.settings['ohlcv_list'][i]
                if i == 0:
                    df = self._create_df(ticker, ohlcv)
                else:
                    temp_df = self._create_df(ticker, ohlcv)
                    df = pd.concat([df, temp_df], axis=1)
            df.index = pd.to_datetime(df.index)
            self.ohlcv_df = df

    def _create_df(self, ticker, ohlcv):
        df = pd.DataFrame(ohlcv)
        df.set_index('date', inplace=True)
        df.rename(columns={'close_price': ticker}, inplace=True)
        return df

    def _calc_port_returns(self, period='M'):
        self.ohlcv_df.index = pd.to_datetime(self.ohlcv_df.index)
        R = self.ohlcv_df.resample(period).last().pct_change()
        R.dropna(how='all', inplace=True)
        self.R = R

    def portfolio_info(self):
        BM_wr, BM_r, BM_v, BM_yc = self._bm_specs()
        wr, r, v, yc = self._backtest_port(self.W, self.R)
        sr = self._sharpe_ratio(r, BM_r, v)
        yield_r = yc.ix[len(yc)-1] - 1
        bt = pd.concat([yc, BM_yc], axis=1)
        bt.columns = ['Portfolio', 'Benchmark']
        return r, v, sr, yield_r, bt

    def _bm_specs(self, period='M'):
        from stockapi.models import Benchmark
        BM_qs = Benchmark.objects.filter(name='KOSPI').distinct('date')
        BM_data = list(BM_qs.exclude(date__lte=self.filter_date).values('date', 'index'))
        BM = pd.DataFrame(BM_data)
        BM.set_index('date', inplace=True)
        BM.index = pd.to_datetime(BM.index)
        BM.rename(columns={'index': 'Benchmark'}, inplace=True)
        BM_R = Benchmark.resample(period).last().pct_change()
        BM_R.dropna(how='all', inplace=True)
        W = pd.Series([1], index=['Benchmark'])
        return self._backtest_port(W, BM_R)

    def _backtest_port(self, W=None, BM=None):
        if type(W) == type(None) and type(BM) == type(None):
            W_R = self.W * self.R
        else:
            W_R = W*BM
        WR = W_R.sum(axis=1)
        port_ret = WR.mean()
        port_var = WR.std()
        yield_curve = (WR + 1).cumprod()
        return WR, port_ret, port_var, yield_curve

    def _sharpe_ratio(self, r, bm_r, v):
        return (r - bm_r)/v

    def change_bt_format(self, bt):
        new_data = dict()
        for column in bt.columns:
            ret_data = list()
            dates = bt.index.astype(np.int64)//1000000 # pandas timestamp returns in microseconds, divide by million
            for i in range(len(bt)):
                data = bt.ix[i]
                date = dates[i]
                ret_data.append([date, float(format(round(data[column], 4), '.4f'))])
            new_data[column] = ret_data
        return new_data
