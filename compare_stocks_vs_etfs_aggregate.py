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

# Top Tech Core Stocks
tech_stocks = {
    '300308.SZ': '中际旭创',
    '300502.SZ': '新易盛',
    '300394.SZ': '天孚通信',
    '688256.SH': '寒武纪',
    '688981.SH': '中芯国际',
    '688041.SH': '海光信息',
    '688012.SH': '中微公司',
    '002371.SZ': '北方华创',
    '603501.SH': '韦尔股份',
    '603986.SH': '兆易创新',
    '688008.SH': '澜起科技',
    '601138.SH': '工业富联',
    '002475.SZ': '立讯精密',
    '000977.SZ': '浪潮信息',
    '002230.SZ': '科大讯飞'
}

stock_codes = list(tech_stocks.keys())
print(f"Fetching margin details for {len(stock_codes)} top tech stocks...")

stock_margins = info.get_margin_detail(stock_codes, begin_date=20260901, end_date=calendar[-1])

# Process stock margins
stock_records = []
for code in stock_codes:
    if code in stock_margins and stock_margins[code] is not None and not stock_margins[code].empty:
        df = stock_margins[code].copy()
        df['code'] = code
        df['name'] = tech_stocks[code]
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        stock_records.append(df)

df_all_stocks = pd.concat(stock_records, ignore_index=True)
df_all_stocks['margin_yi'] = df_all_stocks['BORROW_MONEY_BALANCE'] / 1e8

# Daily sum for tech stocks
daily_stocks = df_all_stocks.groupby('TRADE_DATE')['margin_yi'].agg(['sum', 'count']).reset_index()
daily_stocks.columns = ['date', 'stock_total_margin_yi', 'stock_count']

# Now let's fetch daily margin for tech ETFs:
# Tech Broad-based: 588000.SH (科创50), 159915.SZ (创业板), 159949.SZ (创50), 588080.SH (科创板50), 588300.SH (双创50), 159781.SZ (双创50)
# Tech Sector: 588200.SH (科创芯片), 159995.SZ (芯片ETF), 512480.SH (半导体), 588170.SH (科创半导体), 515880.SH (通信ETF), 512720.SH (计算机ETF), 515230.SH (软件ETF), 159819.SZ (人工智能)
target_tech_etfs = [
    '588000.SH', '159915.SZ', '159949.SZ', '588080.SH', '588300.SH', '159781.SZ',
    '588200.SH', '159995.SZ', '512480.SH', '588170.SH', '515880.SH', '512720.SH', '515230.SH', '159819.SZ'
]

etf_margins = info.get_margin_detail(target_tech_etfs, begin_date=20260901, end_date=calendar[-1])
etf_records = []
for code in target_tech_etfs:
    if code in etf_margins and etf_margins[code] is not None and not etf_margins[code].empty:
        df = etf_margins[code].copy()
        df['code'] = code
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        etf_records.append(df)

df_all_etfs = pd.concat(etf_records, ignore_index=True)
df_all_etfs['margin_yi'] = df_all_etfs['BORROW_MONEY_BALANCE'] / 1e8

# Daily sum for tech ETFs
daily_etfs = df_all_etfs.groupby('TRADE_DATE')['margin_yi'].agg(['sum', 'count']).reset_index()
daily_etfs.columns = ['date', 'etf_total_margin_yi', 'etf_count']

# Also separate Tech Broad-based vs Tech Sector ETFs
broad_codes = ['588000.SH', '159915.SZ', '159949.SZ', '588080.SH', '588300.SH', '159781.SZ']
sector_codes = [c for c in target_tech_etfs if c not in broad_codes]

daily_broad = df_all_etfs[df_all_etfs['code'].isin(broad_codes)].groupby('TRADE_DATE')['margin_yi'].sum().reset_index()
daily_broad.columns = ['date', 'etf_broad_margin_yi']

daily_sector = df_all_etfs[df_all_etfs['code'].isin(sector_codes)].groupby('TRADE_DATE')['margin_yi'].sum().reset_index()
daily_sector.columns = ['date', 'etf_sector_margin_yi']

# Merge everything by date
merged = pd.merge(daily_stocks, daily_etfs, on='date', how='inner')
merged = pd.merge(merged, daily_broad, on='date', how='left')
merged = pd.merge(merged, daily_sector, on='date', how='left')
merged = merged.sort_values('date').reset_index(drop=True)

print("\n=== 科技核心个股总融资额 vs 科技ETF总融资额每日明细 (2026-09-22 至今) ===")
sub = merged[merged['date'] >= '20260922'].copy()
print(sub.to_string())

# Save daily comparison
merged.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/daily_stocks_vs_etfs_tech_margin.csv', index=False)

# Print individual stock status
print("\n=== 15大科技权重个股融资余额明细 (最新 vs 10月峰值) ===")
stock_stat_list = []
for code in stock_codes:
    sub_s = df_all_stocks[df_all_stocks['code'] == code].sort_values('TRADE_DATE')
    if not sub_s.empty:
        name = tech_stocks[code]
        latest_val = sub_s.iloc[-1]['margin_yi']
        peak_val = sub_s['margin_yi'].max()
        peak_d = sub_s.loc[sub_s['margin_yi'].idxmax(), 'TRADE_DATE']
        
        # 10月20日融资额
        sub_oct = sub_s[sub_s['TRADE_DATE'] >= '20261020']
        oct_val = sub_oct.iloc[0]['margin_yi'] if not sub_oct.empty else latest_val
        
        drop_from_peak_pct = (latest_val - peak_val) / peak_val * 100
        drop_from_oct_pct = (latest_val - oct_val) / oct_val * 100
        abs_drop_from_peak = latest_val - peak_val
        
        stock_stat_list.append({
            'code': code,
            'name': name,
            'latest_date': sub_s.iloc[-1]['TRADE_DATE'],
            'latest_margin_yi': round(latest_val, 2),
            'peak_date': peak_d,
            'peak_margin_yi': round(peak_val, 2),
            'oct20_margin_yi': round(oct_val, 2),
            'drop_from_peak_pct': round(drop_from_peak_pct, 2),
            'drop_from_oct_pct': round(drop_from_oct_pct, 2),
            'abs_drop_from_peak_yi': round(abs_drop_from_peak, 2)
        })

df_stock_stats = pd.DataFrame(stock_stat_list).sort_values('latest_margin_yi', ascending=False).reset_index(drop=True)
print(df_stock_stats.to_string())
df_stock_stats.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/tech_stocks_margin_stats.csv', index=False)
