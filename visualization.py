#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import numpy as np
import pandas as pd
import  seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from scipy import stats
from  collections import namedtuple


sns.set_context(rc= {'figure.figsize': (14,7)})
figsize = figsize = (14,7)

import os
import sys

sys.path.insert(0, os.path.abspath('/home/yao/IdeaProjects/abu'))
import abupy

from abupy import ABuSymbolPd
from abupy import pd_rolling_std, pd_ewm_std
from abupy import pd_rolling_mean

tsla_df = ABuSymbolPd.make_kl_df('usTSLA', n_folds =2)
print(tsla_df.tail())

def plot_demo(axs =None, just_series= False):

    drawer = plt if axs is None else axs
    drawer.plot(tsla_df.close, c = 'r')
    if not just_series:
        drawer.plot(tsla_df.close.index, tsla_df.close.values +10, c ='g')
        drawer.plot(tsla_df.close.index.tolist(),(tsla_df.close.values+20).tolist(), c='b')

    plt.xlabel('time')
    plt.ylabel('close')
    plt.title('TSLA CLOSE')
    plt.grid(True)


__colorup__ = "red"
__colordown__ = "green"

tsla_part_df = tsla_df[:30]
fig, ax = plt.subplots(figsize=(14,7))
qutotes = []

# for index, (d,o,c,h,l) in enumerate(zip(tsla_part_df.index, tsla_part_df.open,tsla_part_df.close,tsla_part_df.high,tsla_part_df.low)):
#     d = mpf.date2num(d)
#     val = (d,o,c,h,l)
#     qutotes.append(val)
#
# mpf.candlestick_ochl(ax, qutotes, width=0.6, colorup=__colorup__,
#                      colordown=__colordown__)
# ax.autoscale_view()
# ax.xaxis_date()


# tsla_df_copy = tsla_df.copy()
# tsla_df_copy['return'] = np.log(tsla_df['close']/ tsla_df['close'].shift(1))
# tsla_df_copy['mov_std'] = pd_rolling_std(tsla_df_copy['return'],window =20, center = False)*np.sqrt(20)
# tsla_df_copy['std_ewm'] = pd_ewm_std(tsla_df_copy['return'], span=20, min_periods=20, adjust=True)*np.sqrt(20)
# tsla_df_copy[['close','mov_std','std_ewm','return']].plot(subplots=True, grid = True)
#

# tsla_df.close.plot()
#
# pd_rolling_mean(tsla_df.close, window =30).plot()
# pd_rolling_mean(tsla_df.close, window =60).plot()
# pd_rolling_mean(tsla_df.close, window=90).plot()
# plt.legend(['close','30 mv', '60 mv', '90 mv'], loc='best')
# plt.show()

def plot_trade(buy_date,sell_date):
    start = tsla_df[tsla_df.index == buy_date].key.values[0]
    end = tsla_df[tsla_df.index == sell_date].key.values[0]

    plot_demo(just_series=True)

    plt.fill_between(tsla_df.index, 0, tsla_df['close'], color = 'blue', alpha = 0.08)

    plt.fill_between(tsla_df.index[start:end],0,tsla_df['close'][start:end],color='green', alpha = 0.38)
    plt.ylim(np.min(tsla_df['close'])-5, np.max(tsla_df['close'])+5)
    plt.legend(['close'],loc='best')


#how to calculate golden line
cs_max = tsla_df.close.max()
cs_min = tsla_df.close.min()

sp382 = (cs_max-cs_min)*0.382 +cs_min
sp618 = (cs_max-cs_min)*0.618 +cs_min



sp382_stats = stats.scoreatpercentile(tsla_df.close,38.2)
sp618_stats = stats.scoreatpercentile(tsla_df.close, 61.8)

print(sp618_stats)


def plot_golden():
    above618 = np.maximum(sp618,sp618_stats)
    below618 = np.minimum(sp618,sp618_stats)
    above382 = np.maximum(sp382,sp382_stats)
    below382 = np.minimum(sp382,sp382_stats)

    #plot close price

    plt.plot(tsla_df.close)

    plt.axhline(sp382,c='r')
    plt.axhline(sp382_stats, c='m')
    plt.axhline(sp618,c='g')
    plt.axhline(sp618_stats,c='k')


    plt.fill_between(tsla_df.index,above618,below618, alpha=0.5, color ="r")
    plt.fill_between(tsla_df.index,above382,below382, alpha=0.5, color="g")

    return  namedtuple('golden', ['above618', 'below618','above382','below382'])(above618,below618,above382,below382)

golden = plot_golden()
plt.legend(['close','sp382', 'sp382_stats','sp618','sp618_stats'], loc='best')
plt.show()

