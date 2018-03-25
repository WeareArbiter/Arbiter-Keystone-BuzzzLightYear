from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/', include('buzzzapi.urls', namespace='api')),
    url(r'^stock-api/', include('stockapi.urls', namespace='stockapi')),
    url(r'^defacto/', include('defacto.urls', namespace='defacto')), # general views
    url(r'^sd-api/', include('defacto.api.urls', namespace='sd-api')), # api views
]
