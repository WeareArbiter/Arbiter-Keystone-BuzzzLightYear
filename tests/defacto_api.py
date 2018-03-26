# from django.contrib.auth import get_user_model
# from django.test import TestCase
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from defacto.models import (
#     DefacoTicker,
#     DefacoReg,
#     AgentData,
#     AgentCalcData,
#     ScoreData,
#     RankData,
#     )
#
# User = get_user_model()
#
#
# class DefactoAPITestCase(TestCase):
#     '''
#     Defacto REST API testing module
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
#     def test_AgentData_post_API(self):
#         # sending post request on BM without authentication
#         agent_data = {
#             'date' = '20180325',
#             'code' = self.ticker,
#             'ind_possession' = 50000000000,
#             'for_possession' = 50000000000,
#             'ins_possession' = 50000000000,
#             'cor_possession' = 50000000000,
#             'tru_possession' = 50000000000,
#             'pen_possession' = 50000000000,
#             'circulate_stock' = 50000000000,
#             'ins_purity' = 0.45,
#             'ind_height' = 0.52,
#             'for_height' = 0.14,
#             'ins_height' = 0.12,
#             'cor_height' = 0.21,
#             'ind_proportion' = 0.12,
#             'for_proportion' = 0.34,
#             'ins_proportion' = 0.23,
#             'cor_proportion' = 0.21,
#         }
#         response = self.client.post(
#             '/defacto-api/agent-data/',
#             agent_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # attempt again with authentication
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/defacto-api/agent-data/',
#             agent_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_AgentCalcData_post_API(self):
#         # sending post request on AgentCalcData without authentication
#         agent_calc_data = {
#             'date' = '20180325',
#             'code' = self.ticker,
#             'ind_tp' = 50000.999,
#             'for_tp' = 23232.121,
#             'ins_tp' = 10034.123,
#             'cor_tp' = 19302.231,
#             'ind_buy_cumsum' = 53432
#             'for_buy_cumsum' = 12340,
#             'ins_buy_cumsum' = 30043,
#             'cor_buy_cumsum' = 13040,
#             'ind_tp_buy_cumsum' = 2012121112,
#             'for_tp_buy_cumsum' = 2031212121,
#             'ins_tp_buy_cumsum' = 1232343121,
#             'cor_tp_buy_cumsum' = 1233445212,
#             'ind_apps' = 23131.23,
#             'for_apps' = 34321.34,
#             'ins_apps' = 23213.34,
#             'cor_apps' = 34343.34,
#         }
#         response = self.client.post(
#             '/defacto-api/calc-data/',
#             agent_calc_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # attempt again with authentication
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/defacto-api/agent-calc-data/',
#             agent_calc_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_DefactoReg_post_API(self):
#         # sending post request on AgentCalcData without authentication
#         reg_data = {
#             'date' = 201803
#             'code' = self.ticker,
#             'ind_tv' = 2.12,
#             'for_tv' = 1.69,
#             'ins_tv' = 1.95,
#             'cor_tv' = 1.33,
#             'ind_coef' = 1.32,
#             'for_coef' = 3.12,
#             'ins_coef' = 4.32,
#             'cor_coef' = 5.32
#         }
#         response = self.client.post(
#             '/defacto-api/Reg-data/',
#             reg_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # attempt again with authentication
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/defacto-api/Reg-data/',
#             reg_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_DefactoReg_post_API(self):
#         # sending post request on AgentCalcData without authentication
#         reg_data = {
#             'date' = 201803
#             'code' = self.ticker,
#             'ind_tv' = 2.12,
#             'for_tv' = 1.69,
#             'ins_tv' = 1.95,
#             'cor_tv' = 1.33,
#             'ind_coef' = 1.32,
#             'for_coef' = 3.12,
#             'ins_coef' = 4.32,
#             'cor_coef' = 5.32
#         }
#         response = self.client.post(
#             '/defacto-api/Reg-data/',
#             reg_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # attempt again with authentication
#         user = User.objects.get(username='testcase')
#         self.client.force_authenticate(user=user)
#         response = self.client.post(
#             '/defacto-api/Reg-data/',
#             reg_data,
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
