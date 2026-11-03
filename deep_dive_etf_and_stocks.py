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

# Load all ETF margin summary
df_etf = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/all_etf_margin_summary.csv')

# Let's inspect A500 specifically
a500_mask = df_etf['symbol'].str.contains('A500|500A', case=False, na=False)
print("=== A500 ETFs in Database ===")
print(df_etf[a500_mask][['code', 'symbol', 'latest_margin_yi', 'oct20_margin_yi', 'chg_from_oct20_pct']].to_string())

# 1. Classification function
def classify_etf(row):
    sym = str(row['symbol'])
    code = str(row['code'])
    
    # Gold & Commodities & Bonds
    if any(k in sym for k in ['黄金', '金ETF', '白银', '豆粕', '能源化工', '有色']):
        return '商品类'
    if any(k in sym for k in ['债', '国债', '信用债', '政金债', '城投', '可转债']):
        return '债券/货币类'
    if any(k in sym for k in ['纳斯达克', '标普', '纳指', '德国', '日经', '法国', '美股']):
        return '跨境海外'
    if any(k in sym for k in ['恒生', '港股', 'H股', '互联']):
        return '港股通/互联'
        
    # Traditional Broad Broad-based (大盘蓝筹宽基)
    if any(k in sym for k in ['300', '沪深300', '50ETF', '上证50', 'A500', '中证A500', 'A50', '800', 'MSCI中国']):
        return '传统蓝筹宽基 (300/50/A500)'
    if any(k in sym for k in ['500ETF', '中证500', '1000ETF', '中证1000', '2000ETF', '中证2000']):
        return '传统中小盘宽基 (500/1000/2000)'
        
    # Tech Broad-based (双创宽基)
    if any(k in sym for k in ['科创50', '科创板50', '科创100', '双创50', '科创创业', '创业板', '创50', '创业板50']):
        return '科技成长宽基 (科创/创业板)'
        
    # Tech Sector/Themes
    if any(k in sym for k in ['半导体', '芯片', '集成电路']):
        return '半导体/芯片行业'
    if any(k in sym for k in ['通信', '5G', '光通信']):
        return '通信/5G行业'
    if any(k in sym for k in ['软件', '计算机', '大数据', '云计算', '信创', '人工智能', 'AI', '算力', '机器人', '物联网']):
        return '软件/计算/AI行业'
    if any(k in sym for k in ['电子', '消费电子', '元器件']):
        return '电子元器件'
        
    # Financial / Cyclical / Defensive / Dividend
    if any(k in sym for k in ['证券', '券商', '银行', '保险', '金融']):
        return '金融类 (券商/银行)'
    if any(k in sym for k in ['红利', '高股息', '低波']):
        return '红利低波类'
    if any(k in sym for k in ['医药', '医疗', '生物', '中药']):
        return '医药医疗类'
    if any(k in sym for k in ['军工', '航天', '国防']):
        return '军工类'
    if any(k in sym for k in ['光伏', '新能源', '电池', '电力', '风电', '储能']):
        return '新能源类'
    if any(k in sym for k in ['消费', '酒', '食品', '饮料', '家电', '农业']):
        return '消费类'
        
    return '其他行业主题'

df_etf['category'] = df_etf.apply(classify_etf, axis=1)

# Group by category and compute stats
cat_stats = df_etf.groupby('category').agg(
    etf_count=('code', 'count'),
    total_latest_margin=('latest_margin_yi', 'sum'),
    total_sep22_margin=('sep22_margin_yi', 'sum'),
    total_oct20_margin=('oct20_margin_yi', 'sum'),
    total_peak_margin=('peak_margin_yi', 'sum')
).reset_index()

cat_stats['chg_from_sep22_yi'] = cat_stats['total_latest_margin'] - cat_stats['total_sep22_margin']
cat_stats['chg_from_sep22_pct'] = (cat_stats['total_latest_margin'] - cat_stats['total_sep22_margin']) / cat_stats['total_sep22_margin'] * 100

cat_stats['chg_from_oct20_yi'] = cat_stats['total_latest_margin'] - cat_stats['total_oct20_margin']
cat_stats['chg_from_oct20_pct'] = (cat_stats['total_latest_margin'] - cat_stats['total_oct20_margin']) / cat_stats['total_oct20_margin'] * 100

cat_stats['chg_from_peak_yi'] = cat_stats['total_latest_margin'] - cat_stats['total_peak_margin']
cat_stats['chg_from_peak_pct'] = (cat_stats['total_latest_margin'] - cat_stats['total_peak_margin']) / cat_stats['total_peak_margin'] * 100

cat_stats = cat_stats.sort_values('total_latest_margin', ascending=False).reset_index(drop=True)
print("\n=== 全市场 ETF 分大类融资余额变动对比 ===")
print(cat_stats[['category', 'etf_count', 'total_latest_margin', 'chg_from_sep22_pct', 'chg_from_sep22_yi', 'chg_from_oct20_pct', 'chg_from_oct20_yi']].to_string())

cat_stats.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/etf_category_margin_stats.csv', index=False)
