from django.contrib import admin

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
)

models = [
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
]
for model in models:
    admin.site.register(model)
