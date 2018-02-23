# -*- coding:utf-8 -*-
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
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('/home/yao/IdeaProjects/abu'))
import abupy

from abupy import abu, ml, nd, tl, pd_resample, AbuML, AbuMLPd, AbuMetricsBase
from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop, AbuFactorBuyBreak
from abupy import ABuSymbolPd, ABuScalerUtil, get_price, ABuMarketDrawing, ABuKLUtil

def plot_trend(symbol='usNVDA', n_folds=1, only_last=False, how='both', show_step=False):
    n_folds = int(n_folds)
    # 获取symbol的n_folds年数据
    kl = ABuSymbolPd.make_kl_df(symbol, n_folds=n_folds)
    # 构造技术线对象
    kl_tl = tl.AbuTLine(kl.close, 'kl')
    if how == 'support':
        # 只绘制支持线
        kl_tl.show_support_trend(only_last=only_last, show=True, show_step=show_step)
    elif how == 'resistance':
        # 只绘制阻力线
        kl_tl.show_resistance_trend(only_last=only_last, show=True, show_step=show_step)
    else:
        # 支持线和阻力线都绘制
        kl_tl.show_support_resistance_trend(only_last=only_last, show=True, show_step=show_step)
tsla_df = ABuSymbolPd.make_kl_df('usTSLA')
jumps = tl.jump.calc_jump(tsla_df)