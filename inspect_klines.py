import pandas as pd
import numpy as np

# Load klines
codes = {
    'sh_comp': '000001.SH',
    'chinext': '399006.SZ',
    'star50': '000688.SH',
    'comm_etf': '515880.SH',
    'chip_etf': '588200.SH',
    'bond30_etf': '511090.SH',
    'gold_etf': '518880.SH'
}

kline_dfs = {}
for name, code in codes.items():
    df = pd.read_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_{code}.csv')
    # print columns and first few rows
    if 'TRADE_DATE' not in df.columns:
        # maybe index or unnamed column
        pass
    kline_dfs[name] = df

print("Columns in 000001.SH kline:", kline_dfs['sh_comp'].columns)
print(kline_dfs['sh_comp'].tail(5))
