import os
import sys
import pandas as pd
import numpy as np
import yfinance as yf

# Unset proxy if set to local 7890
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

print("1. Fetching US historical crashes via yfinance...")
# 2000 Dot-Com
nasdaq_2000 = yf.download('^IXIC', start='1999-10-01', end='2003-01-01', progress=False)
if isinstance(nasdaq_2000.columns, pd.MultiIndex):
    nasdaq_2000.columns = nasdaq_2000.columns.get_level_values(0)
nasdaq_2000.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_nasdaq_2000.csv')
print("Nasdaq 2000 saved, shape:", nasdaq_2000.shape)

# 2020 Covid
sp500_2020 = yf.download('^GSPC', start='2020-01-01', end='2020-06-01', progress=False)
if isinstance(sp500_2020.columns, pd.MultiIndex):
    sp500_2020.columns = sp500_2020.columns.get_level_values(0)
sp500_2020.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_sp500_2020.csv')
print("S&P500 2020 saved, shape:", sp500_2020.shape)

nasdaq_2020 = yf.download('^IXIC', start='2020-01-01', end='2020-06-01', progress=False)
if isinstance(nasdaq_2020.columns, pd.MultiIndex):
    nasdaq_2020.columns = nasdaq_2020.columns.get_level_values(0)
nasdaq_2020.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_nasdaq_2020.csv')

# 2018 US
nasdaq_2018 = yf.download('^IXIC', start='2018-09-01', end='2019-02-01', progress=False)
if isinstance(nasdaq_2018.columns, pd.MultiIndex):
    nasdaq_2018.columns = nasdaq_2018.columns.get_level_values(0)
nasdaq_2018.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_nasdaq_2018.csv')

print("\n2. Fetching A-share historical crashes via AmazingData...")
config.init_amazing_data()
base = ad.BaseData()
calendar = base.get_calendar()
market = ad.MarketData(calendar)

# 2015 crash: 000001.SH, 399006.SZ
# 2008 crash: 000001.SH, 000300.SH
try:
    k_2015 = market.query_kline(['000001.SH', '399006.SZ', '000300.SH'], begin_date=20140601, end_date=20160601, period=ad.constant.Period.day.value)
    for k, v in k_2015.items():
        v.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_2015_{k}.csv')
        print(f"Hist 2015 {k} saved, shape:", v.shape)
except Exception as e:
    print(f"Error fetching 2015 klines: {e}")

try:
    k_2008 = market.query_kline(['000001.SH', '000300.SH'], begin_date=20070101, end_date=20090101, period=ad.constant.Period.day.value)
    for k, v in k_2008.items():
        v.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_2008_{k}.csv')
        print(f"Hist 2008 {k} saved, shape:", v.shape)
except Exception as e:
    print(f"Error fetching 2008 klines: {e}")

print("All historical crash data fetched successfully!")
