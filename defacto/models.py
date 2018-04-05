from django.db import models
from stockapi.models import (
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    )


# Create your models here.

class KospiAgentData(models.Model):
    '''
    - description: KOSPI & KOSDAQ agent data updated daily
    - period: 20080701 ~
    - data: (date, code, possession, height, proportion, ins_purity, tvalue:tv, coefficient:coef)
    - agent: {'individual':ind, 'foreign_retail': for,
            'institution': ins, 'etc_corporate': cor,
            'trust': tru, 'pension': pen}
    - url: /defacto-api/agent-data/',
    '''
    ohlcv = models.OneToOneField(KospiOHLCV,
                                on_delete=models.CASCADE,
                                related_name='agent_data')
    ind_possession = models.BigIntegerField(blank=True, null=True)
    for_possession = models.BigIntegerField(blank=True, null=True)
    ins_possession = models.BigIntegerField(blank=True, null=True)
    cor_possession = models.BigIntegerField(blank=True, null=True)
    tru_possession = models.BigIntegerField(blank=True, null=True)
    pen_possession = models.BigIntegerField(blank=True, null=True)
    # possession : agent's net_buy cumulative sum + abs(min of cumulative sum)
    circulate_stock = models.BigIntegerField(blank=True, null=True)
    #circulate_stock = sum(ind_possession, for_possession, ins_possession, cor_possession)
    ins_purity = models.FloatField(blank=True, null=True)
    #ins_purity: institution_purity = (tru_possession + pen_possession)/ins_possession
    ind_height = models.FloatField(blank=True, null=True)
    for_height = models.FloatField(blank=True, null=True)
    ins_height = models.FloatField(blank=True, null=True)
    cor_height = models.FloatField(blank=True, null=True)
    #height: each(ind, ins, for, cor) possession / circulate_stock
    ind_proportion = models.FloatField(blank=True, null=True)
    for_proportion = models.FloatField(blank=True, null=True)
    ins_proportion = models.FloatField(blank=True, null=True)
    cor_proportion = models.FloatField(blank=True, null=True)
    #proppotion: buy_amount / volume
    ind_tv = models.FloatField(blank=True, null=True)
    for_tv = models.FloatField(blank=True, null=True)
    ins_tv = models.FloatField(blank=True, null=True)
    cor_tv = models.FloatField(blank=True, null=True)
    ind_coef = models.FloatField(blank=True, null=True)
    for_coef = models.FloatField(blank=True, null=True)
    ins_coef = models.FloatField(blank=True, null=True)
    cor_coef = models.FloatField(blank=True, null=True)
    #regression data

    def __str__(self):
        return '{}'.format(self.ohlcv.code)


class KospiAbsoulteScore(models.Model):
    defacto = models.OneToOneField(KospiAgentData,
                                     on_delete=models.CASCADE,
                                     related_name='absoulte_score')
    ind_height_section = models.IntegerField(blank=True, null=True)
    for_height_section = models.IntegerField(blank=True, null=True)
    ins_height_section = models.IntegerField(blank=True, null=True)
    cor_height_section = models.IntegerField(blank=True, null=True)
    ind_proporion_section = models.IntegerField(blank=True, null=True)
    for_proporion_section = models.IntegerField(blank=True, null=True)
    ins_proporion_section = models.IntegerField(blank=True, null=True)
    cor_proporion_section = models.IntegerField(blank=True, null=True)
    ins_purity_weight = models.FloatField(blank=True, null=True)
    ind_tv_section = models.FloatField(blank=True, null=True)
    for_tv_section = models.FloatField(blank=True, null=True)
    ins_tv_section = models.FloatField(blank=True, null=True)
    cor_tv_section = models.FloatField(blank=True, null=True)
    ind_coef_section = models.FloatField(blank=True, null=True)
    for_coef_section = models.FloatField(blank=True, null=True)
    ins_coef_section = models.FloatField(blank=True, null=True)
    cor_coef_section = models.FloatField(blank=True, null=True)
    ind_ab_score = models.FloatField(blank=True, null=True)
    for_ab_score = models.FloatField(blank=True, null=True)
    ins_ab_score = models.FloatField(blank=True, null=True)
    cor_ab_score = models.FloatField(blank=True, null=True)
    absolute_score = models.FloatField(blank=True, null=True)
    lead_agent = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.agent_data.ohlcv.code)


