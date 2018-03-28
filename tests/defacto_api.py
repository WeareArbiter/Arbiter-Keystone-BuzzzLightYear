from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from stockapi.models import Ticker
from defacto.models import (
    DefactoReg,
    AgentData,
    AgentCalcData,
    ScoreData,
    RankData,
    )

User = get_user_model()


class DefactoAPITestCase(TestCase):
    '''
    Defacto REST API testing module
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

    def test_AgentData_post_API(self):
        # make Ticker instance first before saving agent data
        ticker_data = {
            'code': '005930',
            'name': '삼성전자',
            'market_type': 'KOSPI',
            'state': 1
        }
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/stock-api/ticker/',
            ticker_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        # retrieving ticker id value for use in connecting Ticker data instance and agent data instance
        code = Ticker.objects.get(code='005930').id
        agent_data = {
            'date':'20180325',
            'code':code,
            'ind_possession':50000000000,
            'for_possession':50000000000,
            'ins_possession':50000000000,
            'cor_possession':50000000000,
            'tru_possession':50000000000,
            'pen_possession':50000000000,
            'circulate_stock':50000000000,
            'ins_purity':0.45,
            'ind_height':0.52,
            'for_height':0.14,
            'ins_height':0.12,
            'cor_height':0.21,
            'ind_proportion':0.12,
            'for_proportion':0.34,
            'ins_proportion':0.23,
            'cor_proportion':0.21,
        }
        response = self.client.post(
            '/defacto-api/agent-data/',
            agent_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # attempt again with authentication
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/defacto-api/agent-data/',
            agent_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_AgentCalcData_post_API(self):
        # make Ticker instance first before saving agent calc data
        ticker_data = {
            'code': '005930',
            'name': '삼성전자',
            'market_type': 'KOSPI',
            'state': 1
        }
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/stock-api/ticker/',
            ticker_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        # retrieving ticker id value for use in connecting Ticker data instance and agent calc data instance
        code = Ticker.objects.get(code='005930').id
        agent_calc_data = {
            'date':'20180325',
            'code':code,
            'ind_tp':50000.999,
            'for_tp':23232.121,
            'ins_tp':10034.123,
            'cor_tp':19302.231,
            'ind_buy_cumsum':53432,
            'for_buy_cumsum':12340,
            'ins_buy_cumsum':30043,
            'cor_buy_cumsum':13040,
            'ind_tp_buy_cumsum':2012121112,
            'for_tp_buy_cumsum':2031212121,
            'ins_tp_buy_cumsum':1232343121,
            'cor_tp_buy_cumsum':1233445212,
            'ind_apps':23131.23,
            'for_apps':34321.34,
            'ins_apps':23213.34,
            'cor_apps':34343.34,
            'lead_agent':'institution',
        }
        response = self.client.post(
            '/defacto-api/calc-data/',
            agent_calc_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/defacto-api/calc-data/',
            agent_calc_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_DefactoReg_post_API(self):
        # make Ticker instance first before saving defacto reg data
        ticker_data = {
            'code': '005930',
            'name': '삼성전자',
            'market_type': 'KOSPI',
            'state': 1
        }
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/stock-api/ticker/',
            ticker_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        # sending post request on defacto reg data without authentication
        code = Ticker.objects.get(code='005930').id
        reg_data = {
            'date':'201803',
            'code':code,
            'ind_tv':2.12,
            'for_tv':1.69,
            'ins_tv':1.95,
            'cor_tv':1.33,
            'ind_coef':1.32,
            'for_coef':3.12,
            'ins_coef':4.32,
            'cor_coef':5.32
        }
        response = self.client.post(
            '/defacto-api/reg-data/',
            reg_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # attempt again with authentication
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/defacto-api/reg-data/',
            reg_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_ScoreData_post_API(self):
        # make Ticker instance first before saving score data
        ticker_data = {
            'code': '005930',
            'name': '삼성전자',
            'market_type': 'KOSPI',
            'state': 1
        }
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/stock-api/ticker/',
            ticker_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        # sending post request on score data without authentication
        code = Ticker.objects.get(code='005930').id
        score_data = {
            'date':'20180327',
            'code':code,
            'absolute_score':27.12,
            'relative_score':51.69,
            'total_score':78.81,
            'score_rank':22,
            'score_change':-2.82,
            'rank_change':-12,
            'lead_agent':'foreigner',
        }
        response = self.client.post(
            '/defacto-api/score-data/',
            score_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # attempt again with authentication
        user = User.objects.get(username='testcase')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/defacto-api/score-data/',
            score_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

def test_RankData_post_API(self):
    # make Ticker instance first before saving rank data
    ticker_data = {
        'code': '005930',
        'name': '삼성전자',
        'market_type': 'KOSPI',
        'state': 1
    }
    user = User.objects.get(username='testcase')
    self.client.force_authenticate(user=user)
    response = self.client.post(
        '/stock-api/ticker/',
        ticker_data,
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.client.logout()
    # sending post request on rank data without authentication
    code = Ticker.objects.get(code='005930').id
    rank_data = {
        'date':'20180327',
        'code':code,
        'lead_agent':'foreigner',
        'total_score':78.81,
        'category':'foreigner_score',
        'rank_change':-12,
        'sign':"plus-line"
    }
    response = self.client.post(
        '/defacto-api/rank-data/',
        rank_data,
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # attempt again with authentication
    user = User.objects.get(username='testcase')
    self.client.force_authenticate(user=user)
    response = self.client.post(
        '/defacto-api/rank-data/',
        rank_data,
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.client.logout()
