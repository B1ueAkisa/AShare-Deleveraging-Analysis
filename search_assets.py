import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd

config.init_amazing_data()
base = ad.BaseData()

# Fetch ETF code info
etf_info = base.get_code_info(security_type='EXTRA_ETF')
print("ETF info shape:", etf_info.shape)
print(etf_info.head())

def search_etf(kw):
    matches = etf_info[etf_info['symbol'].str.contains(kw, na=False)]
    return matches[['symbol', 'pre_close']]

print("\n--- 通信 ---")
print(search_etf("通信"))

print("\n--- 芯片 ---")
print(search_etf("芯片"))

print("\n--- 国债 ---")
print(search_etf("国债"))

print("\n--- 黄金 ---")
print(search_etf("黄金"))

print("\n--- 创业板 / 科创 ---")
print(search_etf("创业板"))
print(search_etf("科创50"))
