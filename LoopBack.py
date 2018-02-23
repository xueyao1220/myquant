#-*- coding: utf8 -*-

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
from abupy import AbuFactorBuyBreak
from abupy import AbuFactorAtrNStop
from abupy import AbuFactorPreAtrNStop
from abupy import AbuFactorCloseAtrNStop
from abupy import abu, ABuProgress
from abupy import AbuMetricsBase

#设置初始资金数
read_cash = 100000

#设置选股因子
stock_pickers = None

#买入因子仍然沿用向上突破因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},{'xd':42, 'class':AbuFactorBuyBreak}]

#卖出因子
sell_factors = [
    {'stop_loss_n': 1.0, 'stop_win_n':3.0, 'class':AbuFactorAtrNStop},
    {'class':AbuFactorPreAtrNStop,'pre_atr_n':1.5},
    {'class': AbuFactorCloseAtrNStop,'close_atr_n':1.5}
]

#择时股票池
choice_symbols = ['usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG',
                  'usTSLA', 'usWUBA', 'usVIPS']
abu_result_tuple, kl_pd_manger = abu.run_loop_back(read_cash,buy_factors,sell_factors,stock_pickers,choice_symbols,n_folds=2)

metrics = AbuMetricsBase(*abu_result_tuple)
metrics.fit_metrics()
# metrics.plot_returns_cmp()
metrics.plot_sharp_volatility_cmp()
metrics.plot_max_draw_down()