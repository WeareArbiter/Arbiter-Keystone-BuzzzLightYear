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
        specs_inst, created = Specs.objects.get_or_create(date='20180101',
                                                          code=self.ticker,
                                                          momentum=100.0,
                                                          volatility=100.0,
                                                          correlation=100.0,
                                                          volume=100,
                                                          momentum_score=90,
                                                          volatility_score=90,
                                                          correlation_score=90,
                                                          volume_score=90,
                                                          total_score=90)
        self.assertTrue(created, msg='failed to save Specs data')
        self.assertEqual(Specs.objects.count(), 1, msg='Specs data not created properly')


    def test_Financial_set_save(self):
        # try and test saving Financial, FinancialRatio, and QuarterFinancial
        fin_inst, created = Financial.objects.get_or_create(date='20180101',
                                                            code=self.ticker,
                                                            revenue=100,
                                                            profit=100,
                                                            net_profit=100,
                                                            consolidate_profit=100,
                                                            asset=100,
                                                            debt=100,
                                                            capital=100)

        fin_rat_inst, created = FinancialRatio.objects.get_or_create(date='20180101',
                                                                     code=self.ticker,
                                                                     debt_ratio=0.1,
                                                                     profit_ratio=0.1,
                                                                     net_profit_ratio=0.1,
                                                                     consolidate_profit_ratio=0.1,
                                                                     net_roe=0.1,
                                                                     consolidate_roe=0.1,
                                                                     revenue_growth=0.1,
                                                                     profit_growth=0.1,
                                                                     net_profit_growth=0.1)

        q_fin, created = QuarterFinancial.objects.get_or_create(date='20180101',
                                                                code=self.ticker,
                                                                revenue=100,
                                                                profit=100,
                                                                net_profit=100,
                                                                consolidate_profit=100,
                                                                profit_ratio=0.1,
                                                                net_profit_ratio=0.1)

        # now test whether the above three instances have been saved correctly
        financial_revenue = self.ticker.financial.first().revenue
        financial_ratio_profit = self.ticker.financial_ratio.first().profit_ratio
        quarter_financial_revenue = self.ticker.quarter_financial.first().revenue
        self.assertEqual(financial_revenue, 100, msg='Financial data not created properly')
        self.assertEqual(financial_ratio_profit, 0.1, msg='Financial Ratio data not created properly')
        self.assertEqual(quarter_financial_revenue, 100, msg='Quarter Financial data not created properly')


    def test_BuySellNetShort_save(self):
        # create OHLCV instance first before save
        kp_ohlcv, created = KospiOHLCV.objects.get_or_create(date='20180101',
                                                             code=self.ticker,
                                                             open_price=1000,
                                                             high_price=1000,
                                                             low_price=1000,
                                                             close_price=1000,
                                                             volume=1000000)

        # creating Kosdaq ticker for KosdaqOHLCV
        kd_ticker, created = Ticker.objects.get_or_create(code='000030',
                                                          name='우리은행',
                                                          market_type='KOSDAQ',
                                                          state=1)

        kd_ohlcv, created = KosdaqOHLCV.objects.get_or_create(date='20180101',
                                                              code=kd_ticker,
                                                              open_price=1000,
                                                              high_price=1000,
                                                              low_price=1000,
                                                              close_price=1000,
                                                              volume=1000000)

        # Buy data
        kp_buy, created = KospiBuy.objects.get_or_create(ohlcv=kp_ohlcv,
                                                         individual=100,
                                                         foreign_retail=100,
                                                         institution=100,
                                                         financial=100,
                                                         insurance=100,
                                                         trust=100,
                                                         etc_finance=100,
                                                         bank=100,
                                                         pension=100,
                                                         private=100,
                                                         nation=100,
                                                         etc_corporate=100)

        kd_buy, created = KosdaqBuy.objects.get_or_create(ohlcv=kd_ohlcv,
                                                          individual=100,
                                                          foreign_retail=100,
                                                          institution=100,
                                                          financial=100,
                                                          insurance=100,
                                                          trust=100,
                                                          etc_finance=100,
                                                          bank=100,
                                                          pension=100,
                                                          private=100,
                                                          nation=100,
                                                          etc_corporate=100)

        # Sell data
        kp_sell, created = KospiSell.objects.get_or_create(ohlcv=kp_ohlcv,
                                                           individual=-100,
                                                           foreign_retail=-100,
                                                           institution=-100,
                                                           financial=-100,
                                                           insurance=-100,
                                                           trust=-100,
                                                           etc_finance=-100,
                                                           bank=-100,
                                                           pension=-100,
                                                           private=-100,
                                                           nation=-100,
                                                           etc_corporate=-100)

        kd_sell, created = KosdaqSell.objects.get_or_create(ohlcv=kd_ohlcv,
                                                            individual=-100,
                                                            foreign_retail=-100,
                                                            institution=-100,
                                                            financial=-100,
                                                            insurance=-100,
                                                            trust=-100,
                                                            etc_finance=-100,
                                                            bank=-100,
                                                            pension=-100,
                                                            private=-100,
                                                            nation=-100,
                                                            etc_corporate=-100)

        # Net data
        kp_net, created = KospiNet.objects.get_or_create(ohlcv=kp_ohlcv,
                                                         individual=0,
                                                         foreign_retail=0,
                                                         institution=0,
                                                         financial=0,
                                                         insurance=0,
                                                         trust=0,
                                                         etc_finance=0,
                                                         bank=0,
                                                         pension=0,
                                                         private=0,
                                                         nation=0,
                                                         etc_corporate=0)

        kd_net, created = KosdaqNet.objects.get_or_create(ohlcv=kd_ohlcv,
                                                          individual=0,
                                                          foreign_retail=0,
                                                          institution=0,
                                                          financial=0,
                                                          insurance=0,
                                                          trust=0,
                                                          etc_finance=0,
                                                          bank=0,
                                                          pension=0,
                                                          private=0,
                                                          nation=0,
                                                          etc_corporate=0)

        # Short data
        kp_short, created = KospiShort.objects.get_or_create(ohlcv=kp_ohlcv,
                                                             short=100,
                                                             short_proportion=0.1,
                                                             short_total_price=1000000,
                                                             short_avg_price=100,
                                                             short_zscale=1.0,
                                                             short_section=1,
                                                             tp_5d_mean=1000000.0,
                                                             short_5d_mean_section=1.0)

        kd_short, created = KosdaqShort.objects.get_or_create(ohlcv=kd_ohlcv,
                                                              short=100,
                                                              short_proportion=0.1,
                                                              short_total_price=1000000,
                                                              short_avg_price=100,
                                                              short_zscale=1.0,
                                                              short_section=1,
                                                              tp_5d_mean=1000000.0,
                                                              short_5d_mean_section=1.0)

        # assertions/tests
        kp_buy_ins = self.ticker.kp_ohlcv.first().buy.institution
        self.assertEqual(kp_buy_ins, 100, msg='KOSPI Buy data not created properly')
