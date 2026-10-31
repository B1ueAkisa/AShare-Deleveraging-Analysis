import pandas as pd
import numpy as np

codes = {
    'sh_comp': '000001.SH',
    'chinext': '399006.SZ',
    'star50': '000688.SH',
    'comm_etf': '515880.SH',
    'chip_etf': '588200.SH',
    'bond30_etf': '511090.SH',
    'gold_etf': '518880.SH'
}

merged = None
for name, code in codes.items():
    df = pd.read_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_{code}.csv')
    df['kline_time'] = pd.to_datetime(df['kline_time'])
    df = df[['kline_time', 'close', 'open', 'high', 'low', 'amount']].copy()
    df.columns = ['kline_time', f'{name}_close', f'{name}_open', f'{name}_high', f'{name}_low', f'{name}_amount']
    if merged is None:
        merged = df
    else:
        merged = pd.merge(merged, df, on='kline_time', how='outer')

merged = merged.sort_values('kline_time').reset_index(drop=True)
merged.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/merged_market_data.csv', index=False)

# Let's inspect the recent peak, recent trough, and yesterday's drop (2026-10-29 / 2026-10-30)
recent = merged[merged['kline_time'] >= '2026-09-01'].copy()
print("--- Recent 10 trading days closes ---")
cols_to_show = ['kline_time'] + [f'{c}_close' for c in codes.keys()]
print(recent[cols_to_show].tail(10).to_string())

# Check 30-year bond drop on yesterday (2026-10-30) and previous day
print("\n--- 30-Year Bond ETF (511090.SH) recent changes ---")
recent['bond30_chg'] = recent['bond30_etf_close'].pct_change() * 100
recent['gold_chg'] = recent['gold_etf_close'].pct_change() * 100
recent['comm_chg'] = recent['comm_etf_close'].pct_change() * 100
recent['chip_chg'] = recent['chip_etf_close'].pct_change() * 100
recent['chinext_chg'] = recent['chinext_close'].pct_change() * 100
recent['star50_chg'] = recent['star50_close'].pct_change() * 100
print(recent[['kline_time', 'bond30_etf_close', 'bond30_chg', 'gold_etf_close', 'gold_chg', 'chinext_chg', 'star50_chg', 'comm_chg', 'chip_chg']].tail(6).to_string())
