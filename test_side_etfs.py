import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd
import numpy as np

config.init_amazing_data()
base = ad.BaseData()
calendar = base.get_calendar()
info = ad.InfoData()
market = ad.MarketData(calendar)

# Target side ETFs to test:
# 1. 561980.SH - 芯片设备 (Semiconductor Equipment)
# 2. 588290.SH - 芯片科创 (STAR Chip Hua'an)
# 3. 159995.SZ - 芯片ETF (Semiconductor Chip SZ)
# 4. 588000.SH - 科创50 ETF
# 5. 159949.SZ - 创业板50 ETF
# 6. 159915.SZ - 创业板 ETF
# 7. 515050.SH - 5G通信 ETF
side_etfs = {
    '561980.SH': '芯片设备ETF',
    '588290.SH': '芯片科创ETF',
    '159995.SZ': '芯片ETF',
    '588000.SH': '科创50ETF',
    '159949.SZ': '创业50ETF',
    '159915.SZ': '创业板ETF',
    '515050.SH': '5G通信ETF'
}

codes = list(side_etfs.keys())
print("Fetching K-lines for side ETFs...")
klines = market.query_kline(codes, begin_date=20260501, end_date=calendar[-1], period=ad.constant.Period.day.value)

print("Fetching Margin Details for side ETFs...")
margins = info.get_margin_detail(codes, begin_date=20260501, end_date=calendar[-1])

results = []
for code, name in side_etfs.items():
    if code in klines and code in margins:
        df_k = klines[code].copy()
        df_k['date'] = pd.to_datetime(df_k['kline_time'])
        
        df_m = margins[code].copy()
        df_m['date'] = pd.to_datetime(df_m['TRADE_DATE'].astype(str))
        
        m = pd.merge(df_k[['date', 'close']], df_m[['date', 'BORROW_MONEY_BALANCE']], on='date', how='inner')
        m = m.sort_values('date').reset_index(drop=True)
        
        # Wave 2: 2026-09-22 to latest
        sub_w2 = m[m['date'] >= '2026-09-22'].copy()
        if not sub_w2.empty:
            p_start, p_end = sub_w2['close'].iloc[0], sub_w2['close'].iloc[-1]
            p_drop = (p_end - p_start) / p_start * 100
            
            m_start, m_end = sub_w2['BORROW_MONEY_BALANCE'].iloc[0], sub_w2['BORROW_MONEY_BALANCE'].iloc[-1]
            m_drop = (m_end - m_start) / m_start * 100
            
            # Check peak in wave 2 margin
            m_peak = sub_w2['BORROW_MONEY_BALANCE'].max()
            m_peak_date = sub_w2.loc[sub_w2['BORROW_MONEY_BALANCE'].idxmax(), 'date'].strftime('%m-%d')
            
            results.append({
                '代码': code,
                '名称': name,
                '第二波价格跌幅%': round(p_drop, 2),
                '第二波起始融资(亿)': round(m_start/1e8, 2),
                '第二波最新融资(亿)': round(m_end/1e8, 2),
                '第二波融资变动%': round(m_drop, 2),
                '第二波融资峰值(亿)': round(m_peak/1e8, 2),
                '峰值日期': m_peak_date
            })

df_res = pd.DataFrame(results)
print("\n=== Side ETFs (细分及宽基ETF) 第二波表现实测 ===")
print(df_res.to_string())
df_res.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/side_etfs_test.csv', index=False)
