import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd
import numpy as np

config.init_amazing_data()
base = ad.BaseData()
calendar = base.get_calendar()
market = ad.MarketData(calendar)
info = ad.InfoData()

# Load candidate ETFs from CSV
df_cand = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/semi_equipment_material_etfs_list.csv', index_col=0)

# Filter out non-relevant ones (e.g. 碳中和基, 医疗设备, 电网设备, 建筑材料)
exclude = ['碳中和基', '医疗设备', '电网设备', '建筑材料', '新材料']
df_cand = df_cand[~df_cand['symbol'].apply(lambda s: any(e in str(s) for e in exclude))]

# Filter listed before 2026
df_cand = df_cand[df_cand['list_day'] < 20260101]

codes = df_cand.index.tolist()
print(f"Candidate semiconductor/equipment/material ETFs: {len(codes)}")
print(df_cand[['symbol', 'list_day']].to_string())

# Fetch K-lines from 20260101 to 20261030
klines = market.query_kline(codes, begin_date=20260101, end_date=calendar[-1], period=ad.constant.Period.day.value)

# Fetch Margins
margins = info.get_margin_detail(codes, begin_date=20260901, end_date=calendar[-1])

results = []
for code, row in df_cand.iterrows():
    if code in klines and klines[code] is not None and not klines[code].empty:
        df_k = klines[code].copy()
        df_k['date'] = pd.to_datetime(df_k['kline_time'])
        df_k = df_k.sort_values('date').reset_index(drop=True)
        
        # Check if code has data on 2026-01-05
        p_ytd_start = df_k.iloc[0]['close']
        p_latest = df_k.iloc[-1]['close']
        p_peak = df_k['close'].max()
        peak_date = df_k.loc[df_k['close'].idxmax(), 'date'].strftime('%m-%d')
        
        # Note: if there was a split (e.g. 588200), handle or note it
        # Let's inspect price jump
        ytd_ret = (p_latest - p_ytd_start) / p_ytd_start * 100
        peak_gain = (p_peak - p_ytd_start) / p_ytd_start * 100
        
        # Wave 2: 2026-09-22 to 2026-10-30
        sub_w2 = df_k[df_k['date'] >= '2026-09-22']
        if not sub_w2.empty:
            w2_start = sub_w2.iloc[0]['close']
            w2_drop = (p_latest - w2_start) / w2_start * 100
        else:
            w2_drop = np.nan
            
        # Margin change in wave 2
        m_change_pct = np.nan
        m_latest_val = np.nan
        if code in margins and margins[code] is not None and not margins[code].empty:
            df_m = margins[code].copy()
            df_m['date'] = pd.to_datetime(df_m['TRADE_DATE'].astype(str))
            df_m = df_m.sort_values('date').reset_index(drop=True)
            sub_m_w2 = df_m[df_m['date'] >= '2026-09-22']
            if not sub_m_w2.empty:
                m_start = sub_m_w2.iloc[0]['BORROW_MONEY_BALANCE']
                m_end = sub_m_w2.iloc[-1]['BORROW_MONEY_BALANCE']
                m_change_pct = (m_end - m_start) / m_start * 100
                m_latest_val = m_end / 1e8
        
        results.append({
            '代码': code,
            '名称': row['symbol'],
            '上市日期': int(row['list_day']),
            '年初收盘': round(p_ytd_start, 3),
            '年内最高': round(p_peak, 3),
            '最高日期': peak_date,
            '最新收盘': round(p_latest, 3),
            '年内最大涨幅%': round(peak_gain, 2),
            '本年迄今涨幅%': round(ytd_ret, 2),
            '第二波(10月)跌幅%': round(w2_drop, 2),
            '最新融资(亿)': round(m_latest_val, 2) if pd.notnull(m_latest_val) else np.nan,
            '第二波融资变动%': round(m_change_pct, 2) if pd.notnull(m_change_pct) else np.nan
        })

df_sorted = pd.DataFrame(results)
# Sort by 年内最大涨幅% or 本年迄今涨幅%
df_sorted = df_sorted.sort_values('年内最大涨幅%', ascending=False).reset_index(drop=True)
print("\n=== 全部半导体/材料/设备 ETF 涨幅排行榜 (2026年) ===")
print(df_sorted.to_string())
df_sorted.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/semi_materials_equipment_ranked.csv', index=False)
