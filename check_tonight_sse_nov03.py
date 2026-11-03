import sys
import os
import pandas as pd
import numpy as np

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
info = ad.InfoData()
base = ad.BaseData()
calendar = base.get_calendar()

print("Checking 20261103 margin data at:", pd.Timestamp.now())

# 1. Margin Summary
ms = info.get_margin_summary(begin_date=20261030, end_date=20261103)
if ms is not None and not ms.empty:
    ms['TRADE_DATE'] = ms['TRADE_DATE'].astype(str)
    print("\n=== Margin Summary (20261030 - 20261103) ===")
    print(ms[['TRADE_DATE', 'EXCHANGE', 'SUM_BORROW_MONEY_BALANCE', 'SUM_PURCH_WITH_BORROW_MONEY', 'SUM_REPAYMENT_OF_BORROW_MONEY']].to_string())
else:
    print("No margin summary data returned for 20261103")

# 2. Key SSE ETFs
sse_etfs = ['588200.SH', '515880.SH', '588000.SH', '588170.SH', '560780.SH', '512480.SH']
etf_res = info.get_margin_detail(sse_etfs, begin_date=20261030, end_date=20261103)
print("\n=== SSE Key ETF Margin Balances ===")
for c, df in etf_res.items():
    if df is not None and not df.empty:
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        df['MARGIN_BALANCE_100M'] = (df['BORROW_MONEY_BALANCE'] / 1e8).round(2)
        df['PURCHASE_100M'] = (df['PURCH_WITH_BORROW_MONEY'] / 1e8).round(2)
        df['REPAYMENT_100M'] = (df['REPAYMENT_OF_BORROW_MONEY'] / 1e8).round(2)
        print(f"\nETF {c}:")
        print(df[['TRADE_DATE', 'MARGIN_BALANCE_100M', 'PURCHASE_100M', 'REPAYMENT_100M']].to_string())

# 3. Key SSE Stocks
sse_stocks = ['688256.SH', '688981.SH', '688008.SH', '688041.SH', '603083.SH', '600183.SH', '603986.SH', '601138.SH']
stk_res = info.get_margin_detail(sse_stocks, begin_date=20261030, end_date=20261103)
print("\n=== SSE Key Tech Stock Margin Balances ===")
for c, df in stk_res.items():
    if df is not None and not df.empty:
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        df['MARGIN_BALANCE_100M'] = (df['BORROW_MONEY_BALANCE'] / 1e8).round(2)
        df['PURCHASE_100M'] = (df['PURCH_WITH_BORROW_MONEY'] / 1e8).round(2)
        df['REPAYMENT_100M'] = (df['REPAYMENT_OF_BORROW_MONEY'] / 1e8).round(2)
        print(f"\nStock {c}:")
        print(df[['TRADE_DATE', 'MARGIN_BALANCE_100M', 'PURCHASE_100M', 'REPAYMENT_100M']].to_string())
