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

# Check 30 tech stocks from expanded_30_tech_stocks_margin.csv
stk_file = r'd:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\expanded_30_tech_stocks_margin.csv'
if os.path.exists(stk_file):
    df_30 = pd.read_csv(stk_file)
    stock_codes = df_30['code'].tolist()
else:
    stock_codes = ['300308.SZ', '300502.SZ', '300394.SZ', '688256.SH', '688981.SH', '688041.SH', '300476.SZ', '301308.SZ', '603083.SH', '688525.SH']

klines = market.query_kline(stock_codes, begin_date=20261030, end_date=20261103, period=ad.constant.Period.day.value)

res = []
for c in stock_codes:
    if c in klines and klines[c] is not None and len(klines[c]) >= 2:
        df_k = klines[c].copy()
        df_k['pct_chg'] = df_k['close'].pct_change() * 100
        # Get Nov 03 pct change
        nov03_chg = df_k.iloc[-1]['pct_chg']
        nov03_close = df_k.iloc[-1]['close']
        nov02_chg = df_k.iloc[-2]['pct_chg'] if len(df_k) >= 3 else 0
        res.append({
            'code': c,
            'nov03_close': nov03_close,
            'nov03_pct_chg': nov03_chg,
            'nov02_pct_chg': nov02_chg
        })

df_res = pd.DataFrame(res).sort_values('nov03_pct_chg')
print("=== 30 Tech Stocks Performance on 2026-11-03 (Sorted by Drop) ===")
print(df_res.to_string())

# Check ETFs as well
etf_check = ['588200.SH', '515880.SH', '588000.SH', '159915.SZ', '159995.SZ', '588170.SH', '159558.SZ', '560780.SH', '511090.SH', '518880.SH']
k_etf = market.query_kline(etf_check, begin_date=20261030, end_date=20261103, period=ad.constant.Period.day.value)
res_etf = []
for c in etf_check:
    if c in k_etf and k_etf[c] is not None and len(k_etf[c]) >= 2:
        df_k = k_etf[c].copy()
        df_k['pct_chg'] = df_k['close'].pct_change() * 100
        res_etf.append({
            'code': c,
            'nov03_close': df_k.iloc[-1]['close'],
            'nov03_pct_chg': df_k.iloc[-1]['pct_chg']
        })
print("\n=== Key ETFs Performance on 2026-11-03 ===")
print(pd.DataFrame(res_etf).sort_values('nov03_pct_chg').to_string())
