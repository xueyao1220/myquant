#-*- coding:UTF-8 -*-

from __future__ import print_function
from __future__ import division

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_context(rc={'figure.figsize': (14,7)})
figsize_me = figsize = (14,7)

import os
import sys
import abupy

from abupy import AbuFactorBuyBreak
from abupy import AbuBenchmark
from abupy import AbuPickTimeWorker
from abupy import AbuCapital
from abupy import AbuKLManager
from abupy import ABuTradeProxy
from abupy import ABuPickTimeExecute
from abupy import AbuFactorSellBreak
from abupy import AbuFactorAtrNStop
from abupy import AbuFactorPreAtrNStop
from abupy import AbuMetricsBase
from abupy import AbuFactorCloseAtrNStop

#设置买入点
buy_factors = [{'xd':60, 'class':AbuFactorBuyBreak},
               {'xd':42, 'class': AbuFactorBuyBreak}]

#设置卖出点
sell_factor1 = {'xd': 120, 'class': AbuFactorSellBreak}

#设置趋势止盈和止损
sell_factor2 = {'stop_loss_n':0.5, 'stop_win_n':3.0, 'class':AbuFactorAtrNStop}

#设置暴跌止损因子
sell_factor3 = {'pre_atr_n':1.0, 'class':AbuFactorPreAtrNStop}

#设置保护止盈因子组成dict
sell_factor4 = {'close_atr_n':1.5,'class': AbuFactorCloseAtrNStop}


sell_factors = [sell_factor1, sell_factor2, sell_factor3,sell_factor4]

benchmark = AbuBenchmark()

choice_symbols = ['usTSLA', 'usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG', 'usWUBA', 'usVIPS']


capital = AbuCapital(1000000, benchmark)
kl_pd_manager = AbuKLManager(benchmark,capital)


#orders_pd, action_pd, _ = ABuTradeProxy.trade_summary(abu_worker.orders, kl_pd, draw=True)
#orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols, benchmark, buy_factors, sell_factors, capital, show=False)

orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usAAPL'],
                                                                            benchmark,
                                                                            buy_factors,
                                                                            sell_factors,
                                                                            capital, show=True)

orders_pd[:10].filter(['symbol', 'buy_price', 'buy_cnt', 'buy_factor', 'buy_pos',
                       'sell_date', 'sell_type_extra', 'sell_type', 'profit'])

print(action_pd[:10])

metrics = AbuMetricsBase(orders_pd,action_pd,capital,benchmark)
metrics.fit_metrics()
metrics.plot_returns_cmp(only_show_returns=True)