class KosdaqAgentData(models.Model):
    '''
    - description: KOSDAQ agent data updated daily
    - period: 20080701 ~
    - data: (date, code, possession, height, proportion, ins_purity, tvalue:tv, coefficient:coef)
    - agent: {'individual':ind, 'foreign_retail': for,
            'institution': ins, 'etc_corporate': cor,
            'trust': tru, 'pension': pen}
    - url: /defacto-api/kd-ad-api/',
    '''
    ohlcv = models.OneToOneField(KosdaqOHLCV,
                                on_delete=models.CASCADE,
                                related_name='agent_data')
    ind_possession = models.BigIntegerField(blank=True, null=True)
    for_possession = models.BigIntegerField(blank=True, null=True)
    ins_possession = models.BigIntegerField(blank=True, null=True)
    cor_possession = models.BigIntegerField(blank=True, null=True)
    tru_possession = models.BigIntegerField(blank=True, null=True)
    pen_possession = models.BigIntegerField(blank=True, null=True)
    # possession : agent's net_buy cumulative sum + abs(min of cumulative sum)
    circulate_stock = models.BigIntegerField(blank=True, null=True)
    #circulate_stock = sum(ind_possession, for_possession, ins_possession, cor_possession)
    ins_purity = models.FloatField(blank=True, null=True)
    #ins_purity: institution_purity = (tru_possession + pen_possession)/ins_possession
    ind_height = models.FloatField(blank=True, null=True)
    for_height = models.FloatField(blank=True, null=True)
    ins_height = models.FloatField(blank=True, null=True)
    cor_height = models.FloatField(blank=True, null=True)
    #height: each(ind, ins, for, cor) possession / circulate_stock
    ind_proportion = models.FloatField(blank=True, null=True)
    for_proportion = models.FloatField(blank=True, null=True)
    ins_proportion = models.FloatField(blank=True, null=True)
    cor_proportion = models.FloatField(blank=True, null=True)
    #proppotion: buy_amount / volume
    ind_tv = models.FloatField(blank=True, null=True)
    for_tv = models.FloatField(blank=True, null=True)
    ins_tv = models.FloatField(blank=True, null=True)
    cor_tv = models.FloatField(blank=True, null=True)
    ind_coef = models.FloatField(blank=True, null=True)
    for_coef = models.FloatField(blank=True, null=True)
    ins_coef = models.FloatField(blank=True, null=True)
    cor_coef = models.FloatField(blank=True, null=True)
    #regression data

    def __str__(self):
        return '{}'.format(self.ohlcv.code)


class KosdaqAbsoulteScore(models.Model):
    defacto = models.OneToOneField(KosdaqAgentData,
                                     on_delete=models.CASCADE,
                                     related_name='absolute_score')
    ind_height_section = models.IntegerField(blank=True, null=True)
    for_height_section = models.IntegerField(blank=True, null=True)
    ins_height_section = models.IntegerField(blank=True, null=True)
    cor_height_section = models.IntegerField(blank=True, null=True)
    ind_proporion_section = models.IntegerField(blank=True, null=True)
    for_proporion_section = models.IntegerField(blank=True, null=True)
    ins_proporion_section = models.IntegerField(blank=True, null=True)
    cor_proporion_section = models.IntegerField(blank=True, null=True)
    ins_purity_weight = models.FloatField(blank=True, null=True)
    ind_tv_section = models.FloatField(blank=True, null=True)
    for_tv_section = models.FloatField(blank=True, null=True)
    ins_tv_section = models.FloatField(blank=True, null=True)
    cor_tv_section = models.FloatField(blank=True, null=True)
    ind_coef_section = models.FloatField(blank=True, null=True)
    for_coef_section = models.FloatField(blank=True, null=True)
    ins_coef_section = models.FloatField(blank=True, null=True)
    cor_coef_section = models.FloatField(blank=True, null=True)
    ind_ab_score = models.FloatField(blank=True, null=True)
    for_ab_score = models.FloatField(blank=True, null=True)
    ins_ab_score = models.FloatField(blank=True, null=True)
    cor_ab_score = models.FloatField(blank=True, null=True)
    absolute_score = models.FloatField(blank=True, null=True)
    lead_agent = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.agent_data.ohlcv.code)


