import pandas as pd

df = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/merged_market_data.csv')
df['kline_time'] = pd.to_datetime(df['kline_time'])

# inspect comm_etf and chip_etf kline from 2026-01-01 to 2026-10-30
df_2026 = df[df['kline_time'] >= '2026-01-01'].copy()
print("comm_etf 2026 sample:")
print(df_2026[['kline_time', 'comm_etf_close', 'chip_etf_close', 'chinext_close', 'star50_close']].iloc[::15])
