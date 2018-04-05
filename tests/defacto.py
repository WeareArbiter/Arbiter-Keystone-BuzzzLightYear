from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from stockapi.models import (
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,)

from defacto.models import (
    KospiAgentData,
    KospiTruePriceData,
    KosdaqAgentData,
    KosdaqTruePriceData,
    KospiAbsoulteScore,
    KosdaqAbsoulteScore,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    KospiRelativeCalc,
    KosdaqRelativeCalc,
    )

User = get_user_model()

class DefactoTestCase(TestCase):
    '''
    Defacto DB testing module
    '''

    def setUp(self):
        print('Starting defacto test')

        # create Ticker data first, before saving other data
        kp_ticker, created = Ticker.objects.get_or_create(code='005930',
                                                             name='삼성전자',
                                                             market_type='KOSPI',
                                                             state=1,)

        kd_ticker, created = Ticker.objects.get_or_create(code='068760',
                                                          name='셀트리온제약',
                                                          market_type='KOSDAQ',
                                                          state=1)

        kp_ohlcv, created = KospiOHLCV.objects.get_or_create(date='20180101',
                                                             code=kp_ticker,
                                                             open_price=1000,
                                                             high_price=1000,
                                                             low_price=1000,
                                                             close_price=1000,
                                                             volume=1000000)

        kd_ohlcv, created = KosdaqOHLCV.objects.get_or_create(date='20180101',
                                                              code=kd_ticker,
                                                              open_price=1000,
                                                              high_price=1000,
                                                              low_price=1000,
                                                              close_price=1000,
                                                              volume=1000000)

        # ticker variable for ForeignKey
        self.kp_ticker = kp_ticker
        self.kd_ticker = kd_ticker

        self.kp_ohlcv = kp_ohlcv
        self.kd_ohlcv = kd_ohlcv

        # test assertions
        self.assertTrue(created, msg='failed to save DefactoTicker data')
        self.assertEqual(Ticker.objects.all().count(), 2, msg='DefactoTicker data not created properly')
        # check if ForeignKey works properly
        kospi_close_price = self.kp_ticker.kp_ohlcv.first().close_price
        kosdaq_close_price = self.kd_ticker.kd_ohlcv.first().close_price
        self.assertEqual(kospi_close_price, 1000, msg='kospi_close_price OHLCV data not created properly')
        self.assertEqual(kosdaq_close_price, 1000, msg='kosdaq_close_price OHLCV data not created properly')


    def test_Ticker_primary_key_is_code(self):
        ticker_saved_count = Ticker.objects.count()
        self.assertEqual(ticker_saved_count, 2, msg='Ticker saved more than one instance')

        kp_ticker_pk = self.kp_ticker.pk
        kd_ticker_pk = self.kd_ticker.pk
        self.assertEqual(kp_ticker_pk, '005930', msg='Ticker primary key not code value of stock')
        self.assertEqual(kd_ticker_pk, '068760', msg='Ticker primary key not code value of stock')


    def test_AgentData_save(self):
        # test all Kospi, Kosdaq model cases
        # 4 models in total: KospiAgentData, KosdaqAgentData, KospiTruePriceData, KospiTruePriceData)

        kospi_agent_data, created = KospiAgentData.objects.get_or_create(ohlcv = self.kp_ohlcv,
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
                                                                         cor_proportion = 0.21,
                                                                         ind_tv = 2.12,
                                                                         for_tv = 1.69,
                                                                         ins_tv = 1.95,
                                                                         cor_tv = 1.33,
                                                                         ind_coef = 1.32,
                                                                         for_coef = 3.12,
                                                                         ins_coef = 4.32,
                                                                         cor_coef = 5.32,)
        self.assertTrue(created, msg='failed to save AgentData')
        kp_ad_inst_name = self.kp_ticker.kp_ohlcv.first().agent_data.ohlcv.code.name
        self.assertEqual(kp_ad_inst_name, '삼성전자', msg='AgentData not created properly')

        kosdaq_agent_data, created = KosdaqAgentData.objects.get_or_create(ohlcv =  self.kd_ohlcv,
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
                                                                           cor_proportion = 0.21,
                                                                           ind_tv = 2.12,
                                                                           for_tv = 1.69,
                                                                           ins_tv = 1.95,
                                                                           cor_tv = 1.33,
                                                                           ind_coef = 1.32,
                                                                           for_coef = 3.12,
                                                                           ins_coef = 4.32,
                                                                           cor_coef = 5.32,)
        self.assertTrue(created, msg='failed to save AgentData')
        kd_ad_inst_name = self.kd_ticker.kd_ohlcv.first().agent_data.ohlcv.code.name
        self.assertEqual(kd_ad_inst_name, '셀트리온제약', msg='AgentData not created properly')

        kospi_tp_data, created = KospiTruePriceData.objects.get_or_create(ohlcv = self.kp_ohlcv,
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
        kp_tp_inst_name = self.kp_ticker.kp_ohlcv.first().true_price.ohlcv.code.name
        self.assertEqual(kp_tp_inst_name, '삼성전자', msg='KOSPI AgentData not created properly')

        kospi_tp_data, created = KosdaqTruePriceData.objects.get_or_create(ohlcv =  self.kd_ohlcv,
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
        kd_tp_inst_name = self.kd_ticker.kd_ohlcv.first().true_price.ohlcv.code.name
        self.assertEqual(kd_tp_inst_name, '셀트리온제약', msg='KOSDAQ AgentData not created properly')

        kp_ad_ins_poss = self.kp_ticker.kp_ohlcv.first().agent_data.ins_possession
        kd_ad_ins_poss = self.kd_ticker.kd_ohlcv.first().agent_data.ins_possession

        kp_tp_ins = self.kp_ticker.kp_ohlcv.first().true_price.ins_tp
        kd_tp_ins = self.kd_ticker.kd_ohlcv.first().true_price.ins_tp

        self.assertEqual(kp_ad_ins_poss, 50000000000, msg='KOSPI agent data not created properly')
        self.assertEqual(kd_ad_ins_poss, 50000000000, msg='KOSDAQ agnet data not created properly')
        self.assertEqual(kp_tp_ins, 10034.123, msg='KOSPI agent calc data not created properly')
        self.assertEqual(kd_tp_ins, 10034.123, msg='KOSDAQ agnet calc data not created properly')

    def test_RelativeCalc_save(self):
        # test all RelativeCalc

        kp_relative_calc, created = KospiRelativeCalc.objects.get_or_create(ohlcv=self.kp_ohlcv,
                                                                            cp_vol = 0.034,
                                                                            cp_vol_section = 1.69,
                                                                            ins_tp_diff = 0.13,
                                                                            for_tp_diff = -1.33,
                                                                            ins_price_inc = 1,
                                                                            for_price_inc = 6,
                                                                            cp_ind = 0.012,
                                                                            cp_for = 0.01,
                                                                            cp_ins = 0.002,
                                                                            cp_cor = 0.004,
                                                                            cp_ind_section = 2,
                                                                            cp_for_section = 5,
                                                                            cp_ins_section = 12,
                                                                            cp_cor_section = 11,)

        self.assertTrue(created, msg='failed to save AgentData')
        kp_rc_inst_name = self.kp_ticker.kp_ohlcv.first().relative_calc.ohlcv.code.name
        self.assertEqual(kp_rc_inst_name, '삼성전자', msg='relative calc not created properly')

        kd_relative_calc, created = KosdaqRelativeCalc.objects.get_or_create(ohlcv=self.kd_ohlcv,
                                                                            cp_vol = 0.034,
                                                                            cp_vol_section = 1.69,
                                                                            ins_tp_diff = 0.13,
                                                                            for_tp_diff = -1.33,
                                                                            ins_price_inc = 1,
                                                                            for_price_inc = 6,
                                                                            cp_ind = 0.012,
                                                                            cp_for = 0.01,
                                                                            cp_ins = 0.002,
                                                                            cp_cor = 0.004,
                                                                            cp_ind_section = 2,
                                                                            cp_for_section = 5,
                                                                            cp_ins_section = 12,
                                                                            cp_cor_section = 11,)

        self.assertTrue(created, msg='failed to save AgentData')
        kd_rc_inst_name = self.kd_ticker.kd_ohlcv.first().relative_calc.ohlcv.code.name
        self.assertEqual(kd_rc_inst_name, '셀트리온제약', msg='relative calc not created properly')

        kp_rc_cp_vol = self.kp_ticker.kp_ohlcv.first().relative_calc.cp_vol
        self.assertEqual(kp_rc_cp_vol, 0.034, msg='defacto_reg_ind_tv DefactoReg not created properly')
        kd_rc_cp_vol = self.kd_ticker.kd_ohlcv.first().relative_calc.cp_vol
        self.assertEqual(kd_rc_cp_vol, 0.034, msg='defacto_reg_ind_tv DefactoReg not created properly')


    def test_AbsoliteScore_save(self):

        kp_agent_data, created = KospiAgentData.objects.get_or_create(ohlcv = self.kp_ohlcv,
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
                                                                     cor_proportion = 0.21,
                                                                     ind_tv = 2.12,
                                                                     for_tv = 1.69,
                                                                     ins_tv = 1.95,
                                                                     cor_tv = 1.33,
                                                                     ind_coef = 1.32,
                                                                     for_coef = 3.12,
                                                                     ins_coef = 4.32,
                                                                     cor_coef = 5.32,)
        self.assertTrue(created, msg='failed to save AgentData')
        kp_ad_inst_name = self.kp_ticker.kp_ohlcv.first().agent_data.ohlcv.code.name
        self.assertEqual(kp_ad_inst_name, '삼성전자', msg='AgentData not created properly')

        kd_agent_data, created = KosdaqAgentData.objects.get_or_create(ohlcv =  self.kd_ohlcv,
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
                                                                       cor_proportion = 0.21,
                                                                       ind_tv = 2.12,
                                                                       for_tv = 1.69,
                                                                       ins_tv = 1.95,
                                                                       cor_tv = 1.33,
                                                                       ind_coef = 1.32,
                                                                       for_coef = 3.12,
                                                                       ins_coef = 4.32,
                                                                       cor_coef = 5.32,)
        self.assertTrue(created, msg='failed to save AgentData')
        kd_ad_inst_name = self.kd_ticker.kd_ohlcv.first().agent_data.ohlcv.code.name
        self.assertEqual(kd_ad_inst_name, '셀트리온제약', msg='AgentData not created properly')

        kp_ab_score, created = KospiAbsoulteScore.objects.get_or_create(defacto = kp_agent_data,
                                                                        ind_height_section = 1,
                                                                        for_height_section = 3,
                                                                        ins_height_section = 2,
                                                                        cor_height_section = 4,
                                                                        ind_proporion_section = 4,
                                                                        for_proporion_section = 1,
                                                                        ins_proporion_section = 2,
                                                                        cor_proporion_section = 3,
                                                                        ins_purity_weight = 0.75,
                                                                        ind_tv_section = 2,
                                                                        for_tv_section = 1.5,
                                                                        ins_tv_section = 1,
                                                                        cor_tv_section = 0.5,
                                                                        ind_coef_section = 1,
                                                                        for_coef_section = 1.5,
                                                                        ins_coef_section = 2,
                                                                        cor_coef_section = 0.5,
                                                                        ind_ab_score = 8,
                                                                        for_ab_score = 7,
                                                                        ins_ab_score = 5.25,
                                                                        cor_ab_score = 8,
                                                                        absolute_score = 28.25,
                                                                        lead_agent = 'None',)

        self.assertTrue(created, msg='failed to save AgentData')
        kp_ad_inst_name = self.kp_ticker.kp_ohlcv.agent_data.first().absolute_score.defacto.ohlcv.code.name
        self.assertEqual(kp_ad_inst_name, '삼성전자', msg='AgentData not created properly')

        kd_ab_score, created = KospiAbsoulteScore.objects.get_or_create(defacto = kd_agent_data,
                                                                        ind_height_section = 1,
                                                                        for_height_section = 3,
                                                                        ins_height_section = 2,
                                                                        cor_height_section = 4,
                                                                        ind_proporion_section = 4,
                                                                        for_proporion_section = 1,
                                                                        ins_proporion_section = 2,
                                                                        cor_proporion_section = 3,
                                                                        ins_purity_weight = 0.75,
                                                                        ind_tv_section = 2,
                                                                        for_tv_section = 1.5,
                                                                        ins_tv_section = 1,
                                                                        cor_tv_section = 0.5,
                                                                        ind_coef_section = 1,
                                                                        for_coef_section = 1.5,
                                                                        ins_coef_section = 2,
                                                                        cor_coef_section = 0.5,
                                                                        ind_ab_score = 8,
                                                                        for_ab_score = 7,
                                                                        ins_ab_score = 5.25,
                                                                        cor_ab_score = 8,
                                                                        absolute_score = 28.25,
                                                                        lead_agent = 'None',)

        self.assertTrue(created, msg='failed to save AgentData')
        kd_ad_inst_name = self.kd_ticker.kd_ohlcv.agent_data.first().absolute_score.defacto.ohlcv.code.name
        self.assertEqual(kd_ad_inst_name, '셀트리온제약', msg='AgentData not created properly')




    def test_ScoreData_save(self):
        # test score data
        kp_score_data, created = KospiScoreData.objects.get_or_create(ohlcv = self.kp_ohlcv,
                                                                     absolute_score = 27.12,
                                                                     relative_score = 51.69,
                                                                     total_score = 78.81,
                                                                     score_rank = 22,
                                                                     score_change = -2.82,
                                                                     rank_change = -12,
                                                                     lead_agent = 'foreigner',)
        self.assertTrue(created, msg='failed to save AgentData')
        kp_sd_inst_name = self.kp_ticker.kp_ohlcv.first().score_data.ohlcv.code.name
        self.assertEqual(kp_sd_inst_name, '삼성전자', msg='ScoreData not created properly')

        kd_score_data, created = KosdaqScoreData.objects.get_or_create(ohlcv = self.kd_ohlcv,
                                                                       absolute_score = 27.12,
                                                                       relative_score = 51.69,
                                                                       total_score = 78.81,
                                                                       score_rank = 22,
                                                                       score_change = -2.82,
                                                                       rank_change = -12,
                                                                       lead_agent = 'foreigner',)

        self.assertTrue(created, msg='failed to save AgentData')
        kd_sd_inst_name = self.kd_ticker.kd_ohlcv.first().score_data.ohlcv.code.name
        self.assertEqual(kd_sd_inst_name, '셀트리온제약', msg='ScoreData not created properly')

        kp_score_data_ab_score = self.kp_ticker.kp_ohlcv.first().score_data.absolute_score
        self.assertEqual(kp_score_data_ab_score, 27.12, msg='score_data_ab_score ScoreData not created properly')
        kd_score_data_ab_score = self.kd_ticker.kd_ohlcv.first().score_data.absolute_score
        self.assertEqual(kd_score_data_ab_score, 27.12, msg='score_data_ab_score ScoreData not created properly')

    def test_RankData_save(self):
        # test rank data
        rank_data, created = RankData.objects.get_or_create(date = '20180327',
                                                            code = self.kp_ticker,
                                                            lead_agent='foreigner',
                                                            total_score = 78.81,
                                                            category = 'foreigner_score',
                                                            rank_change = -12,
                                                            sign = "plus-line")
        self.assertTrue(created, msg='failed to save AgentData')
        inst_name = rank_data.code.name
        self.assertEqual(inst_name, '삼성전자', msg='RankData not created properly')
        rank_data_lead_agent = self.kp_ticker.rank_data.first().lead_agent
        self.assertEqual(rank_data_lead_agent, 'foreigner', msg='rank_data_lead_agent RankData not created properly')
