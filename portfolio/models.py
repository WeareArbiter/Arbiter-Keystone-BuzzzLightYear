from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from accounts.models import Profile
from stockapi.models import Ticker

PORTFOLIO_TYPES = (
    ('S', 'Stock'),
    ('CS', 'Cash + Stock'),
)

STATUS = (
    ('B', 'Bought'),
    ('S', 'Sold'),
)


class Portfolio(models.Model):
    user = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name='portfolio')
    name = models.CharField(max_length=100,
                            blank=True,
                            null=True)
    capital = models.BigIntegerField(blank=True, null=True)
    portfolio_type = models.CharField(max_length=2,
                                      choices=PORTFOLIO_TYPES,
                                      blank=True,
                                      null=True)
    description = models.CharField(max_length=120,
                                   blank=True,
                                   null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user.username


class PortfolioItem(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='item')
    date = models.CharField(max_length=8)
    code = models.ForeignKey(Ticker, related_name = 'portfolio_record')
    status = models.CharField(max_length=1, choices=STATUS)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return self.portfolio.name

class PortfolioSpecs(models.Model):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE,
                                  related_name = 'portfolio_ret')
    date = models.CharField(max_length=10)
    portfolio_ratio = JSONField()
    ret = models.FloatField(blank=True, null=True)
    avg_ret = models.FloatField(blank=True, null=True)
    avg_vol = models.FloatField(blank=True, null=True)
    sharp_ratio = models.FloatField(blank=True, null=True)
    w_ret = models.FloatField(blank=True, null=True)
    m_ret = models.FloatField(blank=True, null=True)
    q_ret = models.FloatField(blank=True, null=True)
    h_ret = models.FloatField(blank=True, null=True)
    y_ret = models.FloatField(blank=True, null=True)
    kp_w_ret = models.FloatField(blank=True, null=True)
    kp_m_ret = models.FloatField(blank=True, null=True)
    kp_q_ret = models.FloatField(blank=True, null=True)
    kp_h_ret = models.FloatField(blank=True, null=True)
    kp_y_ret = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.portfolio.user.user)
