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

target_etfs = {
    '588000.SH': '科创50 ETF',
    '159915.SZ': '创业板 ETF',
    '159949.SZ': '创业板50 ETF',
    '588200.SH': '科创芯片 ETF',
    '159995.SZ': '芯片 ETF',
    '515880.SH': '通信 ETF',
    '510300.SH': '沪深300 ETF',
    '510050.SH': '上证50 ETF'
}

etf_codes = list(target_etfs.keys())
print("Fetching K-lines and margin details for key ETFs...")
klines = market.query_kline(etf_codes, begin_date=20260901, end_date=calendar[-1], period=ad.constant.Period.day.value)
margins = info.get_margin_detail(etf_codes, begin_date=20260901, end_date=calendar[-1])

results = []

for code, name in target_etfs.items():
    if code in klines and code in margins:
        df_k = klines[code].copy()
        df_k['date'] = pd.to_datetime(df_k['kline_time']).dt.strftime('%Y%m%d')
        df_k = df_k.sort_values('date').reset_index(drop=True)
        
        df_m = margins[code].copy()
        df_m['date'] = df_m['TRADE_DATE'].astype(str)
        df_m = df_m.sort_values('date').reset_index(drop=True)
        
        merged = pd.merge(df_k[['date', 'close']], df_m[['date', 'BORROW_MONEY_BALANCE']], on='date', how='inner')
        merged['margin_yi'] = merged['BORROW_MONEY_BALANCE'] / 1e8
        
        # 1. Period A: 2026-09-22 to latest
        sub_sep = merged[merged['date'] >= '20260922'].copy()
        if not sub_sep.empty:
            p_start_sep = sub_sep.iloc[0]['close']
            p_end = sub_sep.iloc[-1]['close']
            p_ret_sep = (p_end - p_start_sep) / p_start_sep * 100
            
            m_start_sep = sub_sep.iloc[0]['margin_yi']
            m_end = sub_sep.iloc[-1]['margin_yi']
            m_ret_sep = (m_end - m_start_sep) / m_start_sep * 100
            
            # Expected margin if it dropped/moved with price
            m_expected_sep = m_start_sep * (1.0 + p_ret_sep / 100.0)
            excess_m_sep = m_end - m_expected_sep
            excess_pct_sep = m_ret_sep - p_ret_sep
            
            # 2. Period B: Oct Drop (from peak close since 10.08 to latest)
            sub_oct = merged[merged['date'] >= '20261008'].copy()
            peak_idx = sub_oct['close'].idxmax()
            p_peak_oct = sub_oct.loc[peak_idx, 'close']
            peak_date = sub_oct.loc[peak_idx, 'date']
            m_at_peak_oct = sub_oct.loc[peak_idx, 'margin_yi']
            
            p_drop_oct = (p_end - p_peak_oct) / p_peak_oct * 100
            m_chg_oct = (m_end - m_at_peak_oct) / m_at_peak_oct * 100
            
            # If margin dropped with price:
            m_expected_oct = m_at_peak_oct * (1.0 + p_drop_oct / 100.0)
            excess_m_oct = m_end - m_expected_oct
            excess_pct_oct = m_chg_oct - p_drop_oct
            
            results.append({
                'code': code,
                'name': name,
                # 0922-latest
                'p_chg_since_0922_pct': round(p_ret_sep, 2),
                'm_chg_since_0922_pct': round(m_ret_sep, 2),
                'excess_pct_since_0922': round(excess_pct_sep, 2),
                'excess_val_since_0922_yi': round(excess_m_sep, 2),
                # Oct drop to latest
                'peak_date': peak_date,
                'p_drop_oct_pct': round(p_drop_oct, 2),
                'm_chg_oct_pct': round(m_chg_oct, 2),
                'excess_pct_oct': round(excess_pct_oct, 2),
                'm_at_peak_oct_yi': round(m_at_peak_oct, 2),
                'latest_margin_yi': round(m_end, 2),
                'm_expected_oct_yi': round(m_expected_oct, 2),
                'excess_val_oct_yi': round(excess_m_oct, 2)
            })

df_excess = pd.DataFrame(results)
print("\n=== ETF 超额融资扩张测算表 (理论价格匹配 vs 实际融资额) ===")
print(df_excess[['code', 'name', 'p_drop_oct_pct', 'm_chg_oct_pct', 'excess_pct_oct', 'latest_margin_yi', 'm_expected_oct_yi', 'excess_val_oct_yi']].to_string())

df_excess.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/etf_excess_margin_expansion.csv', index=False)
