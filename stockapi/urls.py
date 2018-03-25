from django.conf.urls import url
from stockapi.views import BMAPIView

from stockapi.views import (
    BMAPIView,
    TickerAPIView,
    # KospiOHLCVAPIView,
    # KosdaqOHLCVAPIView,
    # RecentKospiOHLCVAPIView,
    # RecentKosdaqOHLCVAPIView,
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
    url(r'^bm/$', BMAPIView.as_view(), name='bm'),
    url(r'^ticker/$', TickerAPIView.as_view(), name='ticker'),
]
