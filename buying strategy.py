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
from abupy import ABuSymbolPd
from abupy import AbuFactorBuyXD, BuyCallMixin
from abupy import AbuBenchmark
from abupy import AbuCapital
from abupy import ABuPickTimeExecute
from abupy import AbuFactorSellXD, ESupportDirection

class AbuFactorBuyBreak(AbuFactorBuyXD,BuyCallMixin):

    def fit_day(self, today):

        if today.close == self.xd_kl.close.max():
            return self.buy_tomorrow()
        return None

class AbuFactorSellBreak(AbuFactorSellXD):
    def support_direction(self):
        return [ESupportDirection.DIRECTION_CAll.value]

    def fit_day(self, today, orders):
        """
        寻找向下突破作为策略卖出驱动event
        :param today: 当前驱动的交易日金融时间序列数据
        :param orders: 买入择时策略中生成的订单序列
        """
        # 今天的收盘价格达到xd天内最低价格则符合条件
        if today.close == self.xd_kl.close.min():
            for order in orders:
                self.sell_tomorrow(order)

buy_factors = [{'xd':60, 'class':AbuFactorBuyBreak},{'xd':42, 'class':AbuFactorBuyBreak}]

sell_factors1 = {'xd':120, 'class': AbuFactorSellBreak}
sell_factors = [sell_factors1]

benchmark = AbuBenchmark()
capital = AbuCapital(1000000, benchmark)

orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usJNJ'],
                                                                            benchmark,
                                                                            buy_factors,
                                                                            sell_factors,
                                                                            capital, show=True)