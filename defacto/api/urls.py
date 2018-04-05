from django.conf.urls import url

from defacto.api.views import (
    KospiAgentDataAPIView,
    KosdaqAgentDataAPIView,
    KospiTruePriceAPIView,
    KosdaqTruePriceAPIView,
    KospiScoreDataAPIView,
    KosdaqScoreDataAPIView,
    RankDataAPIView,)

urlpatterns = [
    url(r'^kp-ad-api/$', KospiAgentDataAPIView.as_view(), name='kp-agent-data'),
    url(r'^kd-ad-api/$', KosdaqAgentDataAPIView.as_view(), name='kd-agent-data'),
    url(r'^kp-tp-api/$', KospiTruePriceAPIView.as_view(), name='kp-true-price'),
    url(r'^kd-tp-api/$', KosdaqTruePriceAPIView.as_view(), name='kd-true-price'),
    url(r'^kp-sd-api/$', KospiScoreDataAPIView.as_view(), name='kp-score-data'),
    url(r'^kd-sd-api/$', KosdaqScoreDataAPIView.as_view(), name='kd-score-data'),
    url(r'^rd-api/$', RankDataAPIView.as_view(), name='rank-data'),
]
