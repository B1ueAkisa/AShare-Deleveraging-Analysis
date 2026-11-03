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
market = ad.MarketData(calendar)

# Check peak dates and prices around June 2026 to today 2026-11-03
core_symbols = {
    '中际旭创 (300308.SZ)': '300308.SZ',
    '新易盛 (300502.SZ)': '300502.SZ',
    '天孚通信 (300394.SZ)': '300394.SZ',
    '寒武纪 (688256.SH)': '688256.SH',
    '胜宏科技 (300476.SZ)': '300476.SZ',
    '通信ETF (515880.SH)': '515880.SH',
    '科创芯片ETF (588200.SH)': '588200.SH',
    '科创半导 (588170.SH)': '588170.SH',
    '创业板指 (399006.SZ)': '399006.SZ',
    '科创50 (000688.SH)': '000688.SH',
    '上证指数 (000001.SH)': '000001.SH',
}

klines = market.query_kline(list(core_symbols.values()), begin_date=20260601, end_date=20261103, period=ad.constant.Period.day.value)

stats = []
for name, code in core_symbols.items():
    if code in klines and klines[code] is not None:
        df = klines[code].copy()
        df['date'] = pd.to_datetime(df['kline_time']).dt.strftime('%Y%m%d')
        
        # Split adjustments: 515880 was 1:2 on 2026-07-06; 588200 was 1:3 on 2026-07-21
        if code == '515880.SH':
            df.loc[df['date'] < '20260706', 'close'] /= 2.0
            df.loc[df['date'] < '20260706', 'high'] /= 2.0
        elif code == '588200.SH':
            df.loc[df['date'] < '20260721', 'close'] /= 3.0
            df.loc[df['date'] < '20260721', 'high'] /= 3.0
            
        peak_idx = df['high'].idxmax()
        peak_date = df.loc[peak_idx, 'date']
        peak_price = df.loc[peak_idx, 'high']
        
        nov03_close = df.iloc[-1]['close']
        
        # Full drop from peak
        full_drop = (nov03_close - peak_price) / peak_price * 100
        
        # Second wave drop: peak since 2026-09-15
        df_w2 = df[df['date'] >= '20260915'].copy()
        if not df_w2.empty:
            w2_peak_idx = df_w2['high'].idxmax()
            w2_peak_date = df_w2.loc[w2_peak_idx, 'date']
            w2_peak_price = df_w2.loc[w2_peak_idx, 'high']
            w2_drop = (nov03_close - w2_peak_price) / w2_peak_price * 100
        else:
            w2_drop = np.nan
            w2_peak_date = ''
            
        stats.append({
            'name': name,
            'peak_date': peak_date,
            'peak_price': round(peak_price, 3),
            'nov03_close': round(nov03_close, 3),
            'total_drop_pct': round(full_drop, 2),
            'w2_peak_date': w2_peak_date,
            'w2_drop_pct': round(w2_drop, 2)
        })

df_summary = pd.DataFrame(stats)
print("=== Peak to 2026-11-03 Crash Metrics ===")
print(df_summary.to_string())
