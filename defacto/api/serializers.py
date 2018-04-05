from rest_framework import serializers
from defacto.models import (
    KospiAgentData,
    KosdaqAgentData,
    KospiTruePriceData,
    KosdaqTruePriceData,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    )


class KospiAgentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiAgentData
        fields = ('ohlcv',
                  'ind_possession',
                  'for_possession',
                  'ins_possession',
                  'cor_possession',
                  'ind_height',
                  'for_height',
                  'ins_height',
                  'cor_height',
                  'ins_purity',
                  'ind_tv',
                  'for_tv',
                  'ins_tv',
                  'cor_tv',
                  'ind_coef',
                  'for_coef',
                  'ins_coef',
                  'cor_coef',)

class KosdaqAgentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqAgentData
        fields = ('ohlcv'
                  'ind_possession',
                  'for_possession',
                  'ins_possession',
                  'cor_possession',
                  'ind_height',
                  'for_height',
                  'ins_height',
                  'cor_height',
                  'ins_purity',
                  'ind_tv',
                  'for_tv',
                  'ins_tv',
                  'cor_tv',
                  'ind_coef',
                  'for_coef',
                  'ins_coef',
                  'cor_coef',)


class KospiTruePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiTruePriceData
        fields = ('ohlcv',
                  'ind_tp',
                  'for_tp',
                  'ins_tp',
                  'cor_tp',
                  'ind_buy_cumsum',
                  'for_buy_cumsum',
                  'ins_buy_cumsum',
                  'cor_buy_cumsum',
                  'ind_tp_buy_cumsum',
                  'for_tp_buy_cumsum',
                  'ins_tp_buy_cumsum',
                  'cor_tp_buy_cumsum',
                  'ind_apps',
                  'for_apps',
                  'ins_apps',
                  'cor_apps',)


class KosdaqTruePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqTruePriceData
        fields = ('date',
                  'code',
                  'ind_tp',
                  'for_tp',
                  'ins_tp',
                  'cor_tp',
                  'ind_buy_cumsum',
                  'for_buy_cumsum',
                  'ins_buy_cumsum',
                  'cor_buy_cumsum',
                  'ind_tp_buy_cumsum',
                  'for_tp_buy_cumsum',
                  'ins_tp_buy_cumsum',
                  'cor_tp_buy_cumsum',
                  'ind_apps',
                  'for_apps',
                  'ins_apps',
                  'cor_apps',)


class KospiScoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiScoreData
        fields = ('date',
                  'code',
                  'absolute_score',
                  'relative_score',
                  'total_score',
                  'score_rank',
                  'rank_change',
                  'score_change',
                  'lead_agent',)


class KosdaqScoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqScoreData
        fields = ('date',
                  'code',
                  'absolute_score',
                  'relative_score',
                  'total_score',
                  'score_rank',
                  'rank_change',
                  'score_change',
                  'lead_agent',)


class RankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankData
        fields = ('id',
                  'date',
                  'code',
                  'lead_agent',
                  'total_score',
                  'category',
                  'rank_change',
                  'sign',)
