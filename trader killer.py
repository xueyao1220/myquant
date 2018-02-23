# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_context(rc={'figure.figsize': (14,7)})
figsize_me = figsize =(14,7)

import os
import sys
sys.path.insert(0, os.path.abspath('/home/yao/IdeaProjects/abu'))

import abupy


from abupy import AbuFactorBuyBreak
from abupy import AbuBenchmark
from abupy import AbuPickTimeWorker
from abupy import AbuCapital
from abupy import AbuKLManager
from abupy import ABuTradeProxy
from abupy import ABuTradeExecute

#buy_factors 60日向上突破，42日向上突破两个因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
               {'xd': 42, 'class': AbuFactorBuyBreak}]
benchmark = AbuBenchmark()

# define the start capital

capital = AbuCapital(1000000, benchmark)
kl_pd_manager = AbuKLManager(benchmark, capital)
# 获取TSLA的交易数据
kl_pd = kl_pd_manager.get_pick_time_kl_pd('usTSLA')
abu_worker = AbuPickTimeWorker(capital, kl_pd, benchmark, buy_factors, None)


orders_pd, action_pd, _ = ABuTradeProxy.trade_summary(abu_worker.orders, kl_pd, draw=False)
exit()
ABuTradeExecute.apply_action_to_capital(capital, action_pd, kl_pd_manager)
capital.capital_pd.capital_blance.plot()

