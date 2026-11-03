import sys
import os
import pandas as pd
import numpy as np

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
base = ad.BaseData()
info = ad.InfoData()
cal = base.get_calendar()

# 1. Get ETF code list
code_list = base.get_hist_code_list(security_type="EXTRA_ETF")
print(f"Total ETFs in code_list: {len(code_list)}")
print("Sample codes:", code_list[:10])

# 2. Get code info to get ETF names
code_info = base.get_code_info(security_type="EXTRA_ETF")
print(f"Code info shape: {code_info.shape if code_info is not None else None}")
if code_info is not None:
    print(code_info.head(5))
