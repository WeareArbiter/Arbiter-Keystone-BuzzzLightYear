from django.conf.urls import url

from defacto.api.views import (
    AgentCalcDataAPIView,
    AgentDataAPIView,
    DefactoTickerAPIView,
    DefactoRegAPIView,
    ScoreDataAPIView,
    RankDataAPIView,)

urlpatterns = [
    url(r'^defacto-ticker/$', DefactoTickerAPIView.as_view(), name='defacto-ticker'),
    url(r'^agent-data/$', AgentDataAPIView.as_view(), name='agent-data'),
    url(r'^calc-data/$', AgentCalcDataAPIView.as_view(), name='agent-calc-data'),
    url(r'^reg-data/$', DefactoRegAPIView.as_view(), name='reg-data'),
    url(r'^score-data/$', ScoreDataAPIView.as_view(), name='score-data'),
    url(r'^rank-data/$', RankDataAPIView.as_view(), name='rank-data'),
]
