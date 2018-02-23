#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context(rc={'figure.figsize':(14,7)})
figzize_me = figsize = (14,7)

import os
import sys

sys.path.insert(0, os.path.abspath('/home/yao/IdeaProjects/abu'))
import abupy

abupy.env.enable_example_env_ipython()

from abupy import ABuSymbolPd
from abupy import ABuRegUtil
from abupy import pd_rolling_max
from abupy import pd_rolling_min, pd_expanding_min

kl_pd = ABuSymbolPd.make_kl_df('usTSLA', n_folds=2)
train_kl = kl_pd[:252]
test_kl =kl_pd[252:]
#
# sns.set_context(rc={'figure.figsize':(14,7)})
# sns.regplot(x=np.arange(0,kl_pd.shape[0]),y=kl_pd.close.values,marker='.')
#
# deg = ABuRegUtil.calc_regress_deg(kl_pd.close.values)
#
# start =0
# end = int(kl_pd.shape[0]/4)
#
# x=np.arange(start,end)
# y= kl_pd.close.values[start:end]
# sns.regplot(x=x,y=y,marker='+')

tmp_df = pd.DataFrame(np.array([train_kl.close.values, test_kl.close.values]).T, columns=['train','test'])
tmp_df[['train','test']].plot(subplots=True, grid =True,figsize=(14,7))

close_mean = train_kl.close.mean()
close_std = train_kl.close.std()

sell_signal = close_mean+ close_std/3
buy_signal = close_mean -close_std/3

#可视化训练数据的卖出信号阈值，买入信号阈值及均值线
plt.figure(figsize=(14,7))

# #训练集合收盘价格可视化
# train_kl.close.plot()
# plt.axhline(buy_signal,color='r',lw=3)
# plt.axhline(close_mean,color='black',lw=1)
# plt.axhline(sell_signal,color='g',lw=3)
# plt.legend(['train close','buy_signal','close_mean','sell_signal'], loc='best')
#
# buy_index = train_kl[train_kl['close']< buy_signal].index
# train_kl.loc[buy_index,'signal'] =1

#趋势跟踪策略
#当天收盘价超过N1天内最高价格作为买入信号
N1=42

#当天收盘价超过N2天内最低价格作为卖出信号
N2 = 21

kl_pd['n1_high']=pd_rolling_max(kl_pd['high'], window =N1)
kl_pd['n2_low'] =pd_rolling_min(kl_pd['low'],window=N2)
expan_min = pd_expanding_min(kl_pd['close'])
kl_pd['n2_low'].fillna(value=expan_min, inplace=True)
buy_index = kl_pd[kl_pd['close']>kl_pd['n1_high'].shift(1)].index
kl_pd.loc[buy_index,'signal']=1

sell_index = kl_pd[kl_pd['close']<kl_pd['n2_low'].shift(1)].index
kl_pd.loc[sell_index, 'signal']=0

kl_pd['keep']=kl_pd['signal'].shift(1)
kl_pd['keep'].fillna(method='ffill', inplace=True)

#计算基准收益
kl_pd['benchmark_profit']=np.log(kl_pd['close']/kl_pd['close'].shift(1))

#计算使用趋势突破策略的收益
kl_pd['trend_profit'] = kl_pd['keep']*kl_pd['benchmark_profit']

# #可视化收益的情况对比
# kl_pd[['benchmark_profit','trend_profit']].cumsum().plot(grid=True,figsize=(14,7))

#一只股票的时间简史
#第一阶段走势涵盖股票上市后前100天的走势请况
trade_day =100

#这个股票第一阶段走势函数gen_stock_price_array
def gen_stock_price_array():
    price_array = np.ones(trade_day)

    #以时间驱动100个交易日，生成100个交易日走势
    for ind in np.arange(0,trade_day-1):
        if ind ==0:
            #第一交易日50%的概率结果是win
            win = np.random.binomial(1,0.5)
        else:
            win = price_array[ind]>price_array[ind-1]

        if win:
            price_array[ind+1] = (1+0.05)*price_array[ind]

        else:
            price_array[ind+1] = (1-0.05)*price_array[ind]
    return price_array

_, axs = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
price_array1 =gen_stock_price_array()
price_array1_ex = gen_stock_price_array()

axs[0].plot(price_array1)
axs[1].plot(price_array1_ex)
plt.show()