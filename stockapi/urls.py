from django.conf.urls import url
from stockapi.views import BMAPIView


urlpatterns = [
    url(r'^bm/$', BMAPIView.as_view(), name='bm'),
]
