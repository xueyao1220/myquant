#-*-coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys

sys.path.insert(0, os.path.abspath('/home/yao/IdeaProjects/abu'))

import abupy
from abupy import AbuFactorBuyBreak,AbuFactorSellBreak
from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop
from abupy import ABuPickTimeExecute, AbuBenchmark, AbuCapital
from abupy import AbuSlippageBuyBase, slippage
from abupy import AbuMetricsBase,AbuPositionBase,AbuKellyPosition

buy_factors = [{'xd':60,'class': AbuFactorBuyBreak},{'xd':42, 'class':AbuFactorBuyBreak}]

sell_factors = [
    {
        'xd':120,
        'class': AbuFactorSellBreak
    },
    {
        'stop_loss_n':0.5,
        'stop_win_n':3.0,
        'class':AbuFactorAtrNStop
    },
    {
        'class':AbuFactorPreAtrNStop,
        'pre_atr_n':1.0
    },
    {
        'class': AbuFactorCloseAtrNStop,
        'close_atr_n':1.5
    }]

benchmark = AbuBenchmark()
capital = AbuCapital(100000,benchmark)
g_open_down_rate =0.02

#我们假定choice_symbols是我们选股模块的结果
choice_symbols = ['usTSLA', 'usNOAH', 'usSFUN', 'usBIDU', 'usAAPL',
                  'usGOOG', 'usWUBA', 'usVIPS']

#
# class AbuSlippageBuyMean2(AbuSlippageBuyBase):
#
#     @slippage.sbb.slippage_limit_up
#     def fit_price(self):
#
#         if self.kl_pd_buy.pre_close == 0 or (self.kl_pd_buy.open/self.kl_pd_buy.pre_close)<(1-g_open_down_rate):
#             return np.inf
#
#         self.buy_price = np.mean([self.kl_pd_buy['high'],self.kl_pd_buy['low']])
#         return self.buy_price

#buy_factors2 = [{'slippage': AbuSlippageBuyMean2, 'xd':60,'class':AbuFactorBuyBreak},{'xd':42,'class':AbuFactorBuyBreak}]

orders_pd, action_pd,_ =ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,benchmark,buy_factors,sell_factors,capital,show=False)
metrics = AbuMetricsBase(orders_pd, action_pd,capital,benchmark)
metrics.fit_metrics()
metrics.plot_returns_cmp(only_show_returns= True)

# class AbuKellyPosition(AbuPositionBase):
#     def fit_positon(self,factor_object):
#         #败率
#         loss_rate = 1-self.win_rate
#         kelly_pos = self.win_rate - loss_rate/(self.gains_mean/self.losses_mean)
#         kelly_pos = self.pos_max if kelly_pos> self.pos_max else kelly_pos
#
#     def __init__(self, **kwargs):
#
#         #默认kelly 仓位胜率0.50
#         self.win_rate = kwargs.pop('win_rate', 0.50)
#
#         #默认平均获利期望0.10
#         self.gains_mean = kwargs.pop('gains_mean',0.1)
#
#         #默认平均亏损期望0.05
#         self.losses_mean = kwargs.pop('losses_mean',0.05)

buy_factors2 = [{'xd':60,'class':AbuFactorBuyBreak},{'xd':42, 'position':{'class':AbuKellyPosition, 'win_rate': metrics.win_rate,'gain_mean': metrics.gains_mean,'losses_mean': -metrics.losses_mean},'class': AbuFactorBuyBreak}]

capital = AbuCapital(1000000, benchmark)
orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,
                                                                                            benchmark,
                                                                                            buy_factors2,
                                                                                            sell_factors,
                                                                                            capital,
                                                                                            show=False)
print(orders_pd[:10].filter(['symbol','buy_cnt','buy_factor','buy_pos']))
metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark)
metrics.fit_metrics()
metrics.plot_returns_cmp(only_show_returns=True)