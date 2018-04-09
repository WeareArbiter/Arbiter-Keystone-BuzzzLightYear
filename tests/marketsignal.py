from django.test import TestCase

from marketsignal.models import (
    Index,
    MarketScore,
    # MSHome,
    # RankData,
)


class MarketSignalTestCase(TestCase):
    '''
    MarketSignal DB testing module
    '''

    def setUp(self):
        print('Starting marketsignal test')

        # create Ticker data first, before saving other data
        ticker, created = Ticker.objects.get_or_create(code='005930',
                                                       name='삼성전자',
                                                       market_type='KOSPI',
                                                       state=1)
        # ticker variable for ForeignKey
        self.ticker = ticker


    def test_Index_save(self):
        index_inst, created = Index.object.get_or_create(date='20180101',
                                                         name='L',
                                                         index=100.0,
                                                         volume=100.0,
                                                         category='S')

        self.assertTrue(created, msg='failed to save Index data')
        self.assertEqual(Index.objects.count(), 1, msg='Index data not created properly')

        index_val = Index.object.all().first().index
        self.assertEquat(index_val, 100.0, msg='Index value not correct, check again')


    def test_MarketScore_save(self):
        # create Index instance for one to one relationship with MarketScore
        index_inst, created = Index.object.get_or_create(date='20180101',
                                                         name='L',
                                                         index=100.0,
                                                         volume=100.0,
                                                         category='S')

        specs_inst, created = MarketScore.objects.get_or_create(index=index_inst,
                                                                momentum=100.0,
                                                                volatility=100.0,
                                                                correlation=100.0,
                                                                volume=100,
                                                                momentum_score=90,
                                                                volatility_score=90,
                                                                correlation_score=90,
                                                                volume_score=90,
                                                                total_score=90,
                                                                score_rating='A')
        self.assertTrue(created, msg='failed to save MarketScore data')
        self.assertEqual(MarketScore.objects.count(), 1, msg='MarketScore data not created properly')

        # check if one to one relationship works correctly
        total_score = index_inst.score.total_score
        self.assertEqual(total_score, 90, msg='total score of MarketScore not correct, check again')
