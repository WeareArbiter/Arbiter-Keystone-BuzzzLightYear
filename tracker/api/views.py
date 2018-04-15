from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from tracker.models import ProjectState
from tracker.api.serializers import ProjectStateSerializer

from utils.paginations import StandardResultPagination, OHLCVPagination


class ProjectStateAPIView(generics.ListAPIView):
    serializer_class = ProjectStateSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = ProjectState.objects.all().order_by('-id')
        date_by = self.request.GET.get('date')
        if date_by:
            queryset = queryset.filter(date=date_by)
        return queryset
