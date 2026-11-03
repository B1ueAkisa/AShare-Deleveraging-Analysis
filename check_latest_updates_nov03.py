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
print("Latest 5 trading calendar dates:", calendar[-5:])

info = ad.InfoData()
market = ad.MarketData(calendar)

# 1. Check margin summary for latest dates
print("\n=== Margin Summary from 20261028 to latest ===")
ms = info.get_margin_summary(begin_date=20261028, end_date=calendar[-1])
if ms is not None and not ms.empty:
    ms['TRADE_DATE'] = ms['TRADE_DATE'].astype(str)
    ms_sorted = ms.sort_values(['TRADE_DATE', 'EXCHANGE']).reset_index(drop=True)
    print(ms_sorted[['TRADE_DATE', 'EXCHANGE', 'SUM_BORROW_MONEY_BALANCE', 'SUM_PURCH_WITH_BORROW_MONEY', 'SUM_REPAYMENT_OF_BORROW_MONEY']].to_string())

# 2. Check today's market crash (K-lines on 2026-11-02 and 2026-11-03)
check_codes = ['000001.SH', '399006.SZ', '000688.SH', '588000.SH', '159915.SZ', '588200.SH', '515880.SH', '300308.SZ', '300502.SZ', '688256.SH', '300476.SZ', '301308.SZ']
klines = market.query_kline(check_codes, begin_date=20261028, end_date=calendar[-1], period=ad.constant.Period.day.value)

print("\n=== Price Performance (Close & Daily Return) ===")
for c in check_codes:
    if c in klines and klines[c] is not None and not klines[c].empty:
        df_k = klines[c].copy()
        df_k['date'] = pd.to_datetime(df_k['kline_time']).dt.strftime('%Y%m%d')
        df_k['pct_chg'] = df_k['close'].pct_change() * 100
        print(f"\nCode: {c}")
        print(df_k[['date', 'open', 'close', 'high', 'low', 'pct_chg']].tail(4).to_string())
