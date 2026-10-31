import yfinance as yf
import pandas as pd
import numpy as np

# Load raw kline from AmazingData
df_comm = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_515880.SH.csv')
df_comm['date'] = pd.to_datetime(df_comm['kline_time'])
df_comm = df_comm.sort_values('date').reset_index(drop=True)

df_chip = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_588200.SH.csv')
df_chip['date'] = pd.to_datetime(df_chip['kline_time'])
df_chip = df_chip.sort_values('date').reset_index(drop=True)

# Also check ETF fund nav / share data from AmazingData InfoData
import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
info = ad.InfoData()

print("--- Querying ETF Fund Share / NAV for 515880.SH and 588200.SH ---")
try:
    shares = info.get_fund_share(['515880.SH', '588200.SH'], begin_date=20260601, end_date=20261030)
    print("Fund shares shape:", shares.shape if shares is not None else None)
    if shares is not None:
        print(shares.head(10))
        shares.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/etf_fund_shares.csv', index=False)
except Exception as e:
    print("Error getting fund share:", e)

try:
    nav = info.get_fund_iopv(['515880.SH', '588200.SH'], begin_date=20260601, end_date=20261030)
    print("Fund IOPV shape:", nav.shape if nav is not None else None)
    if nav is not None:
        print(nav.head(10))
        nav.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/etf_iopv.csv', index=False)
except Exception as e:
    print("Error getting fund iopv:", e)
