# from django.contrib.auth import get_user_model
# from django.test import TestCase
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from stockapi.models import (
#     Benchmark,
#     Ticker,
#     KospiOHLCV,
#     KosdaqOHLCV,
#     RecentKospiOHLCV,
#     RecentKosdaqOHLCV,
#     Info,
#     Specs,
#     Financial,
#     FinancialRatio,
#     QuarterFinancial,
#     KospiBuy,
#     KosdaqBuy,
#     KospiSell,
#     KosdaqSell,
#     KospiNet,
#     KosdaqNet,
# )
#
# User = get_user_model()
#
#
# class StockapiAPITestCase(TestCase):
#     '''
#     Stockapi REST API testing module
#     '''
#
#     def setUp(self):
#         print('Starting stockapi API test')
#         self.client = APIClient()
#
#         # create new user to send post requests
#         self.user = {
#             'username': 'testcase',
#             'email': 'test@gmail.com',
#             'password': 'test123123123'
#         }
#         response = self.client.post(
#             '/api/user/',
#             self.user,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # check created user specs
#         self.assertEqual(User.objects.get(pk=1).username, self.user['username'])
#         self.assertEqual(User.objects.get(pk=1).email, self.user['email'])
#
#     def test_BM_post_API(self):
#         # sending post request on BM without authentication
#         bm_data = {
#             'date': '20180101',
#             'name': 'KOSPI',
#             'index': 2500,
#             'volume': 1000000,
#             'individual': 5000,
#             'foreigner': 5000,
#             'institution': 5000
#         }
#         response = self.client.post(
#             '/stock-api/bm/',
#             bm_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # attempt again with authentication
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/stock-api/bm/',
#             bm_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # logging out for other test cases
#         self.client.logout()
#
#     def test_Ticker_post_API(self):
#         # sending post request on BM without authentication
#         ticker_data = {
#             'code': '005930',
#             'name': '삼성전자',
#             'market_type': 'KOSPI',
#             'state': 1
#         }
#         response = self.client.post(
#             '/stock-api/ticker/',
#             ticker_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # attempt again with authentication
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/stock-api/ticker/',
#             ticker_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # logging out for other test cases
#         self.client.logout()
#
#     def test_OHLCV_post_API(self):
#         # make Ticker instance first before saving OHLCV data
#         ticker_data = {
#             'code': '005930',
#             'name': '삼성전자',
#             'market_type': 'KOSPI',
#             'state': 1
#         }
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/stock-api/ticker/',
#             ticker_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # retrieving ticker id value for use in connecting Ticker data instance and OHLCV data instance
#         code = Ticker.objects.get(code='005930').id
#         ohlcv_data = {
#             'date': '20000101',
#             'code': code,
#             'open_price': 1000000,
#             'high_price': 1000000,
#             'low_price': 1000000,
#             'close_price': 1000000,
#             'volume': 1000000
#         }
#         response = self.client.post(
#             '/stock-api/kospi/',
#             ohlcv_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
