import pandas as pd
import numpy as np

# Load merged market data
df_market = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/merged_market_data.csv')
df_market['kline_time'] = pd.to_datetime(df_market['kline_time'])

# Load aggregated margin
df_margin = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/aggregated_margin_summary.csv')
df_margin['kline_time'] = pd.to_datetime(df_margin['TRADE_DATE'].astype(str))

df = pd.merge(df_market, df_margin, on='kline_time', how='inner')
df = df[df['kline_time'] >= '2026-05-01'].copy().sort_values('kline_time').reset_index(drop=True)

# Also load ETF margin details for 515880.SH and 588200.SH
m_comm = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_515880.SH.csv')
m_comm['kline_time'] = pd.to_datetime(m_comm['TRADE_DATE'].astype(str))
m_comm = m_comm[['kline_time', 'BORROW_MONEY_BALANCE']].rename(columns={'BORROW_MONEY_BALANCE': 'comm_margin'})

m_chip = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_588200.SH.csv')
m_chip['kline_time'] = pd.to_datetime(m_chip['TRADE_DATE'].astype(str))
m_chip = m_chip[['kline_time', 'BORROW_MONEY_BALANCE']].rename(columns={'BORROW_MONEY_BALANCE': 'chip_margin'})

df = pd.merge(df, m_comm, on='kline_time', how='left')
df = pd.merge(df, m_chip, on='kline_time', how='left')

print("=== 2026 Timeline Inspection ===")
print("June peak days around 2026-06-20 to 2026-07-05:")
print(df[(df['kline_time'] >= '2026-06-20') & (df['kline_time'] <= '2026-07-05')][['kline_time', 'chinext_close', 'star50_close', 'comm_etf_close', 'chip_etf_close', 'SUM_BORROW_MONEY_BALANCE', 'comm_margin', 'chip_margin']].to_string())

print("\nJuly/August trough and rebound days around 2026-07-20 to 2026-08-31:")
print(df[(df['kline_time'] >= '2026-07-20') & (df['kline_time'] <= '2026-08-31')][['kline_time', 'chinext_close', 'star50_close', 'comm_etf_close', 'chip_etf_close', 'SUM_BORROW_MONEY_BALANCE', 'comm_margin', 'chip_margin']].iloc[::3].to_string())

print("\nSeptember to October days:")
print(df[df['kline_time'] >= '2026-09-15'][['kline_time', 'chinext_close', 'star50_close', 'comm_etf_close', 'chip_etf_close', 'SUM_BORROW_MONEY_BALANCE', 'comm_margin', 'chip_margin']].to_string())
