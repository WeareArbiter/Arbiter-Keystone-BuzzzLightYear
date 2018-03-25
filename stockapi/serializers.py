from rest_framework import serializers
from stockapi.models import (
    BM,
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    RecentKospiOHLCV,
    RecentKosdaqOHLCV,
    Info,
    Specs,
    Financial,
    FinancialRatio,
    QuarterFinancial,
    KospiBuy,
    KosdaqBuy,
    ETFBuy,
    KospiSell,
    KosdaqSell,
    ETFSellm
    KospiNet,
    KosdaqNet,
    ETFNet,
)


### KOSPI & KOSDAQ data ###
class BMSerializer(serializers.ModelSerializer):
    class Meta:
        model = BM
        fields = ('date',
                  'name',
                  'index',
                  'individual',
                  'foreigner',
                  'institution',)


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = ('code',
                  'name',
                  'market_type',
                  'state',)


### OHLCV ###
class KospiOHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiOHLCV
        fields = ('date',
                  'code',
                  'open_price',
                  'high_price',
                  'low_price',
                  'close_price',
                  'volume',)


class KosdaqOHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqOHLCV
        fields = ('date',
                  'code',
                  'open_price',
                  'high_price',
                  'low_price',
                  'close_price',
                  'volume',)


class RecentKospiOHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentKospiOHLCV
        fields = ('date',
                  'code',
                  'open_price',
                  'high_price',
                  'low_price',
                  'close_price',
                  'volume',)


class RecentKosdaqOHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentKosdaqOHLCV
        fields = ('date',
                  'code',
                  'open_price',
                  'high_price',
                  'low_price',
                  'close_price',
                  'volume',)


### Info and stock specs ###
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('date',
                  'code',
                  'name',
                  'size_type',
                  'style_type',
                  'market_type',
                  'face_val',
                  'stock_nums',
                  'price',
                  'market_cap',
                  'market_cap_rank',
                  'industry',
                  'foreign_limit',
                  'foreign_possession',
                  'foreign_ratio',
                  'per',
                  'eps',
                  'pbr',
                  'bps',
                  'industry_per',
                  'yield_ret',)


class SpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specs
        fields = ('date',
                  'code',
                  'momentum',
                  'volatility',
                  'correlation',
                  'volume',
                  'momentum_score',
                  'volatility_score',
                  'correlation_score',
                  'volume_score',
                  'total_score',)


### Financial Statement data ###
class FinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financial
        fields = ('date',
                  'code',
                  'name',
                  'revenue',
                  'profit',
                  'net_profit',
                  'consolidate_profit',
                  'asset',
                  'debt',
                  'capital',)


class FinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRatio
        fields = ('date',
                  'code',
                  'name',
                  'debt_ratio',
                  'profit_ratio',
                  'net_profit_ratio',
                  'consolidate_profit_ratio',
                  'net_roe',
                  'consolidate_roe',
                  'revenue_growth',
                  'profit_growth',
                  'net_profit_growth',)


class QuarterFinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterFinancial
        fields = ('date',
                  'code',
                  'name',
                  'revenue',
                  'profit',
                  'net_profit',
                  'consolidate_profit',
                  'profit_ratio',
                  'net_profit_ratio',)


### Buy & Sell data ###
class KospiBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiBuy
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KosdaqBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqBuy
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class ETFBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = ETFBuy
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KospiSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiSell
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KosdaqSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqSell
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class ETFSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETFSell
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KospiNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiNet
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KosdaqNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqNet
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class ETFNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETFNet
        fields = ('date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)
