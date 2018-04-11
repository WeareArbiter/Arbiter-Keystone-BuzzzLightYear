from django.shortcuts import render
from django.views import View


class RealTimeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'realtime.html', {})
