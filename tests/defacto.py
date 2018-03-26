from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from defacto.models import (
    DefactoTicker,
    DefactoReg,
    AgentData,
    AgentCalcData,
    ScoreData,
    RankData,
    )

User = get_user_model()

class DefactoTestCase(TestCase):
    '''
    Defacto DB testing module
    '''

    def setUp(self):
        print('Starting defacto test')

        # create Ticker data first, before saving other data
        ticker, created = DefactoTicker.objects.get_or_create(code='005930',
                                                             name='삼성전자',
                                                             market_type='KOSPI',
                                                             state=1,)
        # ticker variable for ForeignKey
        self.ticker = ticker

        # test assertions
        self.assertTrue(created, msg='failed to save DefactoTicker data')
        self.assertEqual(DefactoTicker.objects.all().count(), 1, msg='DefactoTicker data not created properly')

    def test_AgentData_save(self):
        # test all agent data
        agent_data, created = AgentData.objects.get_or_create(date = '20180325',
                                                              code = self.ticker,
                                                              ind_possession = 50000000000,
                                                              for_possession = 50000000000,
                                                              ins_possession = 50000000000,
                                                              cor_possession = 50000000000,
                                                              tru_possession = 50000000000,
                                                              pen_possession = 50000000000,
                                                              circulate_stock = 50000000000,
                                                              ins_purity = 0.45,
                                                              ind_height = 0.52,
                                                              for_height = 0.14,
                                                              ins_height = 0.12,
                                                              cor_height = 0.21,
                                                              ind_proportion = 0.12,
                                                              for_proportion = 0.34,
                                                              ins_proportion = 0.23,
                                                              cor_proportion = 0.21,)
        self.assertTrue(created, msg='failed to save AgentData')
        inst_name = agent_data.code.name
        self.assertEqual(inst_name, '삼성전자', msg='AgentData not created properly')

        agent_calc_data, created = AgentCalcData.objects.get_or_create(date = '20180325',
                                                                       code = self.ticker,
                                                                       ind_tp = 50000.999,
                                                                       for_tp = 23232.121,
                                                                       ins_tp = 10034.123,
                                                                       cor_tp = 19302.231,
                                                                       ind_buy_cumsum = 53432,
                                                                       for_buy_cumsum = 12340,
                                                                       ins_buy_cumsum = 30043,
                                                                       cor_buy_cumsum = 13040,
                                                                       ind_tp_buy_cumsum = 2012121112,
                                                                       for_tp_buy_cumsum = 2031212121,
                                                                       ins_tp_buy_cumsum = 1232343121,
                                                                       cor_tp_buy_cumsum = 1233445212,
                                                                       ind_apps = 23131.23,
                                                                       for_apps = 34321.34,
                                                                       ins_apps = 23213.34,
                                                                       cor_apps = 34343.34,)
        self.assertTrue(created, msg='failed to save AgentData')
        inst_name = agent_calc_data.code.name
        self.assertEqual(inst_name, '삼성전자', msg='AgentData not created properly')
        agent_data_ind_possession = self.ticker.agent_data.first().ind_possession
        self.assertEqual(agent_data_ind_possession, 50000000000, msg='agent_data_ind_poss AgentData not created properly')
        agent_calc_data_ind_tp = self.ticker.agent_calc_data.first().ind_tp
        self.assertEqual(agent_calc_data_ind_tp, 50000.999, msg='agent_calc_data_ind_tp AgentCalcData not created properly')

    def test_DefactoReg_save(self):
        # test all DefactoReg
        defacto_reg, created = DefactoReg.objects.get_or_create(date = '201803',
                                                               code = self.ticker,
                                                               ind_tv = 2.12,
                                                               for_tv = 1.69,
                                                               ins_tv = 1.95,
                                                               cor_tv = 1.33,
                                                               ind_coef = 1.32,
                                                               for_coef = 3.12,
                                                               ins_coef = 4.32,
                                                               cor_coef = 5.32,)
        self.assertTrue(created, msg='failed to save AgentData')
        inst_name = defacto_reg.code.name
        self.assertEqual(inst_name, '삼성전자', msg='DefatoReg not created properly')
        defacto_reg_ind_tv = self.ticker.defacto_reg.first().ind_tv
        self.assertEqual(defacto_reg_ind_tv, 2.12, msg='defacto_reg_ind_tv DefactoReg not created properly')

    def test_ScoreData_save(self):
        # test score data
        score_data, created = ScoreData.objects.get_or_create(date = '20180327',
                                                              code = self.ticker,
                                                              absolute_score = 27.12,
                                                              relative_score = 51.69,
                                                              total_score = 78.81,
                                                              score_rank = 22,
                                                              score_change = -2.82,
                                                              rank_change = -12,
                                                              lead_agent = 'foreigner',)
        self.assertTrue(created, msg='failed to save AgentData')
        inst_name = score_data.code.name
        self.assertEqual(inst_name, '삼성전자', msg='ScoreData not created properly')
        score_data_ab_score = self.ticker.score_data.first().absolute_score
        self.assertEqual(score_data_ab_score, 27.12, msg='score_data_ab_score ScoreData not created properly')

    def test_RankData_save(self):
        # test rank data
        rank_data, created = RankData.objects.get_or_create(date = '20180327',
                                                            code = self.ticker,
                                                            lead_agent='foreigner',
                                                            total_score = 78.81,
                                                            category = 'foreigner_score',
                                                            rank_change = -12,
                                                            sign = "plus-line")
        self.assertTrue(created, msg='failed to save AgentData')
        inst_name = rank_data.code.name
        self.assertEqual(inst_name, '삼성전자', msg='RankData not created properly')
        rank_data_lead_agent = self.ticker.rank_data.first().lead_agent
        self.assertEqual(rank_data_lead_agent, 'foreigner', msg='rank_data_lead_agent RankData not created properly')
