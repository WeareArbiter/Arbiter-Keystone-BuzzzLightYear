from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from stockapi.models import Ticker
from portfolio.models import (
    Portfolio,
    PortfolioItem,
    PortfolioSpecs,
    )
User = get_user_model()


class PortfolioTestCase(TestCase):
    '''
    protfolio DB testing module
    '''

    def setUp(self):
        print('Starting portfolio db test')
        user, user_created = User.objects.get_or_create(username='test',
                                                        email="test@gmail.com")

        ticker, ticker_created = Ticker.objects.get_or_create(code='005930',
                                                              name='삼성전자',
                                                              market_type='KOSPI',
                                                              state=1)
        self.new_user = user
        self.ticker = ticker
        # test assertions
        self.assertTrue(user_created, msg='failed to save user data')
        self.assertTrue(ticker_created, msg='failed to save ticker data')
        self.assertEqual(User.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(Ticker.objects.all().count(), 1, msg='ticker data not created properly')
        # check if ForeignKey works properly


    def test_Portfolio_save(self):
        # test Portfolio models cases
        portfolio, p_created = Portfolio.objects.get_or_create(user = self.new_user.profile,
                                                               name = 'etf-optimize',
                                                               capital = 10000000,
                                                               portfolio_type = 'S',
                                                               description = 'Greate Moderate')
        self.portfolio = portfolio
        portfolio_item, i_created = PortfolioItem.objects.get_or_create(portfolio = self.portfolio,
                                                                        date = '20180411',
                                                                        code = self.ticker,
                                                                        status = 'B',
                                                                        quantity = 1000,
                                                                        price = 2000000)

        portfolio_spec, s_created = PortfolioSpecs.objects.get_or_create(portfolio = self.portfolio,
                                                                         date = '20180411',
                                                                         portfolio_ratio = {'삼성전자':200000, 'LG전자':25000},
                                                                         ret = 50.4,
                                                                         avg_ret = 10,
                                                                         avg_vol = 5,
                                                                         sharp_ratio = 1,
                                                                         w_ret = 24.5,
                                                                         m_ret = 10.5,
                                                                         q_ret = 5,5,
                                                                         h_ret = 4.5,
                                                                         y_ret = 14,
                                                                         kp_w_ret = 2.4,
                                                                         kp_m_ret = -2.5,
                                                                         kp_q_ret = 4.1,
                                                                         kp_h_ret = -1.4,
                                                                         kp_y_ret = 2.4)

        self.assertTrue(p_created, msg='failed to save portfolio data')
        self.assertTrue(i_created, msg='failed to save portfolio_item data')
        self.assertTrue(s_created, msg='failed to save portfolio_item data')

        portfolio_inst = self.new_user.profile.portfolio.first().name
        portfolio_item_inst = self.new_user.profile.portfolio.first().item.first().code.code
        portfolio_specs_inst = self.new_user.pofile.portfolio.first().portfolio_ret.code.name

        self.assertEqual(portfolio_inst, 'etf-optimize', msg='portfolio not created properly')
        self.assertEqual(portfolio_item_inst, '005930', msg='portfolio_item data not created properly')
        self.assertEqual(portfolio_specs_inst, '삼성전자', msg='portfolio_spec data not created properly')
