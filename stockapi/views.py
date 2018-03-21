from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from stockapi.models import BM
from stockapi.serializers import BMSerializer

from utils.paginations import StandardResultPagination, OHLCVPagination


class BMAPIView(generics.ListCreateAPIView):
    queryset = BM.objects.all()
    serializer_class = BMSerializer
    pagination_class = OHLCVPagination
    filter_backends = [SearchFilter, OrderingFilter]
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        queryset = BM.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        name_by = self.request.GET.get('name')
        category_by = self.request.GET.get('category')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if category_by:
            queryset = queryset.filter(category=category_by)
        return queryset
