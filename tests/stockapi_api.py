from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from stockapi.models import (
    BM,
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    RecentKospiOHLCV,
    RecentKosdaqOHLCV,
    Info,
    Specs,
    Financial,
    FinancialRatio,
    QuarterFinancial,
    KospiBuy,
    KosdaqBuy,
    ETFBuy,
    KospiSell,
    KosdaqSell,
    ETFSell,
    KospiNet,
    KosdaqNet,
    ETFNet,
)

User = get_user_model()


class StockapiAPITestCase(TestCase):
    '''
    Stockapi REST API testing module
    '''

    def setUp(self):
        print('Starting stockapi API test')
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
        self.assertEqual(User.objects.get(pk=1).username, self.user['username'])
        self.assertEqual(User.objects.get(pk=1).email, self.user['email'])

    def test_BM_post_API(self):
        # user, created = User.objects.get_or_create(username='testcase', password='test123123123')
        bm_data = {
            'date': '20180101',
            'name': 'KOSPI',
            'index': 2500,
            'volume': 1000000,
            'individual': 5000,
            'foreigner': 5000,
            'institution': 5000
        }
        response = self.client.post(
            '/stock-api/bm/',
            bm_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
