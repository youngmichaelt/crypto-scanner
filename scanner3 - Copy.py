import ccxt
import asciichart
import pandas as pd
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import schedule
import time
from mpl_finance import candlestick_ohlc
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import stockstats
from stockstats import StockDataFrame as Sdf
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

tickers = ['BTC/USDT', 'ETH/BTC', 'LTC/BTC', 'VEN/BTC', 'ETC/BTC', 'ICX/BTC',
           'ADA/BTC', 'ADX/BTC', 'AE/BTC', 'AION/BTC', 'AMB/BTC', 'APPC/BTC',
           'ARK/BTC', 'ARN/BTC', 'BAT/BTC', 'BCD/BTC', 'BCPT/BTC', 'BLZ/BTC', 'BNB/BTC',
           'BNT/BTC', 'BQX/BTC', 'BRD/BTC', 'BTG/BTC', 'BTS/BTC', 'CDT/BTC', 'CMT/BTC', 'CND/BTC',
           'CTR/BTC', 'DASH/BTC', 'DGD/BTC', 'DNT/BTC', 'DLT/BTC', 'EDO/BTC', 'ELF/BTC', 'ENG/BTC',
           'ENJ/BTC', 'EOS/BTC', 'EVX/BTC', 'FUEL/BTC', 'FUN/BTC', 'GAS/BTC', 'GTO/BTC', 'GVT/BTC',
           'GXS/BTC', 'HSR/BTC', 'ICN/BTC', 'INS/BTC', 'IOST/BTC','IOTA/BTC', 'KMD/BTC', 'KNC/BTC', 'LEND/BTC',
           'LINK/BTC', 'LSK/BTC', 'LUN/BTC', 'MANA/BTC', 'MCO/BTC', 'MDA/BTC', 'MOD/BTC', 'MTH/BTC',
           'MTL/BTC', 'NAV/BTC', 'NEBL/BTC', 'NEO/BTC', 'NULS/BTC', 'OAX/BTC', 'OMG/BTC', 'OST/BTC',
           'PIVX/BTC', 'POE/BTC', 'POWR/BTC', 'PPT/BTC', 'QSP/BTC', 'QTUM/BTC', 'RCN/BTC', 'REQ/BTC',
           'RLC/BTC', 'RPX/BTC', 'SALT/BTC', 'SNGLS/BTC', 'SNM/BTC', 'SNT/BTC', 'STEEM/BTC', 'STORJ/BTC',
           'STRAT/BTC', 'SUB/BTC', 'TNB/BTC', 'TNT/BTC', 'TRIG/BTC', 'TRX/BTC', 'VIA/BTC', 'VIB/BTC',
           'VIBE/BTC', 'WABI/BTC', 'WAVES/BTC', 'WTC/BTC', 'XLM/BTC', 'XMR/BTC', 'XRP/BTC', 'XVG/BTC',
           'XZC/BTC', 'ZEC/BTC', 'ZRX/BTC']
##tickers = ['BTC/USDT']


def poll(tickers):
    i = 0
    kraken = ccxt.binance()
    while i < 103:
        symbol = tickers[i % len(tickers)]
##    symbol = 'BTC/USDT'
        ohlcv = kraken.fetch_ohlcv(symbol, '4h')
        df = pd.DataFrame(ohlcv, columns = ['date','open','high','low','close','volume'])
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        stock = Sdf.retype(df)
        
        df['rsi'] = stock['rsi_14']
        rsi = stock['rsi_14']
        close = stock['close']

        
        df['boll'] = stock['boll']
        df['boll_ub'] = stock['boll_ub']
        df['boll_lb'] = stock['boll_lb']

        df['close_13_ema'] = stock['close_13_ema']
        df['close_34_ema'] = stock['close_34_ema']
        ema_13 = stock['close_13_ema']
        ema_34 = stock['close_34_ema']
        

##        df['macd'] = stock['macd']
##        df['macds'] = stock['macds']
##        df['macdh'] = df['macdh']

        
        stock = stock.reset_index()
        stock['date'] = stock['date'].map(mdates.date2num)

        print (symbol)
        print ('RSI: ',rsi[-1])
        print('Close: ', close[-1])
    
        i += 1
        time.sleep(kraken.rateLimit / 1000)
    
        if rsi[-1]  < 25 or ema_13[-1] >= ema_34[-1] and ema_13[-2] <= ema_34[-2]:
##            if ema_13[-1] >= ema_34[-1] and ema_13[-2] < ema_34[-2]:
            
                print('Yesterday EMA13: ',ema_13[-2],'\n EMA34: ',ema_34[-2],'\n','Today EMA13: ',ema_13[-1],'\n','EMA34: ',ema_34[-1]) 
                ax1 = plt.subplot2grid((10,1), (0,0), rowspan=5, colspan=1)
                ax2 = plt.subplot2grid((10,1), (6,0), rowspan=3, colspan=1, sharex=ax1)
                

                candlestick_ohlc(ax1, stock.values, width=0.1, colorup='g')
                ax1.set_xlim(pd.Timestamp(2018,2,1), pd.Timestamp.now())

                ax2.set_ylim(0, 100)
                ax1.set_title(symbol)
                
            ##    ax1.plot(df['close'])
                ax2.plot(df['rsi_14'])

                ax1.plot(df['close_13_ema'])
                ax1.plot(df['close_34_ema'])
    ##            

    ##            ax1.plot(df['boll'])
    ##            ax1.plot(df['boll_ub'])
    ##            ax1.plot(df['boll_lb'])
    ##            ax3.plot(df['macd'])
    ##            ax3.plot(df['macds'])
    ##            ax3.plot(df['macdh'])


                plt.show()
                    
    ##    i += 1
    ##    time.sleep(kraken.rateLimit / 500)

        ##    print(symbol, stock)
    ##          
           

poll(tickers)

 

