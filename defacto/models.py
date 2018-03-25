from django.db import models

# Create your models here.
class DefacoTicker(models.Model):
    '''
    - description: KOSPI & KOSDAQ tickers for defaco model
    - data: (code, name, market_type, state)
    - url:
    '''
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    market_type = models.CharField(max_length=10)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)

class AgentData(models.Model):
    '''
    - description: KOSPI & KOSDAQ agent data updated daily
    - period: 20080701 ~
    - data: (date, code, possession, height, proportion, ins_purity)
    - agent: {'individual':ind, 'foreign_retail': for,
            'institution': ins, 'etc_corporate': cor,
            'trust': tru, 'pension': pen}
    - url:
    '''
    date = models.CharField(max_length=8)
    code = models.ForeignKey(DefacoTicker,
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

    def __str__(self):
        return '{}'.format(self.code)

class AgentCalcData(models.Model):
    '''
    - description: KOSPI & KOSDAQ agent data updated daily to calculate absolute score
    - period: 20080701 ~
    - data: (date, code, tp, buy_cumsum, apps, tp_buy_cumsum)
    - agent: {'individual':ind, 'foreign_retail': for,
            'institution': ins, 'etc_corporate': cor,
            'trust': tru, 'pension': pen}
    - url:
    '''
    date = models.CharField(max_length=8)
    code = models.ForeignKey(DefacoTicker,
                             on_delete=models.CASCADE,
                             related_name='agent_calc_data')
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
        return '{}'.format(self.code)


class ScoreData(models.Model):
    '''
    - description: KOSPI & KOSDAQ score & score change data
    - period: 20080701 ~
    - data: (date, code, absolute_score, relative_score, score_rank, rank_change,
            score_change, lead_agent)
    - lead_agent: ('individual', 'foreigner', 'institution', 'etc', 'None')
    - url:
    '''
    date = models.CharField(max_length=8)
    code = models.ForeignKey(DefacoTicker,
                             on_delete=models.CASCADE,
                             related_name='score_data')
    absolute_score = models.FloatField(blank=True, null=True)
    relative_score = models.FloatField(blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    score_rank = models.IntegerField(blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    score_change = models.FloatField(blank=True, null=True)
    lead_agent = models.CharField(max_length=20,
                                  blank=True,
                                  null=True)

    def __str__(self):
        return '{}'.format(self.code)


class RankData(models.Model):
    '''
    - description: daily rank data for buzzz defaco page
    - period: -
    - data: (code, name, lead_agent, total_score, rank_change, sign)
    - url:
    '''
    date = models.CharField(max_length=8)
    code = models.ForeignKey(DefacoTicker,
                             on_delete=models.CASCADE,
                             related_name='rank_data')
    lead_agent = models.CharField(max_length=20, blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=40, blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.code)
