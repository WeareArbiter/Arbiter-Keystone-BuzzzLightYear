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
    ETFBuy,
    KospiSell,
    KosdaqSell,
    ETFSell,
    KospiNet,
    KosdaqNet,
    ETFNet,
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

    # def test_BM_save(self):
    #     # BM does not need ForeignKey Ticker data
    #     bm, created = Benchmark.objects.get_or_create(date='20180101',
    #                                                   name='KOSPI',
    #                                                   index=2500,
    #                                                   volume=1000000,
    #                                                   individual=5000,
    #                                                   foreigner=5000,
    #                                                   institution=5000)
    #     self.assertTrue(created, msg='failed to save BM data')
    #     self.assertEqual(Benchmark.objects.count(), 1, msg='Benchmark data not created properly')
    #
    # def test_OHLCV_save(self):
    #     # test all Kospi, Kosdaq model cases
    #     kospi_ohlcv, created = KospiOHLCV.objects.get_or_create(date='20180101',
    #                                                             code=self.ticker,
    #                                                             open_price=1000,
    #                                                             high_price=1000,
    #                                                             low_price=1000,
    #                                                             close_price=1000,
    #                                                             volume=1000000)
    #     self.assertTrue(created, msg='failed to save KOSPI OHLCV data')
    #     inst_name = kospi_ohlcv.code.name
    #     self.assertEqual(inst_name, '삼성전자', msg='KOSPI OHLCV data not created properly')
    #
    #     kosdaq_ohlcv, created = KosdaqOHLCV.objects.get_or_create(date='20180101',
    #                                                               code=self.ticker,
    #                                                               open_price=1000,
    #                                                               high_price=1000,
    #                                                               low_price=1000,
    #                                                               close_price=1000,
    #                                                               volume=1000000)
    #     self.assertTrue(created, msg='failed to save KOSDAQ OHLCV data')
    #     inst_name = kosdaq_ohlcv.code.name
    #     self.assertEqual(inst_name, '삼성전자', msg='KOSDAQ OHLCV data not created properly')
    #
    #     r_kospi_ohlcv, created = RecentKospiOHLCV.objects.get_or_create(date='20180101',
    #                                                                     code=self.ticker,
    #                                                                     open_price=1000,
    #                                                                     high_price=1000,
    #                                                                     low_price=1000,
    #                                                                     close_price=1000,
    #                                                                     volume=1000000)
    #     self.assertTrue(created, msg='failed to save Recent KOSPI OHLCV data')
    #     inst_name = r_kospi_ohlcv.code.name
    #     self.assertEqual(inst_name, '삼성전자', msg='Recent KOSPI OHLCV data not created properly')
    #
    #     r_kosdaq_ohlcv, created = RecentKosdaqOHLCV.objects.get_or_create(date='20180101',
    #                                                                       code=self.ticker,
    #                                                                       open_price=1000,
    #                                                                       high_price=1000,
    #                                                                       low_price=1000,
    #                                                                       close_price=1000,
    #                                                                       volume=1000000)
    #     self.assertTrue(created, msg='failed to save Recent KOSDAQ OHLCV data')
    #     inst_name = r_kosdaq_ohlcv.code.name
    #     self.assertEqual(inst_name, '삼성전자', msg='Recent KOSDAQ OHLCV data not created properly')
    #
    #     # check if ForeignKey works properly
    #     kospi_close_price = self.ticker.kp_ohlcv.first().close_price
    #     kosdaq_close_price = self.ticker.kd_ohlcv.first().close_price
    #     r_kospi_close_price = self.ticker.r_kp_ohlcv.first().close_price
    #     r_kosdaq_close_price = self.ticker.r_kd_ohlcv.first().close_price
    #     self.assertEqual(kospi_close_price, 1000, msg='kospi_close_price OHLCV data not created properly')
    #     self.assertEqual(kosdaq_close_price, 1000, msg='kosdaq_close_price OHLCV data not created properly')
    #     self.assertEqual(r_kospi_close_price, 1000, msg='r_kospi_close_price OHLCV data not created properly')
    #     self.assertEqual(r_kosdaq_close_price, 1000, msg='r_kosdaq_close_price OHLCV data not created properly')
    #
    # def test_Info_save(self):
    #     info_inst, created = Info.objects.get_or_create(date='20180101',
    #                                                     code=self.ticker,
    #                                                     )
