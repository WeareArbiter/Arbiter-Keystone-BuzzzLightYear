from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from portfolio.models import (
    Portfolio,
    PortfolioItem,
    PortfolioSpecs,
    )

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

class PortfolioSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioSpecs
        fields = ('portfolio',
                  'date',
                  'portfolio_ratio',
                  'ret',
                  'avg_ret',
                  'avg_vol',
                  'sharp_ratio',
                  'w_ret',
                  'm_ret',
                  'q_ret',
                  'h_ret',
                  'y_ret',
                  'kp_w_ret',
                  'kp_m_ret',
                  'kp_q_ret',
                  'kp_h_ret',
                  'kp_y_ret',)
