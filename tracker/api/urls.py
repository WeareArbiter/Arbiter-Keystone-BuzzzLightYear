from django.conf.urls import url

from tracker.api.views import ProjectStateAPIView

urlpatterns = [
    url(r'^project-state/$', ProjectStateAPIView.as_view(), name='project-state'),
]
