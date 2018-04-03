from rest_framework import serializers
from stockapi.models import (
    Benchmark,
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
    KospiSell,
    KosdaqSell,
    KospiNet,
    KosdaqNet,
    KospiShort,
    KosdaqShort,
)


### KOSPI & KOSDAQ data ###
class BenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benchmark
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
        fields = ('ohlcv',
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
                  'etc_corporate',)


class KosdaqBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqBuy
        fields = ('ohlcv',
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
                  'etc_corporate',)


class KospiSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiSell
        fields = ('ohlcv',
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
                  'etc_corporate',)


class KosdaqSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqSell
        fields = ('ohlcv',
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
                  'etc_corporate',)


class KospiNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiNet
        fields = ('ohlcv',
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
                  'etc_corporate',)


class KosdaqNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqNet
        fields = ('ohlcv',
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
                  'etc_corporate',)


class KospiShortSerialier(serializers.ModelSerializer):
    class Meta:
        model = KospiShort
        fields = ('ohlcv',
                  'short',
                  'short_proportion',
                  'short_total_price',
                  'short_avg_price',
                  'short_zscale',
                  'short_section',
                  'tp_5d_mean',
                  'short_5d_mean_section',)

class KosdaqShortSerialier(serializers.ModelSerializer):
    class Meta:
        model = KosdaqShort
        fields = ('ohlcv',
                  'short',
                  'short_proportion',
                  'short_total_price',
                  'short_avg_price',
                  'short_zscale',
                  'short_section',
                  'tp_5d_mean',
                  'short_5d_mean_section',)
