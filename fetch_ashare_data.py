import sys
import os
import pandas as pd
import numpy as np

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
base = ad.BaseData()
calendar = base.get_calendar()
info = ad.InfoData()
market = ad.MarketData(calendar)

# 1. Fetch margin summary
print("Fetching margin summary from 2023 to 2026...")
margin_sum = info.get_margin_summary(begin_date=20230101, end_date=calendar[-1])
if margin_sum is not None:
    # aggregate by TRADE_DATE across exchanges
    margin_sum['TRADE_DATE'] = margin_sum['TRADE_DATE'].astype(str)
    grouped_margin = margin_sum.groupby('TRADE_DATE')[['SUM_BORROW_MONEY_BALANCE', 'SUM_PURCH_WITH_BORROW_MONEY', 'SUM_REPAYMENT_OF_BORROW_MONEY', 'SUM_MARGIN_TRADE_BALANCE']].sum().reset_index()
    grouped_margin = grouped_margin.sort_values('TRADE_DATE').reset_index(drop=True)
    print("Latest 5 days of aggregated margin summary:")
    print(grouped_margin.tail(5))
    grouped_margin.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/aggregated_margin_summary.csv', index=False)

# 2. Fetch specific ETF margin details: 515880.SH (通信ETF), 588200.SH (科创芯片), 159995.SZ (芯片ETF)
target_etfs = ['515880.SH', '588200.SH', '159995.SZ', '159915.SZ', '588000.SH', '511090.SH', '518880.SH']
print("\nFetching margin detail for target ETFs...")
try:
    margin_details = info.get_margin_detail(target_etfs, begin_date=20240101, end_date=calendar[-1])
    if margin_details is not None:
        print(f"Margin details fetched, shape: {margin_details.shape}")
        print(margin_details.tail(10))
        margin_details.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/target_etfs_margin_detail.csv', index=False)
except Exception as e:
    print(f"Error fetching margin detail: {e}")

# 3. Fetch K-lines for target ETFs and indices
print("\nFetching daily K-lines for target ETFs and indices...")
kline_codes = target_etfs + ['000001.SH', '399006.SZ', '000688.SH']
try:
    klines = market.query_kline(kline_codes, begin_date=20230101, end_date=calendar[-1], period=ad.constant.Period.day.value)
    print(f"K-lines returned for keys: {list(klines.keys()) if isinstance(klines, dict) else type(klines)}")
    for k, df in klines.items():
        df.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_{k}.csv')
        print(f"Saved {k}, shape: {df.shape}, date range: {df.index.min()} to {df.index.max()}")
except Exception as e:
    print(f"Error fetching klines: {e}")
