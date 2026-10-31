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

# 1. Check SSE vs SZSE reporting delay
print("--- 1. Checking SSE vs SZSE Margin Summary Reporting Dates ---")
margin_sum = info.get_margin_summary(begin_date=20261020, end_date=calendar[-1])
print(margin_sum[['TRADE_DATE', 'EXCHANGE', 'SUM_BORROW_MONEY_BALANCE']].sort_values(['TRADE_DATE', 'EXCHANGE']).to_string())

# 2. Target stocks:
# 通信 "易中天": 新易盛(300502.SZ), 中际旭创(300308.SZ), 天孚通信(300394.SZ)
# 科创半导体: 寒武纪(688256.SH), 中芯国际(688981.SH), 中微公司(688012.SH), 海光信息(688041.SH)
target_stocks = {
    '300502.SZ': '新易盛',
    '300308.SZ': '中际旭创',
    '300394.SZ': '天孚通信',
    '688256.SH': '寒武纪',
    '688981.SH': '中芯国际',
    '688012.SH': '中微公司',
    '688041.SH': '海光信息'
}

stock_codes = list(target_stocks.keys())
print("\n--- 2. Fetching Margin Details for Representative Stocks ---")
try:
    stock_margins = info.get_margin_detail(stock_codes, begin_date=20260501, end_date=calendar[-1])
    if isinstance(stock_margins, dict):
        for code, df_m in stock_margins.items():
            name = target_stocks.get(code, code)
            df_m.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/stock_margin_{code}.csv', index=False)
            print(f"Saved margin for {code} ({name}), shape {df_m.shape}, last date {df_m['TRADE_DATE'].iloc[-1] if not df_m.empty else None}")
except Exception as e:
    print(f"Error fetching stock margin details: {e}")

print("\n--- 3. Fetching K-lines for Representative Stocks ---")
try:
    stock_klines = market.query_kline(stock_codes, begin_date=20260501, end_date=calendar[-1], period=ad.constant.Period.day.value)
    if isinstance(stock_klines, dict):
        for code, df_k in stock_klines.items():
            name = target_stocks.get(code, code)
            df_k.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/stock_kline_{code}.csv')
            print(f"Saved kline for {code} ({name}), shape {df_k.shape}")
except Exception as e:
    print(f"Error fetching stock klines: {e}")
