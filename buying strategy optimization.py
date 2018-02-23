# -*- coding: utf-8 -*-

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
from abupy import AbuFactorBuyBreak, AbuFactorSellBreak
from abupy import AbuFactorAtrNStop
from abupy import ABuPickTimeExecute, AbuBenchmark,AbuCapital
from abupy import AbuFactorPreAtrNStop
from abupy import AbuFactorCloseAtrNStop

buy_factors = [{'xd':60, 'class': AbuFactorBuyBreak},
               {'xd':42,'class': AbuFactorBuyBreak}]

#使用120天向下突破为卖出信号
sell_factor1 ={'xd':120, 'class':AbuFactorSellBreak}
sell_factor2 ={'stop_loss_n': 0.5, 'stop_win_n':40, 'class':AbuFactorAtrNStop}
sell_factor3 ={'class':AbuFactorPreAtrNStop,'pre_atr_n':1.0}
sell_factor4 ={'class':AbuFactorCloseAtrNStop,'close_atr_n':1.5}
#两个卖出因子策略并行同时生效
sell_factors = [sell_factor1, sell_factor2, sell_factor3, sell_factor4]
benchmark = AbuBenchmark()
capital = AbuCapital(10000, benchmark)
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usJNJ'],benchmark,buy_factors,sell_factors,capital,show=True)

