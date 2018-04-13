from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from portfolio.api.serializers import (
    PortfolioSerializer,
    PortfolioItemSerializer,
    PortfolioSpecsSerializer,
    )

from portfolio.models import (
    Portfolio,
    PortfolioItem,
    PortfolioSpecs,
    )

from stockapi.models import Ticker

from utils.paginations import UserResultPagination, StandardResultPagination

class PortfolioAPIView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all().order_by('-id')
    serializer_class = PortfolioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultPagination

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PortfolioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['user'] = request.user
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PortfolioItemAPIView(generics.ListCreateAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultPagination

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data['portfolio'] = Portfolio.objects.get(id=data['portfolio']).id
    #     ticker = Ticker.objects.filter(code=data['code']).order_by('-code').first()
    #     data['code'] = ticker.id
    #     data['date'] = ticker.date
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PortfolioItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PortfolioSpecsAPIView(generics.ListAPIView):
    queryset = PortfolioSpecs.objects.all()
    serializer_class = PortfolioItemDetailAPIView
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultPagination
