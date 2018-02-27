#-*- coding:UTF-8 -*-

import talib
import pandas as pd
from abupy import ABuSymbolPd
import matplotlib.pyplot as plt

jnj_df = ABuSymbolPd.make_kl_df('usJNJ', n_folds=2)

#timeperiod = 14
rsi = talib.RSI(jnj_df.close.values)
rsi1 =talib.RSI(jnj_df.close.values,6)
rsi2 = talib.RSI(jnj_df.close.values,12)
rsi3 = talib.RSI(jnj_df.close.values,24)

jnj_df['rsi'] = rsi
jnj_df['rsi2'] = rsi2
jnj_df['rsi3'] = rsi3
jnj_df['rsi1'] = rsi1

#figure display
#jnj_df.close.plot(figsize =(12,4))
#jnj_df.rsi.plot(figsize=(12,4),xticks=[],color='b')

buyThres = 30
sellThres = 70

rsiSig =[]

# for index in jnj_df.rsi:
#     if index > sellThres:
#         rsiSig.append(-1)
#     elif index<buyThres:
#         rsiSig.append(1)
#     else:
#         rsiSig.append(0)
#
# jnj_df['rsiSig'] = rsiSig
# jnj_df.rsiSig.plot(figsize =(12,4))


jnj_df['rsiDif'] = jnj_df.rsi1-jnj_df.rsi3

rsiSig = [0]*len(jnj_df.rsiDif)
for index in range(len(jnj_df['rsiDif'])-1):
    if jnj_df['rsiDif'][index]>0 and jnj_df['rsiDif'][index-1]<0 and jnj_df['rsi'][index-1]< buyThres:
        rsiSig[index+1]=1
    elif jnj_df['rsiDif'][index]<0 and jnj_df['rsiDif'][index-1]>0 and jnj_df['rsi'][index-1]> sellThres:
        rsiSig[index+1] =-1


jnj_df['rsiSig']= rsiSig

_, ax1 = plt.subplots()
ax1.plot(jnj_df.rsiSig,c='r',label = 'RSI Signal')

ax1.legend(loc=2)
ax1.grid(False)

ax2=ax1.twinx()
ax2.plot(jnj_df.rsi1, c='g', label='RSI')
ax2.legend(loc=1)
ax2.plot(jnj_df.rsi3, c='b', label='RSI')
ax2.legend(loc=1)