class KospiTruePriceData(models.Model):
    '''
    - description: KOSPI agent data updated daily true price
    - period: 20080701 ~
    - data: (date, code, tp, buy_cumsum, apps, tp_buy_cumsum)
    - agent: {'individual':ind, 'foreign_retail': for,
            'institution': ins, 'etc_corporate': cor,
            'trust': tru, 'pension': pen}
    - url: /defacto-api/calc-data/',
    '''
    ohlcv = models.OneToOneField(KospiOHLCV,
                                on_delete=models.CASCADE,
                                related_name='true_price')
    ind_tp = models.FloatField(blank=True, null=True)
    for_tp = models.FloatField(blank=True, null=True)
    ins_tp = models.FloatField(blank=True, null=True)
    cor_tp = models.FloatField(blank=True, null=True)
    #true_price : Reference external documents
    ind_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    for_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    ins_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    cor_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    # buy_cumsum: buy_amount cumsum(ind, for, ins, cor)
    ind_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    for_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    ins_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    cor_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    # tp_buy_cumsum: tp*buy cumsum(ind, for, ins, cor)
    ind_apps = models.FloatField(blank=True, null=True)
    for_apps = models.FloatField(blank=True, null=True)
    ins_apps = models.FloatField(blank=True, null=True)
    cor_apps = models.FloatField(blank=True, null=True)
    # apps : tp_buy_cumsum / buy_cumsum

    def __str__(self):
        return '{}'.format(self.ohlcv.code)



class KosdaqTruePriceData(models.Model):
    '''
    - description: KOSDAQ agent data updated daily true price
    - period: 20080701 ~
    - data: (date, code, tp, buy_cumsum, apps, tp_buy_cumsum)
    - agent: {'individual':ind, 'foreign_retail': for,
            'institution': ins, 'etc_corporate': cor,
            'trust': tru, 'pension': pen}
    - url: /defacto-api/calc-data/',
    '''
    ohlcv = models.OneToOneField(KosdaqOHLCV,
                                on_delete=models.CASCADE,
                                related_name='true_price')
    ind_tp = models.FloatField(blank=True, null=True)
    for_tp = models.FloatField(blank=True, null=True)
    ins_tp = models.FloatField(blank=True, null=True)
    cor_tp = models.FloatField(blank=True, null=True)
    #true_price : Reference external documents
    ind_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    for_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    ins_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    cor_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    # buy_cumsum: buy_amount cumsum(ind, for, ins, cor)
    ind_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    for_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    ins_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    cor_tp_buy_cumsum = models.BigIntegerField(blank=True, null=True)
    # tp_buy_cumsum: tp*buy cumsum(ind, for, ins, cor)
    ind_apps = models.FloatField(blank=True, null=True)
    for_apps = models.FloatField(blank=True, null=True)
    ins_apps = models.FloatField(blank=True, null=True)
    cor_apps = models.FloatField(blank=True, null=True)
    # apps : tp_buy_cumsum / buy_cumsum

    def __str__(self):
        return '{}'.format(self.ohlcv.code)


class KospiRelativeCalc(models.Model):
    '''
    - description: Table to calculate relative score
    - period: 20080701 ~
    - url: None
    '''
    ohlcv = models.OneToOneField(KospiOHLCV,
                                 on_delete=models.CASCADE,
                                 related_name='relative_calc')
    cp_vol = models.FloatField(blank=True, null=True)
    # (close_price * volume) / sum(close_price*volume)
    cp_vol_section = models.IntegerField(blank=True, null=True)
    # divide 24 section
    ins_tp_diff = models.FloatField(blank=True, null=False)
    # ins_apps - close_price / close_price
    for_tp_diff = models.FloatField(blank=True, null=False)
    # for_apps - close_price / close_price
    ins_price_inc = models.FloatField(blank=True, null=False)
    for_price_inc = models.FloatField(blank=True, null=False)
    # divide six secion
    cp_ind = models.FloatField(blank=True, null=True)
    cp_for = models.FloatField(blank=True, null=True)
    cp_ins = models.FloatField(blank=True, null=True)
    cp_cor = models.FloatField(blank=True, null=True)
    # close_price * (ind, for, ins, cor) buy / sum (close_price * (ind, for, ins, cor) buy )
    cp_ind_section = models.IntegerField(blank=True, null=True)
    cp_for_section = models.IntegerField(blank=True, null=True)
    cp_ins_section = models.IntegerField(blank=True, null=True)
    cp_cor_section = models.IntegerField(blank=True, null=True)
    # divide 12 section

    def __str__(self):
        return '{}'.format(self.ohlcv.code)


