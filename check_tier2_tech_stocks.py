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

# Check candidate 2nd/3rd tier tech stocks mentioned by user
candidates = {
    # 光通信/算力二三线
    '300476.SZ': '胜宏科技',
    '301308.SZ': '江波龙',
    '688525.SH': '佰维存储',
    '001309.SZ': '德明利',
    '002436.SZ': '兴森科技',
    '002463.SZ': '沪电股份',
    '600183.SH': '生益科技',
    '300857.SZ': '协创数据',
    '300757.SZ': '罗博特科',
    '603083.SH': '剑桥科技',
    '002130.SZ': '沃尔核材',
    '300442.SZ': '润泽科技',
    '002156.SZ': '通富微电',
    '600584.SH': '长电科技',
    '000988.SZ': '华工科技',
    
    # 之前15大核心龙头
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

codes = list(candidates.keys())
print(f"Testing {len(codes)} tech stocks margin data...")
m_dict = info.get_margin_detail(codes, begin_date=20260901, end_date=calendar[-1])

valid_stocks = {}
for c, name in candidates.items():
    if c in m_dict and m_dict[c] is not None and not m_dict[c].empty:
        df = m_dict[c].copy()
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        df = df.sort_values('TRADE_DATE').reset_index(drop=True)
        latest_m = df.iloc[-1]['BORROW_MONEY_BALANCE'] / 1e8
        peak_m = df['BORROW_MONEY_BALANCE'].max() / 1e8
        peak_d = df.loc[df['BORROW_MONEY_BALANCE'].idxmax(), 'TRADE_DATE']
        
        # 0922 margin
        sub_0922 = df[df['TRADE_DATE'] >= '20260922']
        m_0922 = sub_0922.iloc[0]['BORROW_MONEY_BALANCE'] / 1e8 if not sub_0922.empty else latest_m
        
        # 1020 margin
        sub_1020 = df[df['TRADE_DATE'] >= '20261020']
        m_1020 = sub_1020.iloc[0]['BORROW_MONEY_BALANCE'] / 1e8 if not sub_1020.empty else latest_m
        
        valid_stocks[c] = {
            'name': name,
            'tier': '一线核心龙头' if c in list(candidates.keys())[15:] else '二三线高弹性题材',
            'latest_m': latest_m,
            'peak_m': peak_m,
            'peak_d': peak_d,
            'm_0922': m_0922,
            'm_1020': m_1020,
            'drop_from_peak_pct': (latest_m - peak_m) / peak_m * 100,
            'drop_from_1020_pct': (latest_m - m_1020) / m_1020 * 100,
            'abs_drop_from_peak_yi': latest_m - peak_m,
            'abs_drop_from_1020_yi': latest_m - m_1020
        }

df_res = pd.DataFrame.from_dict(valid_stocks, orient='index').reset_index()
df_res = df_res.rename(columns={'index': 'code'}).sort_values('latest_m', ascending=False)
print(f"Total valid stocks: {len(df_res)}")
print(df_res[['code', 'name', 'tier', 'latest_m', 'peak_m', 'drop_from_peak_pct', 'drop_from_1020_pct', 'abs_drop_from_peak_yi']].to_string())

# Save to CSV
df_res.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/expanded_30_tech_stocks_margin.csv', index=False)
