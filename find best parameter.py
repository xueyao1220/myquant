# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import division

import warnings
warnings.simplefilter('ignore')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets

import os
import sys

sys.path.insert(0,os.path.abspath('/home/yao/IdeaProjects/abu'))
import abupy

from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop, AbuFactorBuyBreak
from abupy import abu, ABuFileUtil, ABuGridHelper,GridSearch, AbuBlockProgress,ABuProgress
from abupy import AbuMetricsBase

stop_win_range = np.arange(2.0,4.5,0.5)
stop_loss_range = np.arange(0.5,2,0.5)

sell_atr_nstop_factor_grid = {
    'class':[AbuFactorAtrNStop],
    'stop_loss_n': stop_loss_range,
    'stop_win_n': stop_win_range
}

close_atr_range =np.arange(1.0,4.0,0.5)
pre_atr_range = np.arange(1.0,3.5,0.5)

sell_atr_pre_factor_grid = {
    'class':[AbuFactorPreAtrNStop],
    'pre_atr_n': pre_atr_range
}

sell_atr_close_factor_grid ={
    'class':[AbuFactorCloseAtrNStop],
    'close_atr_n': close_atr_range
}

sell_factors_product = ABuGridHelper.gen_factor_grid(
    ABuGridHelper.K_GEN_FACTOR_PARAMS_SELL,
    [sell_atr_nstop_factor_grid,sell_atr_pre_factor_grid,sell_atr_close_factor_grid],need_empty_sell=True
)

buy_bk_factor_grid1 ={
    'class':[AbuFactorBuyBreak],
    'xd':[42]
}
buy_bk_factor_grid2 ={
    'class':[AbuFactorBuyBreak],
    'xd':[60]
}

buy_factors_product = ABuGridHelper.gen_factor_grid(
    ABuGridHelper.K_GEN_FACTOR_PARAMS_BUY,[buy_bk_factor_grid1,buy_bk_factor_grid2]
)

read_cash = 100000
choice_symbols = ['usAAPL', 'usTSLA','usTQQQ']

grid_search = GridSearch(read_cash,choice_symbols,buy_factors_product=buy_factors_product,sell_factors_product=sell_factors_product)

scores = None
score_tuple_array = None


def run_grid_search():
    global scores, score_tuple_array
    # 运行GridSearch n_jobs=-1启动cpu个数的进程数
    scores, score_tuple_array = grid_search.fit(n_jobs=-1)
    # 运行完成输出的score_tuple_array可以使用dump_pickle保存在本地，以方便之后使用
    ABuFileUtil.dump_pickle(score_tuple_array, '../gen/score_tuple_array')


def load_score_cache():
    """有本地数据score_tuple_array后，即可以从本地缓存读取score_tuple_array"""
    global scores, score_tuple_array

    with AbuBlockProgress('load score cache'):
        score_tuple_array = ABuFileUtil.load_pickle('../gen/score_tuple_array')
        if not hasattr(grid_search, 'best_score_tuple_grid'):
            # load_pickle的grid_search没有赋予best_score_tuple_grid，这里补上
            from abupy import make_scorer, WrsmScorer
            scores = make_scorer(score_tuple_array, WrsmScorer)
            grid_search.best_score_tuple_grid = score_tuple_array[scores.index[-1]]
        print('load complete!')


def select(select):
    if select == 'run gird search':
        run_grid_search()
    else:  # load score cache
        load_score_cache()


_ = ipywidgets.interact_manual(select, select=['run gird search', 'load score cache'])

best_score_tuple_grid = grid_search.best_score_tuple_grid
AbuMetricsBase.show_general(best_score_tuple_grid.orders_pd, best_score_tuple_grid.action_pd,
                                        best_score_tuple_grid.capital, best_score_tuple_grid.benchmark)
