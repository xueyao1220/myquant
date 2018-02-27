#-*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import division

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import abupy

from abupy import ABuSymbolPd

us_tqqq = ABuSymbolPd.make_kl_df('usTQQQ',start='2015-07-28',end='2017-07-28')
us_qqq = ABuSymbolPd.make_kl_df('QQQ', start='2015-07-28',end='2017-07-28')
diff_abs = (us_tqqq.p_change)/(us_qqq.p_change)
diff_open_qqq = (us_tqqq.p_change/us_tqqq.open)/(us_qqq.p_change/us_qqq.open)
diff_close_qqq = (us_tqqq.p_change/us_tqqq.close)/(us_qqq.p_change/us_qqq.close)

_, ax1 = plt.subplots()
ax1.plot(diff_abs,c='r',label = 'diff_abs')
ax1.plot(diff_open_qqq,c='b',label = 'diff_open_qqq')
ax1.plot(diff_close_qqq,c='g',label = 'diff_close_qqq')

_2,ax2 = plt.subplots()
ax2.plot(us_tqqq.p_change,c='r',label = 'tqqq')
ax2.plot(us_qqq.p_change,c='b',label = 'qqq')

ax1.legend(loc=1)
ax2.legend(loc=1)
plt.show()