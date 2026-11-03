import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
info = ad.InfoData()
ms = info.get_margin_summary(begin_date=20261102, end_date=20261103)
if ms is not None and not ms.empty:
    ms['TRADE_DATE'] = ms['TRADE_DATE'].astype(str)
    print("Available margin summary dates:")
    print(ms[['TRADE_DATE', 'EXCHANGE', 'SUM_BORROW_MONEY_BALANCE']])
else:
    print("No margin summary yet for 20261103")

# Check SSE 588200.SH and 515880.SH
etf = info.get_margin_detail(['588200.SH', '515880.SH'], begin_date=20261102, end_date=20261103)
for c, df in etf.items():
    if df is not None and not df.empty:
        df['TRADE_DATE'] = df['TRADE_DATE'].astype(str)
        print(f"Margin detail for {c}:")
        print(df[['TRADE_DATE', 'BORROW_MONEY_BALANCE']])
