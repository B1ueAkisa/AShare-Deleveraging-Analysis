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

print("Calendar latest date:", calendar[-1])

# 1. Get all ETF codes and names
etf_info = base.get_code_info(security_type='EXTRA_ETF')
print(f"Total ETFs: {len(etf_info)}")

# 2. Get all ETF margin data from 20260901 to latest
# Let's batch query or query all ETF codes
all_etf_codes = etf_info.index.tolist()
print(f"Fetching margin details for {len(all_etf_codes)} ETFs...")

# Fetch in batches of 100 to be safe and avoid timeout
batch_size = 100
all_margins = {}
for i in range(0, len(all_etf_codes), batch_size):
    batch = all_etf_codes[i:i+batch_size]
    try:
        res = info.get_margin_detail(batch, begin_date=20260915, end_date=calendar[-1])
        if isinstance(res, dict):
            for k, v in res.items():
                if v is not None and not v.empty:
                    all_margins[k] = v
        elif isinstance(res, pd.DataFrame) and not res.empty:
            for k, group in res.groupby('MARKET_CODE'):
                all_margins[k] = group
        print(f"Batch {i//batch_size + 1}/{(len(all_etf_codes)-1)//batch_size + 1}: fetched {len(all_margins)} ETFs with margin data so far")
    except Exception as e:
        print(f"Error in batch {i}: {e}")

print(f"\nTotal ETFs with active margin trading data: {len(all_margins)}")

# Save list of ETFs with margin data
etf_margin_summary = []
for code, df in all_margins.items():
    df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
    df = df.sort_values('TRADE_DATE').reset_index(drop=True)
    symbol = etf_info.loc[code, 'symbol'] if code in etf_info.index else ''
    
    # Latest margin
    latest_row = df.iloc[-1]
    latest_date = latest_row['TRADE_DATE']
    latest_margin = latest_row['BORROW_MONEY_BALANCE'] / 1e8 # in 100M (亿)
    
    # Peak margin since 2026-09-15
    peak_idx = df['BORROW_MONEY_BALANCE'].idxmax()
    peak_row = df.iloc[peak_idx]
    peak_margin = peak_row['BORROW_MONEY_BALANCE'] / 1e8
    peak_date = peak_row['TRADE_DATE']
    
    # Margin on 2026-09-22 (start of wave 2) or earliest available
    df_w2 = df[df['TRADE_DATE'] >= '20260922']
    w2_start_margin = df_w2.iloc[0]['BORROW_MONEY_BALANCE'] / 1e8 if not df_w2.empty else latest_margin
    
    # Margin on 2026-10-20 or 2026-10-23 (market peak/turn)
    df_oct = df[df['TRADE_DATE'] >= '20261020']
    oct_margin = df_oct.iloc[0]['BORROW_MONEY_BALANCE'] / 1e8 if not df_oct.empty else latest_margin
    
    chg_from_sep22_pct = (latest_margin - w2_start_margin) / w2_start_margin * 100 if w2_start_margin > 0 else 0
    chg_from_peak_pct = (latest_margin - peak_margin) / peak_margin * 100 if peak_margin > 0 else 0
    chg_from_oct20_pct = (latest_margin - oct_margin) / oct_margin * 100 if oct_margin > 0 else 0
    
    abs_chg_from_sep22 = latest_margin - w2_start_margin
    abs_chg_from_oct20 = latest_margin - oct_margin
    
    etf_margin_summary.append({
        'code': code,
        'symbol': symbol,
        'latest_date': latest_date,
        'latest_margin_yi': round(latest_margin, 2),
        'peak_date': peak_date,
        'peak_margin_yi': round(peak_margin, 2),
        'sep22_margin_yi': round(w2_start_margin, 2),
        'oct20_margin_yi': round(oct_margin, 2),
        'chg_from_sep22_pct': round(chg_from_sep22_pct, 2),
        'chg_from_peak_pct': round(chg_from_peak_pct, 2),
        'chg_from_oct20_pct': round(chg_from_oct20_pct, 2),
        'abs_chg_from_sep22_yi': round(abs_chg_from_sep22, 2),
        'abs_chg_from_oct20_yi': round(abs_chg_from_oct20, 2)
    })

df_summary = pd.DataFrame(etf_margin_summary)
df_summary = df_summary.sort_values('latest_margin_yi', ascending=False).reset_index(drop=True)
print("\n--- TOP 30 ETFs by Latest Margin Balance ---")
print(df_summary.head(30).to_string())

df_summary.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/all_etf_margin_summary.csv', index=False)
print("Saved all_etf_margin_summary.csv successfully!")
