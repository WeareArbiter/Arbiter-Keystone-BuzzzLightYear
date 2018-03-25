from django.conf.urls import url

from stockapi.views import (
    BenchmarkAPIView,
    TickerAPIView,
    KospiOHLCVAPIView,
    KosdaqOHLCVAPIView,
    RecentKospiOHLCVAPIView,
    RecentKosdaqOHLCVAPIView,
    # InfoAPIView,
    # SpecsAPIView,
    # FinancialAPIView,
    # FinancialRatioAPIView,
    # QuarterFinancialAPIView,
    # KospiBuyAPIView,
    # KosdaqBuyAPIView,
    # ETFBuyAPIView,
    # KospiSellAPIView,
    # KosdaqSellAPIView,
    # ETFSellAPIView,
    # KospiNetAPIView,
    # KosdaqNetAPIView,
    # ETFNetAPIView,
)


urlpatterns = [
    url(r'^bm/$', BenchmarkAPIView.as_view(), name='bm'),
    url(r'^ticker/$', TickerAPIView.as_view(), name='ticker'),
    url(r'^kospi/$', KospiOHLCVAPIView.as_view(), name='kospi-ohlcv'),
    url(r'^kosdaq/$', KosdaqOHLCVAPIView.as_view(), name='kosdaq-ohlcv'),
    url(r'^recent-kospi/$', RecentKospiOHLCVAPIView.as_view(), name='recent-kospi-ohlcv'),
    url(r'^recent-kosdaq/$', RecentKosdaqOHLCVAPIView.as_view(), name='recent-kosdaq-ohlcv'),
]
