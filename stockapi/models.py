from django.db import models

SIZE_TYPES = (
    ('L', 'Large Cap'), # large cap stocks
    ('M', 'Middle Cap'), # mid cap stocks
    ('S', 'Small Cap'), # small cap stocks
)

STYLE_TYPES = (
    ('G', 'Growth'), # growth stocks
    ('V', 'Value'), # value stocks
    ('D', 'Dividend'), # high dividend stocks
)


class BM(models.Model):
    '''
    - description: KOSPI & KOSDAQ benchmarks index points
    - period: 20000104 ~
    - data: (date, name, index, volume, individual, foreigner, institution)
    - url: /stock-api/bm/
    '''
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    index = models.FloatField()
    volume = models.IntegerField()
    individual = models.IntegerField()
    foreigner = models.IntegerField()
    institution = models.IntegerField()

    def __str__(self):
        return self.name


class Ticker(models.Model):
    '''
    - description: KOSPI & KOSDAQ tickers updated daily
    - period: -
    - data: (code, name, market_type, state)
    - url: /stock-api/ticker/
    '''
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    market_type = models.CharField(max_length=10)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


### OHLCV ###
class KospiOHLCV(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kp_ohlcv')
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.code)


class KosdaqOHLCV(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kd_ohlcv')
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.code)


class RecentKospiOHLCV(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='r_kp_ohlcv')
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.code)


class RecentKosdaqOHLCV(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='r_kd_ohlcv')
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.code)


class Info(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='info')
    name = models.CharField(max_length=50)
    size_type = models.CharField(max_length=1,
                                 choices=SIZE_TYPES,
                                 blank=True,
                                 null=True) # 사이즈
    style_type = models.CharField(max_length=1,
                                  choices=STYLE_TYPES,
                                  blank=True,
                                  null=True) # 스타일
    market_type=models.CharField(max_length=10)
    face_val = models.CharField(max_length=10,
                                blank=True,
                                null=True) # 액면가
    stock_nums = models.BigIntegerField(blank=True, null=True) # 상장주식수
    price = models.IntegerField(blank=True)#당일 종가
    market_cap = models.BigIntegerField(blank=True, null=True) # 시가총액
    market_cap_rank = models.IntegerField(blank=True, null=True) # 시가총액 순위
    industry = models.CharField(max_length=50,
                                blank=True,
                                null=True) # 산업
    foreign_limit = models.BigIntegerField(blank=True, null=True)
    foreign_possession = models.BigIntegerField(blank=True, null=True)
    foreign_ratio = models.FloatField(blank=True, null=True)
    per = models.FloatField(blank=True, null=True) # PER로 성장주/가치주 구분
    eps = models.FloatField(blank=True, null=True)
    pbr = models.FloatField(blank=True, null=True)
    bps = models.FloatField(blank=True)
    industry_per = models.FloatField(blank=True)
    yield_ret = models.FloatField(blank=True, null=True) # 배당수익률

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class Specs(models.Model):
    date = models.CharField(max_length=8)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='specs')
    momentum = models.FloatField(blank=True, null=True)
    volatility = models.FloatField(blank=True, null=True)
    correlation = models.FloatField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    momentum_score = models.IntegerField(blank=True, null=True)
    volatility_score = models.IntegerField(blank=True, null=True)
    correlation_score = models.IntegerField(blank=True, null=True)
    volume_score = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.code
