import pandas as pd
import numpy as np

# Load aggregated margin summary
df_margin = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/aggregated_margin_summary.csv')
df_margin['TRADE_DATE'] = df_margin['TRADE_DATE'].astype(str)

# Filter out incomplete days (e.g. 20261030 if it only has SSE)
# Let's inspect the raw margin summary first
# Let's check max date and recent trajectory
print("--- Aggregated Margin Summary Top 10 Highest Margin Balance Days ---")
print(df_margin.sort_values('SUM_BORROW_MONEY_BALANCE', ascending=False).head(10)[['TRADE_DATE', 'SUM_BORROW_MONEY_BALANCE', 'SUM_PURCH_WITH_BORROW_MONEY', 'SUM_REPAYMENT_OF_BORROW_MONEY']])

print("\n--- Recent Margin Summary (last 15 days up to 20261029) ---")
print(df_margin.iloc[-16:-1][['TRADE_DATE', 'SUM_BORROW_MONEY_BALANCE', 'SUM_PURCH_WITH_BORROW_MONEY', 'SUM_REPAYMENT_OF_BORROW_MONEY']])

# Load target ETFs margin
etfs = ['515880.SH', '588200.SH', '159995.SZ', '159915.SZ', '588000.SH']
for code in etfs:
    path = rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_{code}.csv'
    try:
        m = pd.read_csv(path)
        m['TRADE_DATE'] = m['TRADE_DATE'].astype(str)
        m = m.sort_values('TRADE_DATE').reset_index(drop=True)
        # find peak and recent
        peak_row = m.loc[m['BORROW_MONEY_BALANCE'].idxmax()]
        latest_row = m.iloc[-1]
        print(f"\n--- Margin for {code} ---")
        print(f"Peak: Date {peak_row['TRADE_DATE']}, Balance: {peak_row['BORROW_MONEY_BALANCE']:,.0f}")
        print(f"Latest: Date {latest_row['TRADE_DATE']}, Balance: {latest_row['BORROW_MONEY_BALANCE']:,.0f}")
        pct_change = (latest_row['BORROW_MONEY_BALANCE'] - peak_row['BORROW_MONEY_BALANCE']) / peak_row['BORROW_MONEY_BALANCE'] * 100
        print(f"Change from peak: {pct_change:.2f}%")
    except Exception as e:
        print(f"Error reading margin for {code}: {e}")
