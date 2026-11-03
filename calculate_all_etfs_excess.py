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

# Load all ETF margin summary to get all equity ETFs
df_etf = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/all_etf_margin_summary.csv')

# Filter out non-equity (exclude gold, bonds, money market, cross-border overseas)
def is_equity_etf(sym):
    sym = str(sym)
    if any(k in sym for k in ['黄金', '白银', '豆粕', '有色', '商品', '债', '国债', '信用债', '纳斯达克', '标普', '纳指', '德国', '日经', '法国']):
        return False
    return True

df_equity = df_etf[df_etf['symbol'].apply(is_equity_etf)].copy()
equity_codes = df_equity['code'].tolist()
print(f"Total equity ETFs with margin data: {len(equity_codes)}")

# Query K-lines from 20261008 to latest for all equity ETFs
klines = market.query_kline(equity_codes, begin_date=20261008, end_date=calendar[-1], period=ad.constant.Period.day.value)
margins = info.get_margin_detail(equity_codes, begin_date=20261008, end_date=calendar[-1])

records = []
for code in equity_codes:
    sym = df_equity.loc[df_equity['code'] == code, 'symbol'].values[0]
    if code in klines and code in margins and klines[code] is not None and margins[code] is not None:
        df_k = klines[code].copy()
        df_m = margins[code].copy()
        if not df_k.empty and not df_m.empty:
            df_k['date'] = pd.to_datetime(df_k['kline_time']).dt.strftime('%Y%m%d')
            df_m['date'] = df_m['TRADE_DATE'].astype(str)
            merged = pd.merge(df_k[['date', 'close']], df_m[['date', 'BORROW_MONEY_BALANCE']], on='date', how='inner')
            if len(merged) >= 2:
                merged['margin_yi'] = merged['BORROW_MONEY_BALANCE'] / 1e8
                p_start = merged.iloc[0]['close'] # 10.08
                p_end = merged.iloc[-1]['close'] # latest
                p_ret = (p_end - p_start) / p_start * 100
                
                m_start = merged.iloc[0]['margin_yi']
                m_end = merged.iloc[-1]['margin_yi']
                m_ret = (m_end - m_start) / m_start * 100 if m_start > 0 else 0
                
                m_expected = m_start * (1.0 + p_ret / 100.0)
                excess_val = m_end - m_expected
                excess_pct = m_ret - p_ret
                actual_chg_val = m_end - m_start
                
                records.append({
                    'code': code,
                    'symbol': sym,
                    'p_ret_oct_pct': p_ret,
                    'm_start_yi': m_start,
                    'm_end_yi': m_end,
                    'm_expected_yi': m_expected,
                    'actual_chg_val_yi': actual_chg_val,
                    'excess_val_yi': excess_val,
                    'excess_pct': excess_pct
                })

df_all_excess = pd.DataFrame(records)
print("\n--- Summary of Equity ETFs Excess Margin Expansion (10.08 to Latest) ---")
print(f"Total valid analyzed equity ETFs: {len(df_all_excess)}")

# Category breakdown
def get_broad_cat(sym):
    sym = str(sym)
    if any(k in sym for k in ['科创', '双创', '创业板', '创50']):
        return '双创成长宽基'
    if any(k in sym for k in ['半导体', '芯片', '集成电路', '通信', '5G', '软件', '计算机', '人工智能', 'AI', '算力', '机器人', '电子', '大数据', '云计算']):
        return '科技核心行业/主题'
    if any(k in sym for k in ['300', '沪深300', '50ETF', '上证50', 'A500', '中证A500', 'A50', '500ETF', '1000ETF', '2000ETF']):
        return '大盘/中小盘传统宽基'
    if any(k in sym for k in ['证券', '券商', '银行', '保险', '金融']):
        return '大金融类'
    return '其他行业/主题'

df_all_excess['category'] = df_all_excess['symbol'].apply(get_broad_cat)

cat_sum = df_all_excess.groupby('category').agg(
    count=('code', 'count'),
    m_start_sum=('m_start_yi', 'sum'),
    m_end_sum=('m_end_yi', 'sum'),
    actual_net_inflow=('actual_chg_val_yi', 'sum'),
    expected_m_sum=('m_expected_yi', 'sum'),
    total_excess_margin=('excess_val_yi', 'sum')
).reset_index()

cat_sum = cat_sum.sort_values('total_excess_margin', ascending=False)
print(cat_sum.to_string())

# Total across all equity ETFs
total_excess = df_all_excess['excess_val_yi'].sum()
total_actual_inflow = df_all_excess['actual_chg_val_yi'].sum()
print(f"\n==========================================")
print(f"全市场股票型 ETF 实际净流入融资额: {total_actual_inflow:.2f} 亿元")
print(f"全市场股票型 ETF 超额融资扩张总量: {total_excess:.2f} 亿元")
print(f"==========================================")