class KosdaqRelativeCalc(models.Model):
    '''
    - description: Table to calculate relative score
    - period: 20080701 ~
    - url: None
    '''
    ohlcv = models.OneToOneField(KosdaqOHLCV,
                                 on_delete=models.CASCADE,
                                 related_name='relative_calc')
    cp_vol = models.FloatField(blank=True, null=True)
    # (close_price * volume) / sum(close_price*volume)
    cp_vol_section = models.IntegerField(blank=True, null=True)
    # divide 24 section
    ins_tp_diff = models.FloatField(blank=True, null=False)
    # ins_apps - close_price / close_price
    for_tp_diff = models.FloatField(blank=True, null=False)
    # for_apps - close_price / close_price
    ins_price_inc = models.FloatField(blank=True, null=False)
    for_price_inc = models.FloatField(blank=True, null=False)
    # divide six secion
    cp_ind = models.FloatField(blank=True, null=True)
    cp_for = models.FloatField(blank=True, null=True)
    cp_ins = models.FloatField(blank=True, null=True)
    cp_cor = models.FloatField(blank=True, null=True)
    # close_price * (ind, for, ins, cor) buy / sum (close_price * (ind, for, ins, cor) buy )
    cp_ind_section = models.IntegerField(blank=True, null=True)
    cp_for_section = models.IntegerField(blank=True, null=True)
    cp_ins_section = models.IntegerField(blank=True, null=True)
    cp_cor_section = models.IntegerField(blank=True, null=True)
    # divide 12 section

    def __str__(self):
        return '{}'.format(self.ohlcv.code)



class KospiScoreData(models.Model):
    '''
    - description: KOSDAQ score & score change data
    - period: 20080701 ~
    - data: (date, code, absolute_score, relative_score, score_rank, rank_change,
            score_change, lead_agent)
    - lead_agent: ('individual', 'foreigner', 'institution', 'etc', 'None')
    - url: /defacto-api/score-data/
    '''
    ohlcv = models.OneToOneField(KospiOHLCV,
                                 on_delete=models.CASCADE,
                                 related_name='score_data')
    absolute_score = models.FloatField(blank=True, null=True)
    relative_score = models.FloatField(blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    score_rank = models.IntegerField(blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    score_change = models.FloatField(blank=True, null=True)
    lead_agent = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.code)


class KosdaqScoreData(models.Model):
    '''
    - description: KOSDAQ score & score change data
    - period: 20080701 ~
    - data: (date, code, absolute_score, relative_score, score_rank, rank_change,
            score_change, lead_agent)
    - lead_agent: ('individual', 'foreigner', 'institution', 'etc', 'None')
    - url: /defacto-api/score-data/
    '''
    ohlcv = models.OneToOneField(KosdaqOHLCV,
                                 on_delete=models.CASCADE,
                                 related_name='score_data')
    absolute_score = models.FloatField(blank=True, null=True)
    relative_score = models.FloatField(blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    score_rank = models.IntegerField(blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    score_change = models.FloatField(blank=True, null=True)
    lead_agent = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.code)



class RankData(models.Model):
    '''
    - description: daily rank data for buzzz defacto page
    - period: -
    - data: (code, name, lead_agent, total_score, rank_change, sign)
    - url: /defacto-api/rank-data/
    '''
    date = models.CharField(max_length=8)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='rank_data')
    lead_agent = models.CharField(max_length=20, blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=40, blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.code)
