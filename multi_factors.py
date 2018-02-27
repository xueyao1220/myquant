#-*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import abupy

from abupy import AbuDoubleMaBuy, AbuDoubleMaSell, AbuSDBreak, AbuFactorBuyBreak
from abupy import AbuFactorCloseAtrNStop, AbuFactorAtrNStop, AbuFactorPreAtrNStop
from abupy import abu, ABuProgress, AbuMetricsBase, EMarketTargetType
from abupy import AbuFactorSellNDay, AbuFactorBuyWD, AbuFactorSellBreak

buy_factors = [

               {'class': AbuDoubleMaBuy,
                'sell_factors': [{'fast': 5, 'slow': 60,
                                  'class': AbuDoubleMaSell}]},
               {'xd': 42, 'class': AbuFactorBuyBreak,
                'sell_factors': [{'xd': 21,
                                  'class': AbuFactorSellBreak}]},
               {'xd': 21, 'class': AbuSDBreak}]

# 基础卖出因子（止盈止损&风险控制&利润保护）对应所有买入因子生效
sell_factors = [
    {'stop_loss_n': 1.0, 'stop_win_n': 2.0, 'class': AbuFactorAtrNStop},
    {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
    {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
]

us_choice_symbols = ['usSYK', 'usVAR', 'usJNJ', 'usMDT', 'usBSX',
                     'usISRG', 'usCAH', 'usABT']

cash = 1000000

def run_loo_back(choice_symbols, ps =None, n_folds=3,start =None,end = None,only_info = False):
    abu_result_tuple,_ = abu.run_loop_back(cash,buy_factors,sell_factors,ps, start=start,end=end,n_folds=n_folds,choice_symbols=choice_symbols)

    abu_result_tuple.orders_pd['buy_factor'] = abu_result_tuple.orders_pd['buy_factor'].apply(lambda bf:bf.split(':')[0])
    ABuProgress.clear_output()
    metrics = AbuMetricsBase.show_general(*abu_result_tuple,returns_cmp=only_info,only_info=only_info,only_show_returns=True)
    return abu_result_tuple,metrics

abu_result_tuple, metrics = run_loo_back(us_choice_symbols)
metrics.plot_sell_factors()
metrics.plot_buy_factors()
abu_result_tuple.orders_pd.groupby('buy_factor')['sell_type_extra'].value_counts()

