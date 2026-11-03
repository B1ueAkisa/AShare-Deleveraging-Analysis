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

etf_codes = ['588200.SH', '515880.SH', '588000.SH', '159915.SZ', '159995.SZ', '588170.SH']
etf_margins = info.get_margin_detail(etf_codes, begin_date=20261028, end_date=calendar[-1])

print("\n=== Key ETF Margin Balances ===")
for c, df in etf_margins.items():
    if df is not None and not df.empty:
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        print(f"\nETF {c}:")
        print(df[['TRADE_DATE', 'BORROW_MONEY_BALANCE', 'PURCH_WITH_BORROW_MONEY', 'REPAYMENT_OF_BORROW_MONEY']].to_string())

stock_codes = ['300308.SZ', '300502.SZ', '300394.SZ', '688256.SH', '688981.SH', '300476.SZ', '301308.SZ']
stk_margins = info.get_margin_detail(stock_codes, begin_date=20261028, end_date=calendar[-1])

print("\n=== Key Stock Margin Balances ===")
for c, df in stk_margins.items():
    if df is not None and not df.empty:
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        print(f"\nStock {c}:")
        print(df[['TRADE_DATE', 'BORROW_MONEY_BALANCE', 'PURCH_WITH_BORROW_MONEY', 'REPAYMENT_OF_BORROW_MONEY']].to_string())
