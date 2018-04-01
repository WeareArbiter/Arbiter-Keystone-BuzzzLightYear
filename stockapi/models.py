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


### KOSPI & KOSDAQ data ###
class Benchmark(models.Model):
    '''
    - description: KOSPI & KOSDAQ benchmarks index points
    - period: 20000104 ~
    - data: (date, name, index, volume, individual, foreigner, institution)
    - url: /stock-api/bm/
    '''
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    index = models.FloatField()
    volume = models.IntegerField(null=True)
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
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    market_type = models.CharField(max_length=10)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


### OHLCV ###
class KospiOHLCV(models.Model):
    '''
    - description: KOSPI OHLCV updated daily after market closes
    - period: -
    - data: (date, code, open_price, high_price, low_price, close_price, volume)
    - url: /stock-api/kospi/
    '''
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
    '''
    - description: KOSDAQ OHLCV updated daily after market closes
    - period: -
    - data: (date, code, open_price, high_price, low_price, close_price, volume)
    - url: /stock-api/kosdaq/
    '''
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
    '''
    - description: Recent 5 years of KOSPI OHLCV data renewed from KospiOHLCV everyday
    - period: -
    - data: (date, code, open_price, high_price, low_price, close_price, volume)
    - url: /stock-api/recent-kospi/
    '''
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
    '''
    - description: Recent 5 years of KOSDAQ OHLCV data renewed from KosdaqOHLCV everyday
    - period: -
    - data: (date, code, open_price, high_price, low_price, close_price, volume)
    - url: /stock-api/recent-kosdaq/
    '''
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


### Info and stock specs ###
class Info(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='info')
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
    price = models.IntegerField(blank=True) # 당일 종가
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


### Financial Statement data ###
class Financial(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='financial')
    revenue = models.IntegerField(blank=True, null=True)
    profit = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    consolidate_profit = models.IntegerField(blank=True, null=True)
    asset = models.IntegerField(blank=True, null=True)
    debt = models.IntegerField(blank=True, null=True)
    capital = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class FinancialRatio(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='financial_ratio')
    debt_ratio = models.FloatField(blank=True, null=True)
    profit_ratio = models.FloatField(blank=True, null=True)
    net_profit_ratio = models.FloatField(blank=True, null=True)
    consolidate_profit_ratio = models.FloatField(blank=True, null=True)
    net_roe = models.FloatField(blank=True, null=True)
    consolidate_roe = models.FloatField(blank=True, null=True)
    revenue_growth = models.FloatField(blank=True, null=True)
    profit_growth = models.FloatField(blank=True, null=True)
    net_profit_growth = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class QuarterFinancial(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='quarter_financial')
    revenue = models.IntegerField(blank=True, null=True)
    profit = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    consolidate_profit = models.IntegerField(blank=True, null=True)
    profit_ratio = models.FloatField(blank=True, null=True)
    net_profit_ratio = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


### Buy & Sell data ###
class KospiBuy(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kospi_buy')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KosdaqBuy(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kosdaq_buy')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class ETFBuy(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='etf_buy')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KospiSell(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kospi_sell')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KosdaqSell(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kosdaq_sell')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class ETFSell(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='etf_sell')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KospiNet(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kospi_net')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KosdaqNet(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kosdaq_net')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class ETFNet(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='etf_net')
    individual = models.IntegerField(blank=True, null=True)
    foreign_retail = models.IntegerField(blank=True, null=True)
    institution = models.IntegerField(blank=True, null=True)
    financial = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    etc_finance = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    pension = models.IntegerField(blank=True, null=True)
    private = models.IntegerField(blank=True, null=True)
    nation = models.IntegerField(blank=True, null=True)
    etc_corporate = models.IntegerField(blank=True, null=True)
    foreign = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KospiShort(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kp_short')
    short = models.IntegerField(blank=True, null=True)
    short_proportion = models.FloatField(blank=True, null=True)
    short_total_price = models.IntegerField(blank=True, null=True)
    short_avg_price = models.IntegerField(blank=True, null=True)
    short_zscale = models.FloatField(blank=True, null=True)
    short_section = models.IntegerField(blank=True, null=True)
    tp_5d_mean = models.FloatField(blank=True, null=True) # short_total_price rolling_mean 5days

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class KosdaqShort(models.Model):
    date = models.CharField(max_length=10)
    code = models.ForeignKey(Ticker,
                             on_delete=models.CASCADE,
                             related_name='kd_short')
    short = models.IntegerField(blank=True, null=True)
    short_proportion = models.FloatField(blank=True, null=True)
    short_total_price = models.IntegerField(blank=True, null=True)
    short_avg_price = models.IntegerField(blank=True, null=True)
    short_zscale = models.FloatField(blank=True, null=True)
    short_section = models.IntegerField(blank=True, null=True)
    tp_5d_mean = models.FloatField(blank=True, null=True) # short_total_price rolling_mean 5days

    def __str__(self):
        return '{} {}'.format(self.code, self.name)
