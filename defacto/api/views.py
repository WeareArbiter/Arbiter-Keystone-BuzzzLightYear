from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from defacto.models import (
    KospiAgentData,
    KosdaqAgentData,
    KospiAgentCalcData,
    KosdaqAgentCalcData,
    DefactoReg,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    )
from defacto.api.serializers import (
    KospiAgentDataSerializer,
    KosdaqAgentDataSerializer,
    KospiAgentCalcDataSerializer,
    KosdaqAgentCalcDataSerializer,
    DefactoRegSerializer,
    KospiScoreDataSerializer,
    KosdaqScoreDataSerializer,
    RankDataSerializer,
    )
from utils.paginations import StandardResultPagination

class KospiAgentDataAPIView(generics.ListAPIView):
    queryset = KospiAgentData.objects.all()
    serializer_class = KospiAgentDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = KospiAgentData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset

class KosdaqAgentDataAPIView(generics.ListAPIView):
    queryset = KosdaqAgentCalcData.objects.all()
    serializer_class = KosdaqAgentCalcDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = KospiAgentData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class KospiAgentCalcDataAPIView(generics.ListAPIView):
    queryset = KospiAgentCalcData.objects.all()
    serializer_class = KospiAgentCalcDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = KospiAgentCalcData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class KosdaqAgentCalcDataAPIView(generics.ListAPIView):
    queryset = KosdaqAgentCalcData.objects.all()
    serializer_class = KosdaqAgentCalcDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = KosdaqAgentCalcData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class DefactoRegAPIView(generics.ListAPIView):
    queryset = DefactoReg.objects.all()
    serializer_class = DefactoRegSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = DefactoReg.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class KospiScoreDataAPIView(generics.ListAPIView):
    queryset = KospiScoreData.objects.all()
    serializer_class = KospiScoreDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = KospiScoreData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        lead_agent_by = self.request.GET.get('lead_agent')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if lead_agent_by:
            queryset = queryset.filter(lead_agent=lead_agent_by)
        return queryset


class KosdaqScoreDataAPIView(generics.ListAPIView):
    queryset = KosdaqScoreData.objects.all()
    serializer_class = KosdaqScoreDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = KosdaqScoreData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        lead_agent_by = self.request.GET.get('lead_agent')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if lead_agent_by:
            queryset = queryset.filter(lead_agent=lead_agent_by)
        return queryset


class RankDataAPIView(generics.ListAPIView):
    queryset = RankData.objects.all()
    serializer_class = RankDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = RankData.objects.all()
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        category = self.request.GET.get('category')
        rankpage = self.request.GET.get('rankpage')
        items_per_page = 0
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if category:
            queryset = queryset.filter(cartegory=category)
            items_per_page = 10 if 'score' in category else 6
        if rankpage:
            start_index = (int(rankpage) - 1) * items_per_page
            end_index = int(rankpage) * items_per_page
            queryset = queryset.order_by('id')[start_index:end_index]
        return queryset
