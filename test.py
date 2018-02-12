#-*- coding: utf-8 -*-


from __future__ import print_function

import os
import sys
sys.path.insert(0, '/home/yao/IdeaProjects/abu')

import six
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

import abupy
from abupy import six, xrange, range, reduce, map, filter, partial
from abupy import ABuSymbolPd
from collections import namedtuple
from collections import OrderedDict
from abc import ABCMeta,abstractmethod
#
#
# price_str = '30.14, 29.58, 26.36, 32.56, 32.82'
#
# price_str = price_str.replace(' ', '')
#
# price_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).close.todolist()
#
#
# date_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).date.todolist()
#
# date_base = 20170118
#
# for _ in xrange(0,len(price_array)):
#     date_array.append(str(date_base))
#     date_base+=1
#
# stock_tuple_list = [(date,price) for date, price in zip(date_array,price_array)]
# stock_namedtuple = namedtuple('stock', ('date','price'))
# stock_namedtuple_list = [stock_namedtuple(date, price ) for date, price in zip(date_array,price_array)]
#
# stock_dict = {date:price for date, price in zip(date_array,price_array)}
#
#
#
# def find_second_max(dict_array):
#     stock_prices_sorted = sorted(zip(dict_array.values(),dict_array.keys()))
#
#
#     return stock_prices_sorted[-2]
#
# price_float_array = [float(price_str) for price_str in stock_dict.values()]
# pp_array = [(price1,price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
#
# change_array = list(map(lambda pp: reduce(lambda a, b: round((b - a) / a, 3), pp), pp_array))
# change_array.insert(0,0)

class StockTradeDays(object):
    def __init__(self, price_array, start_date, date_array=None):
        self.__price_array=price_array
        self.__date_array = self.__init_days(start_date,date_array)
        self.__change_array = self.__init_change()
        self.stock_dict = self.__init_stock_dict()

    def __init_change(self):


        price_float_array = [float(price_str) for price_str in
                             self.__price_array]
        # 通过将时间平移形成两个错开的收盘价序列，通过zip打包成为一个新的序列
        # 每个元素为相邻的两个收盘价格
        pp_array = [(price1, price2) for price1, price2 in
                    zip(price_float_array[:-1], price_float_array[1:])]
        change_array = list(map(lambda pp: reduce(lambda a, b: round((b - a) / a, 3), pp), pp_array))
        # list insert插入数据，将第一天的涨跌幅设置为0
        change_array.insert(0, 0)
        return change_array

    def __init_days(self,start_date, date_array):
        if date_array is None:
            date_array=[str(start_date+ind) for ind, _ in enumerate(self.__price_array)]

        else:
            date_array= [str(date) for date in date_array]
        return date_array

    def __init_stock_dict(self):
        stock_namedtuple = namedtuple('stock',('date','price','change'))

        stock_dict = OrderedDict((date, stock_namedtuple(date, price, change)) for date, price, change in zip(self.__date_array,self.__price_array,self.__change_array))
        return stock_dict

    def filter_stock(self, want_up=True, want_calc_sum = False):
        filter_func = (lambda p_day:p_day.change >0) if want_up else (lambda p_day: p_day.change<0)
        want_days = list(filter(filter_func, self.stock_dict.values()))

        if not want_calc_sum:
            return want_days

        change_sum = 0.0000
        for day in want_days:
            change_sum += day.change
        return change_sum

    def __str__(self):
        return str(self.stock_dict)

    __repr__ = __str__

    def __iter__(self):

        for key in self.stock_dict:
            yield self.stock_dict[key]

    def __getitem__(self, ind):
        date_key = self.__date_array[ind]
        return self.stock_dict[date_key]

    def __len__(self):
        return len(self.stock_dict)


# price_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).close.tolist()
#
#
# date_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).date.tolist()
#
# date_base = 20170118
# trade_days = StockTradeDays(price_array, date_base,date_array)

class TradeStrategyBase(six.with_metaclass(ABCMeta,object)):


    @abstractmethod
    def buy_strategy(self, *args, **kwargs):
        # buying strategy
        pass

    @abstractmethod
    def sell_strategy(self, *args, **kwargs):
        # selling strategy
        pass

class TradeStrategy1(TradeStrategyBase):

    #交易策略1： 追涨策略， 当股价上涨一个阈值认为7%时，买入股票并持有s_keep_stock_threhold(20)天
    s_keep_stock_threshold =20

    def __init__(self):
        self.keep_stock_day =0
        #7% up tolerance
        self.__buy_change_threshold = 0.07

    def buy_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_day ==0 and \
            trade_day.change > self.__buy_change_threshold:
            self.keep_stock_day += 1
        elif self.keep_stock_day>0:
            self.keep_stock_day +=1

    def sell_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_day >= \
            TradeStrategy1.s_keep_stock_threshold:
            self.keep_stock_day =0


    @property
    def buy_change_threshold(self):
        return self.__buy_change_threshold

    @buy_change_threshold.setter
    def buy_change_threshold(self, buy_change_threshold):
        if not isinstance(buy_change_threshold,float):
            raise TypeError('buy_change_threshold must be float')
        self.__buy_change_threshold= round(buy_change_threshold,2)




class TradeLoopBack(object):
    """
    交易回测系统
    """

    def __init__(self,trade_days,trade_strategy):

        self.trade_days = trade_days
        self.trade_strategy = trade_strategy

        self.profit_array = []

    def execute_trade(self):
        """
        执行交易回测
        :return:
        """
        for ind, day in enumerate(self.trade_days):
            """
                以时间驱动，完成交易回测
            """
            if self.trade_strategy.keep_stock_day > 0:
                # 如果有持有股票，加入交易盈亏结果序列
                self.profit_array.append(day.change)

            # hasattr: 用来查询对象有没有实现某个方法
            if hasattr(self.trade_strategy, 'buy_strategy'):
                # 买入策略执行
                self.trade_strategy.buy_strategy(ind, day,
                                                 self.trade_days)

            if hasattr(self.trade_strategy, 'sell_strategy'):
                # 卖出策略执行
                self.trade_strategy.sell_strategy(ind, day,
                                                  self.trade_days)

price_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).close.tolist()


date_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).date.tolist()

date_base = 20170118
trade_days = StockTradeDays(price_array, date_base,date_array)


trade_loop_back = TradeLoopBack(trade_days, TradeStrategy1())
trade_loop_back.execute_trade()


sns.set_context(rc={'figure.figsize': (14,7)})
plt.plot(np.array(trade_loop_back.profit_array).cumsum())
plt.show()

