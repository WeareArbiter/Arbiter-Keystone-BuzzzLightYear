from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import Profile
from stockapi.models import Ticker
from portfolio.models import Portfolio, PortfolioItem
User = get_user_model()


class PortfolioAPITestCase(TestCase):
    '''
    portfolio REST API testing module
    '''

    def setUp(self):
        print('Starting portfolio API test')

        ticker, created = Ticker.objects.get_or_create(code='005930',
                                                       name='삼성전자',
                                                       market_type='KOSPI',
                                                       state=1)
        self.ticker = ticker
        self.client = APIClient()

        # create new user to send post requests
        self.user = {
            'username': 'testcase',
            'email': 'test@gmail.com',
            'password': 'test123123123'
        }
        response = self.client.post(
            '/api/user/',
            self.user,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check created user specs
        self.assertEqual(User.objects.first().username, self.user['username'])
        self.assertEqual(User.objects.first().email, self.user['email'])


    def test_Portfolio_post_API(self):
        user = User.objects.get(username='testcase')
        profile = Profile.objects.get(user=user).user.username
        portfolio_data = {
            'user': profile,
            'name':'etf-optimize',
            'capital': 1000000,
            'high_price': 1000000,
            'portfolio': 'CS',
            'description': 'Greate Moderate',
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/portfolio-api/portfolio/',
            portfolio_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Portfolio_item_post_API(self):
        user = User.objects.get(username='testcase')
        code =self.ticker.code
        profile = Profile.objects.get(user=user).user.username

        portfolio_data = {
            'user': profile,
            'name':'etf-optimize',
            'capital': 1000000,
            'portfolio_type': 'CS',
            'description': 'Greate Moderate',
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/portfolio-api/portfolio/',
            portfolio_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        portfolio = Portfolio.objects.get(user=profile).id
        portfolio_item_data = {
            'portfolio': portfolio,
            'date':'20180411',
            'code': code,
            'status': 'B',
            'quantity': 100000,
            'price': 100000,
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/portfolio-api/item/',
            portfolio_item_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
