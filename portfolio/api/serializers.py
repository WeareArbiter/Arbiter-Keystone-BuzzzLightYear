import time, datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from portfolio.models import Portfolio, PortfolioItem

User = get_user_model()


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id',
                  'user',
                  'name',
                  'capital',
                  'portfolio_type',
                  'description',
                  'created',
                  'updated',)


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ('id',
                  'portfolio',
                  'date',
                  'code',
                  'status',
                  'quantity',
                  'price',)
