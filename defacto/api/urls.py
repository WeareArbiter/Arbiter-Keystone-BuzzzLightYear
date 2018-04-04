from django.conf.urls import url

from defacto.api.views import (
    KospiAgentDataAPIView,
    KosdaqAgentDataAPIView,
    KospiAgentCalcDataAPIView,
    KosdaqAgentCalcDataAPIView,
    DefactoRegAPIView,
    KospiScoreDataAPIView,
    KosdaqScoreDataAPIView,
    RankDataAPIView,)

urlpatterns = [
    url(r'^kp-agent-data/$', KospiAgentDataAPIView.as_view(), name='kp-agent-data'),
    url(r'^kd-agent-data/$', KosdaqAgentDataAPIView.as_view(), name='kd-agent-data'),
    url(r'^kp-calc-data/$', KospiAgentCalcDataAPIView.as_view(), name='kp-calc-data'),
    url(r'^kd-calc-data/$', KosdaqAgentCalcDataAPIView.as_view(), name='kd-calc-data'),
    url(r'^reg-data/$', DefactoRegAPIView.as_view(), name='reg-data'),
    url(r'^kp-score-data/$', KospiScoreDataAPIView.as_view(), name='kp-score-data'),
    url(r'^kd-score-data/$', KosdaqScoreDataAPIView.as_view(), name='kd-score-data'),
    url(r'^rank-data/$', RankDataAPIView.as_view(), name='rank-data'),
]
