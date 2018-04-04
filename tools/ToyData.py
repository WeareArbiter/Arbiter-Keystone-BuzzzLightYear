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


class ToyData(object):
    def __init__(self, send_data):
        if send_data == True:
            ticker, created = Ticker.objects.get_or_create(code='005930',
                                                           name='삼성전자',
                                                           market_type='KOSPI',
                                                           state=1)

            kp_ohlcv, created = KospiOHLCV.objects.get_or_create(date='20180101',
                                                                 code=ticker,
                                                                 open_price=1000,
                                                                 high_price=1000,
                                                                 low_price=1000,
                                                                 close_price=1000,
                                                                 volume=1000000)

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

    def check_data(self):
        ticker = Ticker.objects.all().first()
        ohlcv = ticker.kp_ohlcv.all().first()
        buy = ohlcv.buy.institution
        print(buy)
