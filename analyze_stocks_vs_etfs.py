import pandas as pd
import numpy as np

stocks = {
    '300502.SZ': '新易盛',
    '300308.SZ': '中际旭创',
    '300394.SZ': '天孚通信',
    '688256.SH': '寒武纪',
    '688981.SH': '中芯国际',
    '688012.SH': '中微公司',
    '688041.SH': '海光信息'
}

etfs = {
    '515880.SH': '通信ETF',
    '588200.SH': '科创芯片ETF'
}

data = {}

for code, name in {**stocks, **etfs}.items():
    prefix = 'stock' if code in stocks else 'margin'
    k_prefix = 'stock_kline' if code in stocks else 'kline'
    
    # margin
    if code in stocks:
        m_path = rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/stock_margin_{code}.csv'
    else:
        m_path = rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_{code}.csv'
        
    df_m = pd.read_csv(m_path)
    df_m['TRADE_DATE'] = df_m['TRADE_DATE'].astype(str)
    df_m['date'] = pd.to_datetime(df_m['TRADE_DATE'])
    df_m = df_m.sort_values('date').reset_index(drop=True)
    
    # kline
    k_path = rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/{k_prefix}_{code}.csv'
    df_k = pd.read_csv(k_path)
    df_k['date'] = pd.to_datetime(df_k['kline_time'])
    df_k = df_k.sort_values('date').reset_index(drop=True)
    
    merged = pd.merge(df_k[['date', 'close', 'open', 'high', 'low', 'amount']], 
                      df_m[['date', 'BORROW_MONEY_BALANCE', 'PURCH_WITH_BORROW_MONEY', 'REPAYMENT_OF_BORROW_MONEY']], 
                      on='date', how='inner')
    data[code] = merged

# Function to calculate wave stats
def analyze_wave(df_sub, code, name, wave_name):
    if df_sub.empty:
        return None
    start = df_sub.iloc[0]
    end = df_sub.iloc[-1]
    
    p_start, p_end = start['close'], end['close']
    p_drop = (p_end - p_start) / p_start * 100
    
    m_start, m_end = start['BORROW_MONEY_BALANCE'], end['BORROW_MONEY_BALANCE']
    m_drop = (m_end - m_start) / m_start * 100
    
    # elasticity: delta_m% / delta_p%
    elasticity = m_drop / p_drop if p_drop != 0 else np.nan
    
    return {
        '波段': wave_name,
        '代码': code,
        '名称': name,
        '起始日期': start['date'].strftime('%Y-%m-%d'),
        '截止日期': end['date'].strftime('%Y-%m-%d'),
        '起始股价/净值': round(p_start, 2),
        '截止股价/净值': round(p_end, 2),
        '价格跌幅%': round(p_drop, 2),
        '起始融资余额(亿)': round(m_start / 1e8, 2),
        '截止融资余额(亿)': round(m_end / 1e8, 2),
        '融资余额变动%': round(m_drop, 2),
        '去杠杆弹性(融资/价格)': round(elasticity, 2)
    }

results_w1 = []
results_w2 = []
results_oct_rush = []

for code, name in {**stocks, **etfs}.items():
    df_s = data[code]
    
    # Wave 1: 2026-06-25 to 2026-07-31
    sub_w1 = df_s[(df_s['date'] >= '2026-06-25') & (df_s['date'] <= '2026-07-31')].sort_values('date')
    r1 = analyze_wave(sub_w1, code, name, '第一波 (7月波: 06.25-07.31)')
    if r1: results_w1.append(r1)
    
    # Wave 2: 2026-09-22 to latest available
    sub_w2 = df_s[(df_s['date'] >= '2026-09-22')].sort_values('date')
    r2 = analyze_wave(sub_w2, code, name, '第二波 (10月波: 09.22-最新)')
    if r2: results_w2.append(r2)
    
    # Oct rush: 2026-10-23 to latest available
    sub_rush = df_s[(df_s['date'] >= '2026-10-23')].sort_values('date')
    r3 = analyze_wave(sub_rush, code, name, '10月下旬急跌 (10.23-最新)')
    if r3: results_oct_rush.append(r3)

df_res_w1 = pd.DataFrame(results_w1)
df_res_w2 = pd.DataFrame(results_w2)
df_res_rush = pd.DataFrame(results_oct_rush)

print("=== 第一波 (7月波) 个股 vs ETF 表现 ===")
print(df_res_w1[['代码', '名称', '价格跌幅%', '起始融资余额(亿)', '截止融资余额(亿)', '融资余额变动%', '去杠杆弹性(融资/价格)']].to_string())

print("\n=== 第二波 (10月波) 个股 vs ETF 表现 ===")
print(df_res_w2[['代码', '名称', '价格跌幅%', '起始融资余额(亿)', '截止融资余额(亿)', '融资余额变动%', '去杠杆弹性(融资/价格)']].to_string())

print("\n=== 10月下旬急跌 (10.23-最新) 个股 vs ETF 表现 ===")
print(df_res_rush[['代码', '名称', '价格跌幅%', '起始融资余额(亿)', '截止融资余额(亿)', '融资余额变动%', '去杠杆弹性(融资/价格)']].to_string())

# Save to CSV
combined = pd.concat([df_res_w1, df_res_w2, df_res_rush], ignore_index=True)
combined.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/stocks_vs_etfs_margin_analysis.csv', index=False)
