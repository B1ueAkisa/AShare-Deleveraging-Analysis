import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd
import numpy as np

config.init_amazing_data()
base = ad.BaseData()
calendar = base.get_calendar()

# Get all ETF code info
etf_info = base.get_code_info(security_type='EXTRA_ETF')
print(f"Total ETFs in database: {len(etf_info)}")

# User criteria:
# 1. Listed before 2026: list_day < 20260101
etf_info['list_day'] = pd.to_numeric(etf_info['list_day'], errors='coerce')
etfs_pre_2026 = etf_info[etf_info['list_day'] < 20260101].copy()
print(f"ETFs listed before 2026: {len(etfs_pre_2026)}")

# Specific codes mentioned by user:
user_codes = ['588170.SH', '159558.SZ', '560780.SH', '561980.SH', '588200.SH', '588290.SH', '159995.SZ', '512760.SH', '159813.SZ', '560060.SH', '159516.SZ']

# Search keywords in symbol: 半导体, 芯片, 设备, 材料
keywords = ['半导体', '芯片', '设备', '材料']
mask = etfs_pre_2026['symbol'].apply(lambda x: any(kw in str(x) for kw in keywords))
semi_etfs = etfs_pre_2026[mask].copy()

# Add any user_codes that might be missed
for c in user_codes:
    if c in etf_info.index and c not in semi_etfs.index:
        semi_etfs = pd.concat([semi_etfs, etf_info.loc[[c]]])

print(f"\nFiltered pre-2026 Semi/Equipment/Material ETFs count: {len(semi_etfs)}")
print(semi_etfs[['symbol', 'list_day', 'pre_close']].to_string())

# Save to CSV
semi_etfs.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/semi_equipment_material_etfs_list.csv')
