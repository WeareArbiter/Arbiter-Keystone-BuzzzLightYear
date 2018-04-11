from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/', include('buzzzapi.urls', namespace='api')),
    url(r'^stock-api/', include('stockapi.urls', namespace='stockapi')),
    url(r'^market-api/', include('marketsignal.api.urls', namespace='marketsignal-api')), # api views
    url(r'^defacto/', include('defacto.urls', namespace='defacto')), # general views
    url(r'^defacto-api/', include('defacto.api.urls', namespace='defacto-api')), # api views
    url(r'^portfolio/', include('portfolio.urls', namespace='portfolio')),
    url(r'^portfolio-api/', include('portfolio.api.urls', namespace='portfolio-api')),
]
