from rest_framework import serializers
from defacto.models import AgentData, AgentCalcData, ScoreData, RankData


class AgentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentData
        fields = ('date',
                  'code',
                  'ind_possession',
                  'for_possession',
                  'ins_possession',
                  'cor_possession',
                  'ind_height',
                  'for_height',
                  'ins_height',
                  'cor_height',
                  'ins_purity',)


class AgentCalcDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentCalcData
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


class ScoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreData
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
                  'name',
                  'lead_agent',
                  'total_score',
                  'category',
                  'rank_change',
                  'sign',)
