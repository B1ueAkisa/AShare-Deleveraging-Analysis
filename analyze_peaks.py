import pandas as pd
import numpy as np

# Load merged market data
df = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/merged_market_data.csv')
df['kline_time'] = pd.to_datetime(df['kline_time'])

# Also load aggregated margin summary
df_margin = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/aggregated_margin_summary.csv')
df_margin['kline_time'] = pd.to_datetime(df_margin['TRADE_DATE'].astype(str))

merged_all = pd.merge(df, df_margin, on='kline_time', how='left')

print("--- Data Summary from 2024 to 2026 ---")
assets = ['sh_comp', 'chinext', 'star50', 'comm_etf', 'chip_etf', 'bond30_etf', 'gold_etf']
for a in assets:
    col = f'{a}_close'
    peak_val = merged_all[col].max()
    peak_date = merged_all.loc[merged_all[col].idxmax(), 'kline_time']
    df_2024 = merged_all[merged_all['kline_time'] >= '2024-01-01']
    min_2024 = df_2024[col].min()
    min_date = df_2024.loc[df_2024[col].idxmin(), 'kline_time']
    latest_val = merged_all[col].iloc[-1]
    drawdown = (latest_val - peak_val) / peak_val * 100
    print(f"Asset: {a:12s} | 2024 Low: {min_2024:.4f} ({min_date.strftime('%Y-%m-%d')}) | Peak: {peak_val:.4f} ({peak_date.strftime('%Y-%m-%d')}) | Latest: {latest_val:.4f} | Drawdown: {drawdown:.2f}%")

print("\n--- Margin Balance Peaks and Recent Trend ---")
margin_col = 'SUM_BORROW_MONEY_BALANCE'
valid_margin = merged_all.dropna(subset=[margin_col])
peak_margin = valid_margin[margin_col].max()
peak_margin_date = valid_margin.loc[valid_margin[margin_col].idxmax(), 'kline_time']
df_m_2024 = valid_margin[valid_margin['kline_time'] >= '2024-01-01']
min_margin_2024 = df_m_2024[margin_col].min()
min_margin_date = df_m_2024.loc[df_m_2024[margin_col].idxmin(), 'kline_time']
latest_complete_margin = valid_margin.iloc[-2]

print(f"Margin Low 2024: {min_margin_2024/1e12:.3f}T ({min_margin_date.strftime('%Y-%m-%d')})")
print(f"Margin Peak: {peak_margin/1e12:.3f}T ({peak_margin_date.strftime('%Y-%m-%d')})")
print(f"Latest Complete Margin: {latest_complete_margin[margin_col]/1e12:.3f}T ({latest_complete_margin['kline_time'].strftime('%Y-%m-%d')})")
print(f"Decline in Margin: {(latest_complete_margin[margin_col] - peak_margin)/1e12:.3f}T ({(latest_complete_margin[margin_col] - peak_margin)/peak_margin*100:.2f}%)")
