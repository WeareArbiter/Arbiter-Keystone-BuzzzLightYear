from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from stockapi.models import (
    Benchmark,
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    RecentKospiOHLCV,
    RecentKosdaqOHLCV,
    Info,
    Specs,
    Financial,
    FinancialRatio,
    QuarterFinancial,
    KospiBuy,
    KosdaqBuy,
    KospiSell,
    KosdaqSell,
    KospiNet,
    KosdaqNet,
    KospiShort,
    KosdaqShort,
)

User = get_user_model()


class StockapiTestCase(TestCase):
    '''
    Stockapi DB testing module
    '''

    def setUp(self):
        print('Starting stockapi test')

        # create Ticker data first, before saving other data
        ticker, created = Ticker.objects.get_or_create(code='005930',
                                                       name='삼성전자',
                                                       market_type='KOSPI',
                                                       state=1)
        # ticker variable for ForeignKey
        self.ticker = ticker

        # test assertions
        self.assertTrue(created, msg='failed to save Ticker data')
        self.assertEqual(Ticker.objects.all().count(), 1, msg='Ticker data not created properly')


    def test_Ticker_primary_key_is_code(self):
        ticker_saved_count = Ticker.objects.count()
        self.assertEqual(ticker_saved_count, 1, msg='Ticker saved more than one instance')

        ticker_pk = self.ticker.pk
        self.assertEqual(ticker_pk, '005930', msg='Ticker primary key not code value of stock')


    def test_BM_save(self):
        # BM does not need ForeignKey Ticker data
        # simple testing whether save works or not
        bm, created = Benchmark.objects.get_or_create(date='20180101',
                                                      name='KOSPI',
                                                      index=2500,
                                                      volume=1000000,
                                                      individual=5000,
                                                      foreigner=5000,
                                                      institution=5000)
        self.assertTrue(created, msg='failed to save BM data')
        self.assertEqual(Benchmark.objects.count(), 1, msg='Benchmark data not created properly')


    def test_OHLCV_save(self):
        # test all Kospi, Kosdaq model cases
        # 4 models in total: KospiOHLCV, KosdaqOHLCV, RecentKospiOHLCV, RecentKosdaqOHLCV
        kospi_ohlcv, created = KospiOHLCV.objects.get_or_create(date='20180101',
                                                                code=self.ticker,
                                                                open_price=1000,
                                                                high_price=1000,
                                                                low_price=1000,
                                                                close_price=1000,
                                                                volume=1000000)

        kosdaq_ohlcv, created = KosdaqOHLCV.objects.get_or_create(date='20180101',
                                                                  code=self.ticker,
                                                                  open_price=1000,
                                                                  high_price=1000,
                                                                  low_price=1000,
                                                                  close_price=1000,
                                                                  volume=1000000)

        r_kospi_ohlcv, created = RecentKospiOHLCV.objects.get_or_create(date='20180101',
                                                                        code=self.ticker,
                                                                        open_price=1000,
                                                                        high_price=1000,
                                                                        low_price=1000,
                                                                        close_price=1000,
                                                                        volume=1000000)

        r_kosdaq_ohlcv, created = RecentKosdaqOHLCV.objects.get_or_create(date='20180101',
                                                                          code=self.ticker,
                                                                          open_price=1000,
                                                                          high_price=1000,
                                                                          low_price=1000,
                                                                          close_price=1000,
                                                                          volume=1000000)

        # check if ForeignKey works properly
        kospi_close_price = self.ticker.kp_ohlcv.first().close_price
        kosdaq_close_price = self.ticker.kd_ohlcv.first().close_price
        r_kospi_close_price = self.ticker.r_kp_ohlcv.first().close_price
        r_kosdaq_close_price = self.ticker.r_kd_ohlcv.first().close_price
        self.assertEqual(kospi_close_price, 1000, msg='kospi_close_price OHLCV data not created properly')
        self.assertEqual(kosdaq_close_price, 1000, msg='kosdaq_close_price OHLCV data not created properly')
        self.assertEqual(r_kospi_close_price, 1000, msg='r_kospi_close_price OHLCV data not created properly')
        self.assertEqual(r_kosdaq_close_price, 1000, msg='r_kosdaq_close_price OHLCV data not created properly')


    def test_OHLCV_filtering(self):
        # create OHLCV data first
        kospi_ohlcv, created = KospiOHLCV.objects.get_or_create(date='20180101',
                                                                code=self.ticker,
                                                                open_price=1000,
                                                                high_price=1000,
                                                                low_price=1000,
                                                                close_price=1000,
                                                                volume=1000000)

        # filter with code value from Ticker instance
        code_val = self.ticker.code
        self.assertEqual(code_val, '005930', msg='Code value of Ticker instance not correct')

        queryset = KospiOHLCV.objects.filter(code=code_val)
        self.assertTrue(queryset.exists, msg='Filtering with Ticker foreignkey value not available')


    def test_Info_save(self):
        info_inst, created = Info.objects.get_or_create(date='20180101',
                                                        code=self.ticker,
                                                        size_type='L',
                                                        style_type='V',
                                                        market_type='KOSPI',
                                                        face_val=100,
                                                        stock_nums=1000000,
                                                        price=100,
                                                        market_cap=100,
                                                        market_cap_rank=100,
                                                        industry='기타산업',
                                                        foreign_limit=100,
                                                        foreign_possession=100,
                                                        foreign_ratio=0.5,
                                                        per=1.0,
                                                        eps=100.0,
                                                        pbr=2.0,
                                                        bps=100.0,
                                                        industry_per=1.0,
                                                        yield_ret=0.1)
        self.assertTrue(created, msg='failed to save Info data')
        self.assertEqual(Info.objects.count(), 1, msg='Info data not created properly')

    def test_Specs_save(self):
        pass
