#-*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import division

import warnings
warnings.simplefilter('ignore')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import abupy

from abupy import abu, AbuFactorBuyTD,BuyCallMixin,ABuSymbolPd,ABuKLUtil,EMarketSourceType
from abupy import AbuFactorSellNDay,AbuMetricsBase,ABuProgress




us_choice_symbols = ['usSYK', 'usVAR', 'usJNJ', 'usMDT', 'usBSX',
                     'usISRG', 'usCAH', 'usABT']
kl_dict = {us_symbol[2:]:ABuSymbolPd.make_kl_df(us_symbol,start='2017-01-01',end='2018-01-01') for us_symbol in us_choice_symbols}

pd.options.display.precision = 2
pd.options.display.max_columns = 30
#var_dw =ABuKLUtil.date_week_win(kl_dict['TQQQ'])
#var_dw_vd = var_dw[var_dw.win>0.55]

class AbuFactorBuyWD(AbuFactorBuyTD, BuyCallMixin):
    def _init_self(self, **kwargs):
        """
            kwargs中可选参数：buy_dw:    代表周期胜率阀值，默认0.55即55%
            kwargs中可选参数：buy_dwm:   代表涨幅比例阀值系数，默认0.618
            kwargs中可选参数：dw_period: 代表分析dw，dwm所使用的交易周期，默认40天周期(8周)
        """
        self.buy_dw = kwargs.pop('buy_dw', 0.55)
        self.buy_dwm = kwargs.pop('buy_dwm', 0.618)
        self.dw_period = kwargs.pop('dw_period', 40)

        # combine_kl_pd中包含择时金融时间数据与择时之前一年的金融时间数据, 先取出择时开始之前的周期数据
        last_kl = self.combine_kl_pd.loc[:self.kl_pd.index[0]]
        if last_kl.shape[0] > self.dw_period:
            last_kl = last_kl[-self.dw_period:]
        # 开始计算周几买，_make_buy_date把结果被放在self.buy_date_week序列中
        self._make_buy_date(last_kl)

    def fit_month(self, today):
        """月任务，每一个重新取之前一年的金融时间序列数据，重新计算一遍'周几买'"""
        end_ind = self.combine_kl_pd[self.combine_kl_pd.date == today.date].key.values[0]
        start_ind = end_ind - self.dw_period if end_ind - self.dw_period > 0 else 0
        # 根据当前的交易日，切片过去的一年金融时间序列
        last_kl = self.combine_kl_pd.iloc[start_ind:end_ind]
        # 重新计算一遍'周几买'
        self._make_buy_date(last_kl)

    def fit_day(self, today):
        """日任务：昨天下跌，今天开盘也下跌，根据今天是周几，在不在序列self.buy_date_week中决定今天买不买"""
        if self.yesterday.p_change < 0 and today.open < self.yesterday.close \
                and int(today.date_week) in self.buy_date_week:
            # 由于没有用到今天的收盘价格等，可以直接使用buy_today
            return self.buy_today()
        return None

    # noinspection PyProtectedMember
    def _make_buy_date(self, last_kl):
        self.buy_date_week = []
        # 计算周期内，周期的胜率
        last_dw = ABuKLUtil.date_week_win(last_kl)
        # 摘取大于阀值self.buy_dw的'周几'，buy_dw默认0.55
        last_dw_vd = last_dw[last_dw.win >= self.buy_dw]
        """
            eg: last_dw_vd
                       0  1   win
            date_week
            周四         3  5  0.62
            周五         2  6  0.75
        """
        if len(last_dw_vd) > 0:
            # 如果胜率有符合要求的，使用周几平均涨幅计算date_week_mean
            last_dwm = ABuKLUtil.date_week_mean(last_kl)
            # 摘取满足胜率的last_dw_vd
            last_dwm_vd = last_dwm.loc[last_dw_vd.index]
            """
                eg: last_dwm_vd
                           _p_change
                date_week
                周四              1.55
                周五              1.12
            """
            # 阀值计算方式1
            dwm1 = abs(last_dwm.sum()).values[0] / self.buy_dwm
            # 阀值计算方式2
            dwm2 = abs(last_dwm._p_change).mean() / self.buy_dwm
            # 如果symbol多可以使用&的关系
            dm_effect = (last_dwm_vd._p_change > dwm1) | (last_dwm_vd._p_change > dwm2)
            buy_date_loc = last_dwm_vd[dm_effect].index
            """
                eg: buy_date_loc
                Index(['周四', '周五'], dtype='object', name='date_week')
            """
            if len(buy_date_loc) > 0:
                # 如果涨跌幅阀值也满足，tolist，eg：['周一', '周二', '周三', '周四', '周五']
                dw_index = last_dw.index.tolist()
                # 如果是一周5个交易日的就是4，如果是比特币等7天交易日的就是6
                max_ind = len(dw_index) - 1
                for bdl in buy_date_loc:
                    sell_ind = dw_index.index(bdl)
                    buy_ind = sell_ind - 1 if sell_ind > 0 else max_ind
                    self.buy_date_week.append(buy_ind)

#初始化资金
read_cash = 100000

#买入策略AbuFactorBuyWD, 参数都是默认使用
buy_factors = [{'class':AbuFactorBuyWD}]
sell_factors = [{'class':AbuFactorSellNDay,'sell_n':1,'is_sell_today':True}]

def run_loo_back(choice_symbols, start,end):
    abu_result_tuple,_ = abu.run_loop_back(read_cash,buy_factors,sell_factors,start=start,end=end,choice_symbols=choice_symbols,n_process_pick=1)
    ABuProgress.clear_output()
    AbuMetricsBase.show_general(*abu_result_tuple,returns_cmp=True,only_info=True)
    return abu_result_tuple

abu_result_tuple = run_loo_back(us_choice_symbols,'2017-02-20', '2018-02-20')
print(abu_result_tuple.orders_pd.filter(
    ['symbol', 'buy_date', 'sell_date', 'keep_days', 'profit'])[:7])
