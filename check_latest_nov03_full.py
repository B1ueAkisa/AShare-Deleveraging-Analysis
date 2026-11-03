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
print("Trading calendar latest 5:", calendar[-5:])

info = ad.InfoData()
market = ad.MarketData(calendar)

# 1. Check Margin Summary up to latest
ms = info.get_margin_summary(begin_date=20261028, end_date=calendar[-1])
if ms is not None and not ms.empty:
    ms['TRADE_DATE'] = ms['TRADE_DATE'].astype(str)
    ms_pivot = ms.pivot_table(index='TRADE_DATE', columns='EXCHANGE', values='SUM_BORROW_MONEY_BALANCE')
    ms_pivot['TOTAL_SSE_SZSE'] = ms_pivot.get('SSE', 0) + ms_pivot.get('SZSE', 0)
    print("\n=== Margin Summary by Exchange (100M RMB) ===")
    print((ms_pivot / 1e8).round(2).to_string())

# 2. Check 30Y Treasury and Gold ETFs on 11-02 and 11-03
macro_codes = ['511090.SH', '518880.SH', '000001.SH', '399006.SZ', '000688.SH', '515880.SH', '588200.SH']
macro_klines = market.query_kline(macro_codes, begin_date=20261028, end_date=calendar[-1], period=ad.constant.Period.day.value)
print("\n=== Macro Assets & Indices Close and Pct Change ===")
for c in macro_codes:
    if c in macro_klines and macro_klines[c] is not None:
        df = macro_klines[c].copy()
        df['date'] = pd.to_datetime(df['kline_time']).dt.strftime('%Y%m%d')
        df['pct_chg'] = df['close'].pct_change() * 100
        print(f"\n{c}:")
        print(df[['date', 'close', 'pct_chg']].tail(4).to_string())

# 3. Check ETF Margin Details on latest available date (588200, 515880, 588000, 159915, 159995, 588170)
etf_codes = ['588200.SH', '515880.SH', '588000.SH', '159915.SZ', '159995.SZ', '588170.SH']
etf_margins = info.get_margin_detail(etf_codes, begin_date=20261028, end_date=calendar[-1])
if etf_margins is not None and not etf_margins.empty:
    etf_margins['TRADE_DATE'] = etf_margins['TRADE_DATE'].astype(str)
    etf_piv = etf_margins.pivot_table(index='TRADE_DATE', columns='SECURITY_CODE', values='BORROW_MONEY_BALANCE')
    print("\n=== Key ETF Margin Balances (100M RMB) ===")
    print((etf_piv / 1e8).round(2).to_string())

# 4. Check Key Stocks Margin Details on latest available date
stock_codes = ['300308.SZ', '300502.SZ', '300394.SZ', '688256.SH', '688981.SH', '300476.SZ', '301308.SZ', '603083.SH']
stk_margins = info.get_margin_detail(stock_codes, begin_date=20261028, end_date=calendar[-1])
if stk_margins is not None and not stk_margins.empty:
    stk_margins['TRADE_DATE'] = stk_margins['TRADE_DATE'].astype(str)
    stk_piv = stk_margins.pivot_table(index='TRADE_DATE', columns='SECURITY_CODE', values='BORROW_MONEY_BALANCE')
    print("\n=== Key Stocks Margin Balances (100M RMB) ===")
    print((stk_piv / 1e8).round(2).to_string())
