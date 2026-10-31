import pandas as pd
import numpy as np

# Load merged data
df_market = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/merged_market_data.csv')
df_market['kline_time'] = pd.to_datetime(df_market['kline_time'])

df_margin = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/aggregated_margin_summary.csv')
df_margin['kline_time'] = pd.to_datetime(df_margin['TRADE_DATE'].astype(str))

# Fix 2026-10-30 incomplete margin: since only SSE is available, estimate total based on SSE drop or use 2026-10-29
# SSE drop on 10-30 was -192.87亿. SZSE typically drops proportionally ~160亿.
# Let's set 2026-10-29 as the definitive complete official margin day, or 10-30 adjusted.
df_margin_complete = df_margin[df_margin['TRADE_DATE'] < 20261030].copy()
latest_full_m = df_margin_complete.iloc[-1]['SUM_BORROW_MONEY_BALANCE'] # 2.3567T

df = pd.merge(df_market, df_margin, on='kline_time', how='inner').sort_values('kline_time').reset_index(drop=True)

# ETF margins
m_comm = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_515880.SH.csv')
m_comm['kline_time'] = pd.to_datetime(m_comm['TRADE_DATE'].astype(str))
df = pd.merge(df, m_comm[['kline_time', 'BORROW_MONEY_BALANCE']].rename(columns={'BORROW_MONEY_BALANCE': 'comm_margin'}), on='kline_time', how='left')

m_chip = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_588200.SH.csv')
m_chip['kline_time'] = pd.to_datetime(m_chip['TRADE_DATE'].astype(str))
df = pd.merge(df, m_chip[['kline_time', 'BORROW_MONEY_BALANCE']].rename(columns={'BORROW_MONEY_BALANCE': 'chip_margin'}), on='kline_time', how='left')

def calc_wave_metrics(df_sub, name):
    start_row = df_sub.iloc[0]
    end_row = df_sub.iloc[-1]
    days = len(df_sub)
    
    # ChiNext
    cy_start = start_row['chinext_close']
    cy_end = end_row['chinext_close']
    cy_drop = (cy_end - cy_start) / cy_start * 100
    cy_vel = cy_drop / (days - 1)
    
    # STAR 50
    star_start = start_row['star50_close']
    star_end = end_row['star50_close']
    star_drop = (star_end - star_start) / star_start * 100
    star_vel = star_drop / (days - 1)
    
    # Comm ETF (515880)
    comm_start = start_row['comm_etf_close']
    comm_end = end_row['comm_etf_close']
    comm_drop = (comm_end - comm_start) / comm_start * 100
    comm_vel = comm_drop / (days - 1)
    
    # Chip ETF (588200)
    chip_start = start_row['chip_etf_close']
    chip_end = end_row['chip_etf_close']
    chip_drop = (chip_end - chip_start) / chip_start * 100
    chip_vel = chip_drop / (days - 1)
    
    # Total Margin (use complete day 2026-10-29 if end_row is 10-30)
    m_start = start_row['SUM_BORROW_MONEY_BALANCE']
    if end_row['kline_time'] == pd.to_datetime('2026-10-30'):
        # row of 2026-10-29
        row_1029 = df_sub[df_sub['kline_time'] == '2026-10-29'].iloc[0]
        m_end = row_1029['SUM_BORROW_MONEY_BALANCE']
        m_end_label = '至10.29双所全量'
    else:
        m_end = end_row['SUM_BORROW_MONEY_BALANCE']
        m_end_label = '完整双所'
        
    m_drop = (m_end - m_start) / m_start * 100
    m_diff_billion = (m_end - m_start) / 1e8
    
    # Comm Margin (515880 has full 10-30 data as it is SSE)
    cm_start = start_row['comm_margin']
    cm_end = end_row['comm_margin']
    cm_drop = (cm_end - cm_start) / cm_start * 100 if pd.notnull(cm_start) and cm_start > 0 else np.nan
    
    # Chip Margin (588200 has full 10-30 data as it is SSE)
    chm_start = start_row['chip_margin']
    chm_end = end_row['chip_margin']
    chm_drop = (chm_end - chm_start) / chm_start * 100 if pd.notnull(chm_start) and chm_start > 0 else np.nan
    
    return {
        '波段划分': name,
        '起始日期': start_row['kline_time'].strftime('%Y-%m-%d'),
        '截止日期': end_row['kline_time'].strftime('%Y-%m-%d'),
        '交易天数': days,
        '创业板指跌幅%': round(cy_drop, 2),
        '创业板日均跌速%': round(cy_vel, 2),
        '通信ETF跌幅%': round(comm_drop, 2),
        '通信ETF日均跌速%': round(comm_vel, 2),
        '科创50跌幅%': round(star_drop, 2),
        '科创50日均跌速%': round(star_vel, 2),
        '科创芯片ETF跌幅%': round(chip_drop, 2),
        '科创芯片日均跌速%': round(chip_vel, 2),
        '全市场融资变化(亿元)': round(m_diff_billion, 1),
        '全市场融资降幅%': round(m_drop, 2),
        '通信ETF融资变化%': round(cm_drop, 2),
        '科创芯片融资变化%': round(chm_drop, 2)
    }

w1 = df[(df['kline_time'] >= '2026-06-25') & (df['kline_time'] <= '2026-07-31')]
w2_rebound = df[(df['kline_time'] >= '2026-09-22') & (df['kline_time'] <= '2026-10-30')]
w2_oct = df[(df['kline_time'] >= '2026-09-30') & (df['kline_time'] <= '2026-10-30')]
w2_late_oct = df[(df['kline_time'] >= '2026-10-23') & (df['kline_time'] <= '2026-10-30')]
# Full cycle for reference
w_full = df[(df['kline_time'] >= '2026-06-25') & (df['kline_time'] <= '2026-10-30')]

res = [
    calc_wave_metrics(w1, '第一波：7月完整去杠杆踩踏波 (06.25 - 07.31)'),
    calc_wave_metrics(w2_rebound, '第二波：9月高点至10月底主跌浪 (09.22 - 10.30)'),
    calc_wave_metrics(w2_oct, '第二波：国庆节后流动性收紧波 (09.30 - 10.30)'),
    calc_wave_metrics(w2_late_oct, '第二波极速冲刺：10月下旬踩踏浪 (10.23 - 10.30)'),
    calc_wave_metrics(w_full, '全波段回顾：6月底峰值至10月底 (06.25 - 10.30)')
]

res_table = pd.DataFrame(res)
res_table.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/two_waves_comparison.csv', index=False)
print("=== 两波下跌核心量化对比矩阵 (精准修正版) ===")
print(res_table.to_string())
